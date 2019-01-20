#!/bin/bash
set -e
pip freeze | cut -d = -f 1 | pip install -U -r /dev/stdin
pip freeze > requirements.txt
