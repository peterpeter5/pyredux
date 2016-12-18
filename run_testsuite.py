from __future__ import absolute_import, unicode_literals
import itertools
import os
from nose.loader import TestLoader
import nose
from nose.suite import LazySuite


base_path = os.path.dirname(__file__)
paths = (os.path.join(base_path, "pyredux"),)


def run_my_tests():
    all_tests = ()
    for path in paths:
        all_tests = itertools.chain(all_tests, TestLoader().loadTestsFromDir(path))
    suite = LazySuite(all_tests)

    nose.run(suite=suite, argv=["--with-coverage", "--cover-html"])

if __name__ == '__main__':
    run_my_tests()