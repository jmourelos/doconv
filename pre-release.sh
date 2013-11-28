#!/bin/bash

# Generates multiple text files to be used by Sphinx to enrich
# the documentation generated.

if [[ "$VIRTUAL_ENV" != "" ]]; then
    pip install -r requirements.txt
    pip install -r test-requirements.txt
    pip install -r release-requirements.txt

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

