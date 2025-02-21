#!/bin/bash

# Source and Destination Directories
SRC_DIR="/data/Version_0_4_2"
export CABE_DATA_DIR="/home/site/wwwroot/data"  # Set environment variable
LOG_FILE="/var/log/data_copy.log"

# Ensure destination directory exists
mkdir -p "$CABE_DATA_DIR"

# Copy the files using rsync
rsync -av --progress "$SRC_DIR/" "$CABE_DATA_DIR/" | tee -a "$LOG_FILE"

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Copy completed successfully to $CABE_DATA_DIR" | tee -a "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Copy failed" | tee -a "$LOG_FILE"
    exit 1
fi