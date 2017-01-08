import os

from pkg_resources import parse_requirements
from setuptools import setup

install_req = "pyrsistent==0.11.13"
install_req_test = [
    "nose",
    "coverage",
    "flake8",
    "pep8-naming"
]

setup(
    name='pyredux',
    version='1.0.1',
    packages=['pyredux'
              ],
    url='https://github.com/peterpeter5/pyredux',
    license='MIT',
    author='peter',
    author_email='dev.peterpeter5@gmail.com',
    description='Python-Version of redux.js',
    test_suite='pyredux.test',
    install_requires=install_req,
    tests_require=install_req_test,
)