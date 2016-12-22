#!/usr/bin/env bash

mkdir -p ./pyredux

cp -r ../../pyredux/Test ./pyredux/Test
cp ../../run_testsuite.py ./run_testsuite.py

virtualenv TestEnv
source ./TestEnv/bin/activate
pip install ../dist/PyRedux-*.whl

python run_testsuite.py