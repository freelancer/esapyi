#!/usr/bin/env bash

# Activate the virtualenv for this project
source $(poetry env info --path)/bin/activate

set -x
$@
