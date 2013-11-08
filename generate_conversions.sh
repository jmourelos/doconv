# Generate an image of the graph representing all the available format
# conversions provided by doconv.

if [[ "$VIRTUAL_ENV" != "" ]]; then
    pip install pygraphviz
    pip install -r requirements.txt
    pip install -r test-requirements.txt
    py.test doconv/generate_conversions.py
else
    "A virtualenv environment is required to run this script"
    exit 1
fi

