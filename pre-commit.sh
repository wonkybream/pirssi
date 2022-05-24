#!/usr/bin/env bash

set -e

black ./
isort ./
mypy ./
flake8

python -m unittest -v
