#!/usr/bin/env bash

# Error as soon as a command returns a non-zero code
set -e

# Get the current git commit for tagging purposes
GIT_COMMIT=$(git rev-parse HEAD)

function docker_build {
    docker build --file $1 --tag $2:$GIT_COMMIT .
}

function docker_run {
    docker run --rm --user root:root --name "$1" --volume `pwd`:/code $1:$GIT_COMMIT
}

function kill_if_exists {
    docker rm -f $1 || true
}

function find_container {
    docker ps --quiet --all --filter name="$1"
}

function kill_container {
    docker rm -f $1
}

function print_title {
    echo "=============================================="
    echo $1
    echo "=============================================="
}

function python_lint {
    docker_build lib/docker/lint/mypy/Dockerfile api-boilerplate-lint-mypy
    print_title "Running mypy"
    docker_run api-boilerplate-lint-mypy

    docker_build lib/docker/lint/pylint/Dockerfile api-boilerplate-lint-pylint
    print_title "Running pylint"
    docker_run api-boilerplate-lint-pylint
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
    DB_CONTAINER=$(find_container api-boilerplate-mysql-testing-db)
    if [[ $DB_CONTAINER != "" ]]; then
        kill_container api-boilerplate-mysql-testing-db
    fi

    docker create \
        --name api-boilerplate-mysql-testing-db \
        --env MYSQL_DATABASE=api_boilerplate \
        --env MYSQL_USER=dev \
        --env MYSQL_PASSWORD=dev \
        --env MYSQL_ROOT_PASSWORD=root \
        mysql:8
    docker start api-boilerplate-mysql-testing-db
}

function dev_utilities {
    db
}

function dev_app {
    docker_build lib/docker/dev_app/Dockerfile api-boilerplate-dev-app
    kill_if_exists api-boilerplate-dev-app
    dev_utilities
    print_title "Starting Flask App"
    docker run \
        -ti \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --publish 8080:8080 \
        --link api-boilerplate-mysql-db:api-boilerplate-db \
        --env REALM=local_development \
        --name api-boilerplate-dev-app \
        api-boilerplate-dev-app:$GIT_COMMIT
}

# start the python server using the prod config
function prod_app {
    docker_build lib/docker/prod_app/Dockerfile api-boilerplate-dev-app
    kill_if_exists api-boilerplate-dev-app
    dev_utilities
    print_title "Starting Flask App"
    docker run \
        -ti \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --publish 8080:8080 \
        --link api-boilerplate-mysql-db:api-boilerplate-db \
        --env REALM=local_development \
        --name api-boilerplate-dev-app \
        api-boilerplate-dev-app:$GIT_COMMIT
}

function alembic {
    docker_build lib/docker/alembic/Dockerfile api-boilerplate-alembic
    dev_utilities
    docker run \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --env REALM=local_development \
        --link api-boilerplate-mysql-db:api-boilerplate-db \
        --name api-boilerplate-alembic \
        api-boilerplate-alembic:$GIT_COMMIT \
        alembic $@
}

function attach_to_dev_db {
    dev_utilities
    docker exec -ti api-boilerplate-mysql-db mysql -proot
}

function python_test {
    testing_db
    docker_build lib/docker/test/Dockerfile api-boilerplate-test-pytest
    print_title "Running pytest"
    docker run \
        -ti \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --link api-boilerplate-mysql-testing-db:api-boilerplate-db \
        --env REALM=testing \
        --name api-boilerplate-test-pytest \
        api-boilerplate-test-pytest:$GIT_COMMIT
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
    "prod")
        prod_app
        ;;
    "alembic")
        alembic ${@:$OPTIND+1}
        ;;
    *)
        echo "Invalid command"
        ;;
esac
