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
    docker_build lib/docker/lint/mypy/Dockerfile dm-management-lint-mypy
    print_title "Running mypy"
    docker_run dm-management-lint-mypy

    docker_build lib/docker/lint/pylint/Dockerfile dm-management-lint-pylint
    print_title "Running pylint"
    docker_run dm-management-lint-pylint
}

function db {
    DB_CONTAINER=$(find_container dm-management-mysql-db)
    if [[ $DB_CONTAINER == "" ]]; then
        docker create \
            --name dm-management-mysql-db \
            --env MYSQL_DATABASE=dm_management \
            --env MYSQL_USER=dev \
            --env MYSQL_PASSWORD=dev \
            --env MYSQL_ROOT_PASSWORD=root \
            mysql:8
    fi

    docker start dm-management-mysql-db
}

function testing_db {
    DB_CONTAINER=$(find_container dm-management-mysql-testing-db)
    if [[ $DB_CONTAINER != "" ]]; then
        kill_container dm-management-mysql-testing-db
    fi

    docker create \
        --name dm-management-mysql-testing-db \
        --env MYSQL_DATABASE=dm_management \
        --env MYSQL_USER=dev \
        --env MYSQL_PASSWORD=dev \
        --env MYSQL_ROOT_PASSWORD=root \
        mysql:8
    docker start dm-management-mysql-testing-db
}

function dev_utilities {
    db
}

function dev_app {
    docker_build lib/docker/dev_app/Dockerfile dm-management-dev-app
    kill_if_exists dm-management-dev-app
    dev_utilities
    print_title "Starting Flask App"
    docker run \
        -ti \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --publish 8080:8080 \
        --link dm-management-mysql-db:dm-management-db \
        --env REALM=local_development \
        --name dm-management-dev-app \
        dm-management-dev-app:$GIT_COMMIT
}

# start the python server using the prod config
function prod_app {
    docker_build lib/docker/prod_app/Dockerfile dm-management-dev-app
    kill_if_exists dm-management-dev-app
    dev_utilities
    print_title "Starting Flask App"
    docker run \
        -ti \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --publish 8080:8080 \
        --link dm-management-mysql-db:dm-management-db \
        --env REALM=local_development \
        --name dm-management-dev-app \
        dm-management-dev-app:$GIT_COMMIT
}

function alembic {
    docker_build lib/docker/alembic/Dockerfile dm-management-alembic
    dev_utilities
    docker run \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --env REALM=local_development \
        --link dm-management-mysql-db:dm-management-db \
        --name dm-management-alembic \
        dm-management-alembic:$GIT_COMMIT \
        alembic $@
}

function attach_to_dev_db {
    dev_utilities
    docker exec -ti dm-management-mysql-db mysql -proot
}

function python_test {
    testing_db
    docker_build lib/docker/test/Dockerfile dm-management-test-pytest
    print_title "Running pytest"
    docker run \
        -ti \
        --rm \
        --user root:root \
        --volume `pwd`:/code \
        --link dm-management-mysql-testing-db:dm-management-db \
        --env REALM=testing \
        --name dm-management-test-pytest \
        dm-management-test-pytest:$GIT_COMMIT
}

while getopts ":c" opt; do
    case $opt in
        c)
            echo "-c run with $OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
        :)
            echo "Option -$OPTARG requires an argument" >&2
            ;;
    esac
done

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
