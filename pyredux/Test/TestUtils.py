from __future__ import absolute_import, unicode_literals
import unittest

from pyredux.Utils import compose, NotCallableError


class TestCompose(unittest.TestCase):

    def test_calling_compose_with_not_callable_args_raises_error(self):
        self.assertRaises(
            NotCallableError,
            compose,
            lambda x: x, "a", dict()
        )

    def test_non_composeable_args_are_listed_in_error_msg(self):
        call_able_args = (lambda x: x, lambda y: y)
        non_callble_args = ("a_string", dict())
        non_callble_args_representation = list(map(str, non_callble_args))
        call_able_args_representation = list(map(str, call_able_args))
        try:
            compose(*(call_able_args + non_callble_args))
        except NotCallableError as error:
            error_message = getattr(error, "message", str(error))
        callables_not_in_error = map(
            lambda represent: str(represent) not in error_message,
            call_able_args_representation
        )
        non_callables_are_in_error = map(
            lambda represent: str(represent) in error_message,
            non_callble_args_representation
        )
        self.assertTrue(all(callables_not_in_error))
        self.assertTrue(all(non_callables_are_in_error))

    def test_composing_two_funcs_from_right_to_left(self):
        def double(x):
            return x * 2

        def square(x):
            return x ** 2

        self.assertEqual(compose(square, double)(5), 100)

    def test_composing_more_than_two_funcs_from_right_to_left(self):
        def double(x):
            return x * 2

        def square(x):
            return x ** 2

        def half(x):
            return x / 2

        self.assertEqual(compose(double, square, half)(8), 32)
        self.assertEqual(compose(double, half, square)(8), 64)
        self.assertEqual(compose(half, square, double)(8), 128)

    def test_composing_only_one_function_returns_identity(self):
        double = lambda x: x * 2
        self.assertEqual(double, compose(double))

    def test_composing_zero_function_raises_type_error(self):
        self.assertRaises(
            TypeError,
            compose
        )