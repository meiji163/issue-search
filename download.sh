#!/usr/bin/env bash
set -e

help() {
    cat <<EOF
Usage: $0 -R <repo> [-L <max-issues>]

Download issues from a GitHub repository.
EOF
}

repo=''
limit=1000

while getopts 'R:L:' flag; do
    case "${flag}" in
        R) repo="${OPTARG}" ;;
        L) limit="${OPTARG}" ;;
        *) help
           exit 1 ;;
    esac
done

if [[ -z "$repo" ]]; then
    help
    exit 1
fi

if [ ! -d "data" ]; then
    mkdir data 
fi

path="data/${repo/\//-}-issues.json"

gh issue list -R "$repo" -L "$limit" \
    --state all \
    --json number,title,body,comments,labels\
    > "$path"
