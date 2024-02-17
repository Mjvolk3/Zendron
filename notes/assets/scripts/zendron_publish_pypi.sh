#!/bin/bash
cd /Users/michaelvolk/Documents/projects/Zendron
rm -rf ./dist
eval "$(conda shell.bash hook)"
conda activate zendron
python -m build
twine upload dist/*