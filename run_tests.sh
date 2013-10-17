#!/bin/bash

export PYTHONPATH=lib

coverage erase

for f in $(find -name "*.py")
do
    coverage run --append --branch $f || exit 1
done

coverage report --show-missing "--include=lib/*"

pep8 . || exit 1
