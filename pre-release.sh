#!/bin/bash

### This script performs multiple actions needed to release.

# Generate multiple text files to be used by Sphinx to enrich
# the documentation generated.
if [[ "$VIRTUAL_ENV" != "" ]]; then
    pip install -r requirements.txt
    pip install -r test-requirements.txt
    pip install -r release-requirements.txt
    python setup.py install

    # generate supported format conversions graph for documentation
    py.test doconv/generate_conversions.py
    sed -i 's|plugin=|label=|g' conversions.dot
    mv conversions.dot pre_release_generated/

    # generate CLI usage for documentation
    doconv convert -h > pre_release_generated/doconv_convert_usage.txt
else
    "A virtualenv environment is required to run this script"
    exit 1
fi

# Update release history
read -p "Introduce the new version to be released: " version

echo -e "\n\n$version ($(date +%F))" >> HISTORY.rst
echo -e "++++++++++++++++++\n" >> HISTORY.rst

while true; do
    read -p "Do you have any additional message to add to the release notes? " yn
    case $yn in
        [Yy]* ) read -p "Write your message: " release_message
                echo -e "* $release_message" >> HISTORY.rst
                ;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Update the version of doconv specified in different source files
sed -i "s|^VERSION = .\+$|VERSION = '$version'|" doconv/__init__.py
sed -i "s|^pkgver=.\+$|pkgver=$version|" packaging/archlinux/build/PKGBUILD
sed -i "s|^doconv_version=.\+$|doconv_version=$version|" packaging/ubuntu/12.10/build/build_doconv_deb_and_source.sh
sed -i "s|doconv_.\+-1_source.changes$|doconv_$version\-1_source.changes|" packaging/ubuntu/12.10/build/upload.txt

# Commit to repo the changes performed until this point
git add pre_release_generated/
git add HISTORY.rst doconv/__init__.py packaging/archlinux/build/PKGBUILD\
    packaging/ubuntu/12.10/build/build_doconv_deb_and_source.sh packaging/ubuntu/12.10/build/upload.txt

git commit -m "prepare for release $version"
