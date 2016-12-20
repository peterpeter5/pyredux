from __future__ import absolute_import, unicode_literals
from functools import wraps
from pyredux.Utils import compose


def middleware(func):
    def middleware_wrapper(store):
        def _next_middleware_wrapper(next_middleware):

            @wraps(func)
            def _inner(*args, **kwargs):
                return func(store, next_middleware, *args, **kwargs)
            return _inner

        return _next_middleware_wrapper
    return middleware_wrapper


class RestrictedStore(object):

    def __init__(self, store):
        self.__store = store

    @property
    def state(self):
        return self.__store.state

    def dispatch(self, action):
        return self.__store.dispatch(action)


def apply_middleware(*middlewares):
    """
    :param middlewares: middleware-functions to use with pyredux
    :return: wrapper-function to use with create_store
    """

    def store_wrapper(create_store):

        def chained_middleware(reducer, preloaded_state):
            store = create_store(reducer, preloaded_state)
            middleware_api_store = RestrictedStore(store)
            middle_store_initialized = map(lambda middle: middle(middleware_api_store), middlewares)
            chained_dispatcher = compose(*middle_store_initialized)(store.dispatch)
            store.dispatch = chained_dispatcher
            return store

        return chained_middleware

    return store_wrapper
