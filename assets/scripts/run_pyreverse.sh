#!/bin/bash
source /Users/michaelvolk/opt/miniconda3/envs/torchcell/bin/activate

# Initialize conda for the current shell session
conda init bash

# Activate the conda environment
conda activate torchcell
FILE_PATH=$1
FILE_NAME=$(basename -- "$FILE_PATH")
FILE_NAME_WITHOUT_EXT="${FILE_NAME%.*}"
DATE_TIME=$(date "+%Y.%m.%d.%H.%M.%S")
OUTPUT_DIR="notes/assets/images"

pyreverse -o png -p MyProjectName "$FILE_PATH"
mv classes_MyProjectName.png "$OUTPUT_DIR/${FILE_NAME_WITHOUT_EXT}-${DATE_TIME}-classes.png"
mv packages_MyProjectName.png "$OUTPUT_DIR/${FILE_NAME_WITHOUT_EXT}-${DATE_TIME}-packages.png"
