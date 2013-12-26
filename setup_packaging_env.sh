#!/bin/bash

function check_if_sourced() {
    if [ "${FUNCNAME[1]}" != source ]; then
        echo "This script requires to be sourced"
        exit 1
    fi
}
check_if_sourced

if [[ "$VIRTUAL_ENV" != "" ]]; then
    CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    export DOCONV_DEV_DIR=$CURRENT_SCRIPT_DIR

    # generate doconv-version.tar.gz in $DOCONV_DEV_DIR/dist. This to be mounted
    # inside docker machines for packaging purposes.
    cd $DOCONV_DEV_DIR
    make sdist
    cd -
else
    "A virtualenv environment is required to run this script"
fi
