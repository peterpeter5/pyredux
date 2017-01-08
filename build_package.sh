#!/usr/bin/env bash
rm -r -f ./Deploy/
mkdir -p ./Deploy/dist/
mkdir -p ./Deploy/Test/

source ./PyEnv/bin/activate
python setup.py test
python setup.py flake8

python setup.py build bdist_wheel --bdist-dir ./Deploy/build --dist-dir ./Deploy/dist
rm -r -f ./build/
cp -r *.egg-info ./Deploy/dist/
rm -r -f *.egg-info
cp ./test_package.sh ./Deploy/Test/test_package_1.sh
cd ./Deploy/Test/

bash ./test_package_1.sh

