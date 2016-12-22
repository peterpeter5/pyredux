from setuptools import setup
from pip.req import parse_requirements
import os

basepath = os.path.dirname(__file__)
requirements = parse_requirements(os.path.join(basepath, "./requirements.txt"), session="hack")
install_req = reqs = [str(ir.req) for ir in requirements]

setup(
    name='PyRedux',
    version='0.0.3',
    packages=['pyredux'
              ],
    url='https://github.com/peterpeter5/pyredux',
    license='MIT',
    author='peter',
    author_email='dev.peterpeter5@gmail.com',
    description='Python-Version of redux.js',
    test_suite='pyredux.Test',
    install_requires=install_req
    # tests_require=['nose'],
)
