#!/bin/bash

# Define the destination directory
dest_dir="notes/assets/notability"

# Create the destination directory if it doesn't exist
mkdir -p "$dest_dir"

# Copy the file
cp "/Users/michaelvolk/Library/CloudStorage/GoogleDrive-michaeljvolk7@gmail.com/My Drive/Notability/Projects/torchcell/Note Aug 21, 2023 at 1_27_15 PM.pdf" "${dest_dir}/notability.pdf"
