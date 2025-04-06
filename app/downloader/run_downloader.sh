#!/bin/bash

# Change to the script directory
cd "$(dirname "$0")"

# Run the downloader with the specified config
python3 app.downloader.py --config local.config.json 