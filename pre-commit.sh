#!/usr/bin/env bash

set -e

pip install --upgrade pip

black ./
isort ./
mypy ./
flake8

python -m unittest -v
