#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
doconv_dev_dir=$script_dir/../../..

docker run -t -i -v $doconv_dev_dir/packaging/archlinux/build:/tmp/doconv/build -v $doconv_dev_dir/packaging/archlinux/install:/tmp/doconv/install doconv/archlinux-install /bin/bash
