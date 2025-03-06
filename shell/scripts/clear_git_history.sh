#!/bin/bash

# Check if a commit message is provided
if [ -z "$1" ]; then
  echo "Usage: ./clear_git_history.sh '<commit_message>'"
  exit 1
fi

# Create an orphan branch
git checkout --orphan latest_branch

# Add all files to the new branch
git add -A

# Commit changes with the provided message
git commit -am "$1"

# Delete the main branch
git branch -D main

# Rename the new branch to main
git branch -m main

# Force push to update the remote repository
git push -f origin main

echo "Git history cleared and pushed to remote."