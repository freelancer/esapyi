#!/usr/bin/env bash

# Error as soon as a command returns a non-zero code
set -e

function validate_arguments {
    if [ $# -ne 1 ]; then
        echo "This script expects exactly 1 argument" >&2
        exit 1
    fi

    if ! [[ $1 =~ ^[a-z_]+$ ]]; then
        echo "The input name should match '^[a-z_]+$'"
        exit 1
    fi
}

validate_arguments "$@"

# constant for the current project name
PROJECT_NAME='dm_management'
DASH_PROJECT_NAME=$(echo $PROJECT_NAME | sed 's/_/-/g')

# setup two project names, one with a "-" and one with "_"
dash_name=$(echo $1 | sed 's/_/-/g')
underscore_name=$(echo $1 | sed 's/-/_/g')

# capture all files that need processing
all_files=$(find . -not -path '*/\.*' -not -path '*/__pycache__*' -type f -print0 | cat | xargs -0 echo)

# rename all underscore names
echo $all_files | xargs sed -i "s/${PROJECT_NAME,,}/${underscore_name,,}/g"
echo $all_files | xargs sed -i "s/${PROJECT_NAME^^}/${underscore_name^^}/g"

# rename all dash names
echo $all_files | xargs sed -i "s/${DASH_PROJECT_NAME,,}/${dash_name,,}/g"
echo $all_files | xargs sed -i "s/${DASH_PROJECT_NAME^^}/${dash_name^^}/g"


# rename the root folder
mv "${PROJECT_NAME}/" $underscore_name
