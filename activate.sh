#!/usr/bin/env bash

# Call: source activate.sh

source venv/bin/activate

# Have to run this in a way that works with source.
export VERSION_PATH=$( cd "$( dirname "$BASH_SOURCE" )" && pwd )
