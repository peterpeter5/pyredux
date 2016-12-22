#!/usr/bin/env bash
rm -r -f ./Deploy/dist/
mkdir -p ./Deploy/dist/

source ./PyEnv/bin/activate

python setup.py build bdist_wheel --bdist-dir ./Deploy/build --dist-dir ./Deploy/dist
rm -r -f ./build/
