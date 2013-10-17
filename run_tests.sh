#!/bin/bash

export PATH=$(pwd)/bin:$PATH
export PYTHONPATH=$(pwd)/lib

coverage erase

for f in $(find lib -name "*.py")
do
    coverage run --branch --parallel-mode $f || exit 1
done

coverage combine
coverage report --show-missing "--include=lib/*" "--omit=lib/ViDE/Shell/*"

for p in tst/Projects/*
do
    cd $p
    coverage run --branch --parallel-mode ../../../bin/vide graph || exit 1
    mv .coverage.* ../../..
    cd ../../..
done

coverage combine
coverage report --show-missing "--include=lib/*"

pep8 --max-line-length=150 . || exit 1