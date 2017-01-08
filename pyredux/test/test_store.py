from __future__ import absolute_import, unicode_literals
import unittest

from pyrsistent import freeze
from pyrsistent import pmap
from pyredux.store import Store, create_store
from pyredux.static_data import NoSubscriptionFoundError


def static_reducer(action, state=pmap()):
    return state.update({"action": action})


def add_to_string_reducer(action, state=pmap()):
    return state.update({"action": "new" + action})


def init_reducer(action, state=pmap({"init": True})):
    return state


def do_nothing_reducer(action, state):
    return state


class TestStore(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, "assertItemsEqual"):
            self.assertItemsEqual = self.assertCountEqual

    def test_store_exposes_pythonic_js_api_plus_unsubscribe(self):
        store = Store(static_reducer)
        methods = dir(store)
        public_methods = filter(lambda method_name: not method_name.startswith("_"), methods)
        expected_public_methods = ["dispatch", "subscribe", "state", "replace_reducer", "unsubscribe"]
        self.assertItemsEqual(
            public_methods,
            expected_public_methods
        )

    def test_initial_state_of_store_is_empty_pmap(self):
        store = Store(static_reducer)
        initial_state = store.state
        self.assertEqual(pmap({}), initial_state)

    def test_store_updates_its_state_after_dispatch(self):
        store = Store(static_reducer)
        store.dispatch("unittest")
        self.assertEqual(store.state, pmap({"action": "unittest"}))

    def test_dispatch_calls_reducer_and_returns_new_state(self):
        store = Store(static_reducer)
        new_state = store.dispatch("unittest")
        self.assertEqual(new_state, pmap({"action": "unittest"}))

    def test_subscribes_accepts_callable_and_returns_store(self):
        store = Store(static_reducer)
        rt_store = store.subscribe(lambda y: y)
        self.assertEqual(store, rt_store)

    def test_dispatch_calls_subscriber_with_store(self):
        store = Store(static_reducer)
        self._subscriber_called = False
        action = "unittest"

        def subscriber(sub_store):
            self._subscriber_called = True
            self.assertEqual(store, sub_store)
            self.assertEqual(sub_store.state, pmap({"action": action}))

        store = store.subscribe(subscriber)
        store.dispatch(action)
        self.assertTrue(self._subscriber_called, "Subscriber was not called")

    def test_unsubscribe_with_no_subscription_throws_error(self):
        store = Store(static_reducer)
        self.assertRaises(
            NoSubscriptionFoundError,
            store.unsubscribe,
            lambda x: x
        )

    def test_unsubscribe_successfully_removes_subscription(self):
        store = Store(static_reducer)

        def subscriber(x): return x
        store.subscribe(subscriber)
        self.assertEqual(len(store._subscriber), 1)
        store.unsubscribe(subscriber)
        self.assertEqual(len(store._subscriber), 0)

    def test_replace_reducer(self):
        store = Store(static_reducer)
        store = store.replace_reducer(add_to_string_reducer)
        action = "unittest"
        new_state = store.dispatch(action)
        self.assertEqual(pmap({"action": "newunittest"}), new_state)

    def test_create_store_will_return_initialized_store(self):
        new_store = create_store(init_reducer)
        init_state = pmap({"init": True})
        self.assertEqual(init_state, new_store.state)

    def test_can_insert_a_preloaded_state_into_store(self):
        preloaded_state = freeze({
            "init": True
        })
        store = create_store(do_nothing_reducer, preloaded_state)
        self.assertEqual(
            store.state,
            preloaded_state
        )
