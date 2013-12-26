#!/bin/bash

# install doconv
dpkg -i /tmp/doconv/sources/python-doconv*.deb

# install doconv dependencies
apt-get --fix-broken --no-install-recommends install
