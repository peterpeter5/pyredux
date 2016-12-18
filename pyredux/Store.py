from __future__ import unicode_literals, absolute_import

from pyredux.ErrorsAndConstants import NoSubscriptionFoundError, StoreInitAction
from pyrsistent import pmap, pvector


class Store(object):
    def __init__(self, reducer):
        self.__reducer = reducer
        self.__state = pmap({})
        self.__subscriber = pvector()

    def dispatch(self, action):

        if isinstance(action, StoreInitAction):
            new_state = self.__reducer(action=action)
        else:
            new_state = self.__reducer(action, self.__state)
        self.__state = new_state
        for subscriber in self.__subscriber:
            subscriber(self)
        return new_state

    @property
    def state(self):
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
    if enhancer is not None:
        return enhancer(create_store)(reducer, preloaded_state)
    if preloaded_state is not None:
        raise NotImplementedError("Future work")

    store = Store(reducer)
    store.dispatch(StoreInitAction())
    return store
