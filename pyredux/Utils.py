from __future__ import absolute_import, unicode_literals
try:
    from functools import reduce
except ImportError:
    pass


class NotCallableError(Exception):
    pass


def compose(*functions):

    def compose_two_funcs(func1, func2):

        def _composition(*args, **kwargs):
            return func2(func1(*args, **kwargs))
        return _composition

    def composition(*args, **kwargs):
        funcs = reversed(functions)
        composed = reduce(compose_two_funcs, funcs)
        return composed(*args, **kwargs)

    __check_and_raises_for_composability(functions)

    if len(functions) == 1:
        return functions[0]

    return composition


def __check_and_raises_for_composability(functions):
    if len(functions) == 0:
        raise TypeError("Expected one or more function to compose")
    non_callable_args = filter(lambda func: not callable(func), functions)
    if len(non_callable_args) > 0:
        raise NotCallableError(
            "arguments <%s> are not callable and therefor can not be composed" % list(non_callable_args)
        )


