from __future__ import unicode_literals, absolute_import

from pyredux.ErrorsAndConstants import NoSubscriptionFoundError, StoreInitAction
from pyrsistent import pmap, pvector


class Store(object):
    def __init__(self, reducer, preloaded_state=None):
        self.__reducer = reducer
        self.__state = preloaded_state
        self.__subscriber = pvector()

    def dispatch(self, action):

        if isinstance(action, StoreInitAction):
            new_state = self.__setup_reducers(action)
        else:
            new_state = self.__reducer(action, self.state)
        self.__state = new_state
        for subscriber in self.__subscriber:
            subscriber(self)
        return new_state

    def __setup_reducers(self, action):
        if self.__state is None:
            return self.__reducer(action)
        else:
            return self.__reducer(action, self.__state)

    @property
    def state(self):
        if self.__state is None:
            return pmap({})
        else:
            return self.__state

    def subscribe(self, subscriber):
        self.__subscriber = self.__subscriber.append(subscriber)
        return self

    def unsubscribe(self, subscriber):
        try:
            self.__subscriber = self.__subscriber.remove(subscriber)
        except ValueError:
            raise NoSubscriptionFoundError("Didn't found subscription for: %s" % subscriber)

    def replace_reducer(self, new_reducer):
        self.__reducer = new_reducer
        return self

    @property
    def _subscriber(self):
        return self.__subscriber


def create_store(reducer, preloaded_state=None, enhancer=None):
    """
    :param reducer: reducer-function (single-function)
    :param preloaded_state: the preloaded-state your application should start with
    :type preloaded_state: pyrsistent.PMap
    :param enhancer: enhancer-function. Mostly used for apply_middleware
    :rtype: Store
    """
    if enhancer is not None:
        return enhancer(create_store)(reducer, preloaded_state)

    store = Store(reducer, preloaded_state)
    store.dispatch(StoreInitAction())
    return store
