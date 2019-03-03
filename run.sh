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

function print_title {
    echo "=============================================="
    echo $1
    echo "=============================================="
}

function lint {
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

function dev_utilities {
    db
}

function dev {
    docker_build lib/docker/dev/Dockerfile dm-management-dev-app
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
        lint
        ;;
    "dev")
        dev
        ;;
    *)
        echo "Invalid command"
        ;;
esac
