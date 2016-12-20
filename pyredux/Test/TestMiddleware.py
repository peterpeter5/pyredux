from __future__ import absolute_import, unicode_literals
import unittest

from pyrsistent import pmap
from pyrsistent import pvector

from pyredux.Actions import create_action_type
from pyredux.Middleware import apply_middleware, middleware
from pyredux.Store import create_store

call_chain = []


def middleware_a(store):
    def _next_wrapper(next_middleware):
        def _middleware(action):
            call_chain.append("a")
            return next_middleware(action)
        return _middleware
    return _next_wrapper


def middleware_b(store):
    def _nextwrapper(next_middleware):
        def middleware(action):
            call_chain.append("b")
            return next_middleware(action)
        return middleware
    return _nextwrapper


def middleware_dispatching_extra(store):
    def _nextwrapper(next_middleware):
        def middleware(action):
            if isinstance(action, DefaultAction):
                store.dispatch(MiddleWareAction())
            call_chain.append("c")
            return next_middleware(action)
        return middleware
    return _nextwrapper


@middleware
def middleware_decorated(store, next_middleware, action):
    call_chain.append("d")
    assert store.state is not None
    return next_middleware(action)


def default_action_logger(action, state=pmap({"actions": pvector()})):
    if isinstance(action, (DefaultAction, MiddleWareAction)):
        actions = state.get("actions")
        actions = actions.append(action)
        return state.update({"actions": actions})
    else:
        return state

DefaultAction = create_action_type("Unittest")
MiddleWareAction = create_action_type("MiddleWareAction")


class TestMiddleware(unittest.TestCase):

    def setUp(self):
        global call_chain
        call_chain = []
        self.call_chain = call_chain

    def test_dispatch_calls_middleware(self):
        store = create_store(default_action_logger, enhancer=apply_middleware(middleware_b, middleware_a))
        store.dispatch(DefaultAction())
        self.assertEqual(call_chain, ["b", "a"])

    def test_dispatch_from_middleware_does_call_whole_chain_again(self):
        store = create_store(
            default_action_logger,
            enhancer=apply_middleware(middleware_dispatching_extra, middleware_a)
        )
        store.dispatch(DefaultAction())
        actions = store.state["actions"]
        self.assertEqual(call_chain, ["c", "a", "c", "a"])
        self.assertEqual(len(actions), 2)
        self.assertIsInstance(actions[0], MiddleWareAction)
        self.assertIsInstance(actions[1], DefaultAction)

    def test_decorator_for_creating_middleware_func(self):
        store = create_store(default_action_logger, enhancer=apply_middleware(middleware_decorated))
        store.dispatch(DefaultAction())
        self.assertEqual(call_chain, ["d"])
        actions = store.state["actions"]
        self.assertEqual(len(actions), 1)
        self.assertIsInstance(actions[0], DefaultAction)

    def test_combined_middleware_from_decorator_and_functional_declaration_style(self):
        store = create_store(
            default_action_logger, enhancer=apply_middleware(
                middleware_dispatching_extra,
                middleware_decorated,

            )
        )
        store.dispatch(DefaultAction())
        self.assertEqual(call_chain, ["c", "d", "c", "d"])

