#!/usr/bin/env bash

mkdir -p ./pyredux

cp -r ../../pyredux/test ./pyredux/test
cp ../../run_testsuite.py ./run_testsuite.py

virtualenv TestEnv
source ./TestEnv/bin/activate
pip install ../dist/pyredux-*.whl
pip install -r ../../requirements.test.txt

python run_testsuite.py
