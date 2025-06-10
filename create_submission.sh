#!/bin/bash

# Get current timestamp for unique filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Remove submit directory if it exists and create a new empty one
if [ -d "submit" ]; then
    echo "Removing existing submit directory..."
    rm -rf submit
fi

echo "Creating submit directory..."
mkdir submit

# Copy directories and files to submit
echo "Copying files and directories..."

# Copy directories
mkdir -p submit/objects/
mkdir -p submit/tests/
mkdir -p submit/tools/
mkdir -p submit/utils/

cp -r objects/ submit/objects/.
cp -r tests/ submit/tests/.
cp -r tools/ submit/tools/.
cp -r utils/ submit/utils/.

# Copy evaluation.py file
cp evaluation.py submit/.

echo "Files copied successfully!"

# Create zip file with timestamp
ZIP_NAME="submission-${TIMESTAMP}.zip"
echo "Creating zip file: $ZIP_NAME"

zip -r "$ZIP_NAME" submit/

echo "Submission package created: $ZIP_NAME"
echo "Contents of submit directory:"
ls -la submit/ 