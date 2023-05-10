#!/usr/bin/env bash

# Error as soon as a command returns a non-zero code
set -e

# Get the current git commit for tagging purposes
GIT_COMMIT=$(git rev-parse HEAD)
if [ -t 1 ] ; then
    DOCKER_TERMINAL_FLAGS="-ti"
else
    DOCKER_TERMINAL_FLAGS=""
fi

function docker_build {
    docker build --file $1 --tag $2:$GIT_COMMIT .
}

function docker_run {
    docker run $DOCKER_TERMINAL_FLAGS --rm --user root:root --name "$1" $1:$GIT_COMMIT "${*:2}"
}

function kill_if_exists {
    docker rm -f $1 || true
}

function find_container {
    docker ps --quiet --all --filter name="$1"
}

function print_title {
    echo "=============================================="
    echo $1
    echo "=============================================="
}

function dev_utilities {
    db
}

function db {
    DB_CONTAINER=$(find_container api-boilerplate-mysql-db)
    if [[ $DB_CONTAINER == "" ]]; then
        docker create \
            --name api-boilerplate-mysql-db \
            --env MYSQL_DATABASE=api_boilerplate \
            --env MYSQL_USER=dev \
            --env MYSQL_PASSWORD=dev \
            --env MYSQL_ROOT_PASSWORD=root \
            mysql:8
    fi

    docker start api-boilerplate-mysql-db
}

function testing_db {
    kill_if_exists api-boilerplate-mysql-testing-db

    docker create \
        --name api-boilerplate-mysql-testing-db \
        --env MYSQL_DATABASE=api_boilerplate \
        --env MYSQL_USER=dev \
        --env MYSQL_PASSWORD=dev \
        --env MYSQL_ROOT_PASSWORD=root \
        mysql:8
    docker start api-boilerplate-mysql-testing-db
}

function attach_to_dev_db {
    dev_utilities
    docker exec $DOCKER_TERMINAL_FLAGS api-boilerplate-mysql-db mysql -proot
}

function python_lint {
    docker_build lib/docker/dev/Dockerfile api-boilerplate-lint-runtime
    print_title "Running pyright"
    docker_run api-boilerplate-lint-runtime pyright
    print_title "Running ruff"
        mkdir -p .ruff_cache
        docker run \
        $DOCKER_TERMINAL_FLAGS \
        --rm \
        --user root:root \
        --volume `pwd`/.ruff_cache:/code/.ruff_cache \
        --name api-boilerplate-lint-runtime \
        api-boilerplate-lint-runtime:$GIT_COMMIT ruff check .
}

function python_test {
    testing_db
    docker_build lib/docker/dev/Dockerfile api-boilerplate-dev-runtime
    print_title "Running pytest"
    docker run \
        $DOCKER_TERMINAL_FLAGS \
        --rm \
        --user root:root \
        --link api-boilerplate-mysql-testing-db:api-boilerplate-db \
        --env REALM=testing \
        --name api-boilerplate-test-runtime \
        api-boilerplate-dev-runtime:$GIT_COMMIT pytest tests
}

function dev_app {
    docker_build lib/docker/dev/Dockerfile api-boilerplate-dev-runtime
    kill_if_exists api-boilerplate-dev-runtime
    dev_utilities
    print_title "Starting Flask App"
    docker run \
        $DOCKER_TERMINAL_FLAGS \
        --rm \
        --user root:root \
        --volume `pwd`/api_boilerplate:/code/api_boilerplate \
        --publish 8080:8080 \
        --link api-boilerplate-mysql-db:api-boilerplate-db \
        --env REALM=local_development \
        --name api-boilerplate-dev-runtime \
        api-boilerplate-dev-runtime:$GIT_COMMIT python api_boilerplate/app.py python api_boilerplate/app.py
}

function alembic {
    docker_build lib/docker/dev/Dockerfile api-boilerplate-dev-runtime
    dev_utilities
    docker run \
        --rm \
        --user root:root \
        --env REALM=local_development \
        --link api-boilerplate-mysql-db:api-boilerplate-db \
        --name api-boilerplate-alembic-runtime \
        api-boilerplate-dev-runtime:$GIT_COMMIT alembic $@
}

# start the python app using the production uWSGI server
function prod_app {
    docker_build lib/docker/prod_app/Dockerfile api-boilerplate-prod-runtime
    kill_if_exists api-boilerplate-prod-runtime
    dev_utilities
    print_title "Starting Flask App with uWSGI"
    docker run \
        $DOCKER_TERMINAL_FLAGS \
        --rm \
        --user root:root \
        --volume `pwd`/api_boilerplate:/code/api_boilerplate \
        --publish 8080:8080 \
        --link api-boilerplate-mysql-db:api-boilerplate-db \
        --env REALM=local_development \
        --name api-boilerplate-prod-app \
        api-boilerplate-prod-runtime:$GIT_COMMIT
}

case ${@:$OPTIND:1} in
    "lint")
        python_lint
        ;;
    "test")
        python_test
        ;;
    "check")
        python_lint
        python_test
        ;;
    "dev")
        case ${@:$OPTIND+1:1} in
            "db")
                attach_to_dev_db
                ;;
            "")
                dev_app
                ;;
        esac
        ;;
    "alembic")
        alembic ${@:$OPTIND+1}
        ;;
    "prod")
        prod_app
        ;;
    *)
        echo "Invalid command"
        ;;
esac
