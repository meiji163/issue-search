#!/usr/bin/env bash
set -e

if [ "$#" -ne 1 ]; then
    printf "Usage: $0 <repo>\n" 
    exit 1
fi

gh issue list -R "$1" \
    -L 3000 --state all \
    --json number,title,body,comments\
    > issues.json
