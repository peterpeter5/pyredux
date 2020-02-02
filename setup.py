from setuptools import setup
from pip.req import parse_requirements
import os

basepath = os.path.dirname(__file__)
install_req = "pyrsistent>=0.11.4"

requirements_test = parse_requirements(os.path.join(basepath, "./requirements.test.txt"), session="hack")
install_req_test = reqs_test = [str(ir.req) for ir in requirements_test]

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
    python_requires='>=3.5'
)
