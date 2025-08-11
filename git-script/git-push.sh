#!/bin/bash
# Generate a dynamic commit message with the current timestamp
COMMIT_MESSAGE="Update by Doddi Priyambodo on $(date '+%A, %Y-%m-%d %H:%M:%S')"

# Stage all changes
git add .

# Commit with the dynamic message
git commit -m "$COMMIT_MESSAGE"

# Push to the main branch
git push origin main