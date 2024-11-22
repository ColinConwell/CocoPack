#!/bin/bash

# Initialize Coco-Pack by sourcing the scripts in the parent directory of this file
source "$(dirname "$0")/ezshell.sh"
source "$(dirname "$0")/prompt.sh"
source "$(dirname "$0")/colorcode.sh"

# Install to /usr/local/bin
sudo cp "$(dirname "$0")/cocopack.sh" /usr/local/bin/cocopack
sudo cp "$(dirname "$0")/ezshell.sh" /usr/local/bin/ezshell
sudo cp "$(dirname "$0")/prompt.sh" /usr/local/bin/prompt
sudo cp "$(dirname "$0")/colorcode.sh" /usr/local/bin/colorcode
