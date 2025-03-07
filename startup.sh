#!/bin/bash

# Check if rsync is installed
if ! command -v rsync &> /dev/null
then
    echo "rsync is not installed. Installing..."
    apt-get update
    apt-get install -y rsync
else
    echo "rsync is already installed."
fi

# Source and Destination Directories
SRC_DIR="/data/Version_0_4_2"
CABE_DATA_DIR="/home/site/wwwroot/data"
LOG_FILE="/var/log/data_copy.log"

# Ensure destination directory exists
mkdir -p "$CABE_DATA_DIR"
mkdir -p /home/site/wwwroot/logs

# Copy the files using rsync
find "$SRC_DIR" -type f | xargs -n 1 -P 4 -I {} rsync -zav --inplace --progress --checksum {} "$CABE_DATA_DIR/" | tee -a "$LOG_FILE"

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Copy completed successfully to $CABE_DATA_DIR" | tee -a "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Copy failed" | tee -a "$LOG_FILE"
    exit 1
fi