#!/usr/bin/env bash

source /env.sh
python3 /tony.py --username "$TONY_USERNAME" --password "$TONY_PASSWORD" --playlist "$TONY_PLAYLIST" --cache-path /tony_cache
