from __future__ import absolute_import, unicode_literals
import unittest

from pyrsistent import freeze
from pyrsistent import pmap

from pyredux.Actions import create_action_type
from pyredux.Reducer import default_reducer, combine_reducer
from pyredux.Store import Store, create_store

StaticAction = create_action_type("Static")
NormalAction = create_action_type("normal")
DynamicAction = create_action_type("dynamic")


@default_reducer
def reducer_a(action, state=pmap({"static": True})):
    return state


@reducer_a.register(StaticAction)
def _(action, state):
    if action.type == "Static":
        return state.update({"static": 1})
    elif action.type == "AppendAction":
        return state.update({"action": (action.type, action.payload)})


@reducer_a.register(DynamicAction)
def _(action, state):
    return state.update({"dynamic": "dynamo"})


def normal_reducer(action, state=pmap({"my_type": "normal"})):
    if action.type == "normal":
        return state.update({"normal": True})
    else:
        return state


class FunctionalTests(unittest.TestCase):

    def test_combine_reducers_with_singledispatch(self):
        combined_reducer = combine_reducer((normal_reducer, reducer_a))
        static_action = StaticAction()
        expected_state = freeze({
            "normal_reducer": {"my_type": "normal"},
            "reducer_a": {"static": 1}
        })
        self.assertEqual(
            expected_state,
            combined_reducer(static_action)
        )

    def test_combined_reducer_can_match_by_subtype(self):
        combined_reducer = combine_reducer((normal_reducer, reducer_a))
        static_action = StaticAction(type="AppendAction", payload="900")
        expected_state = freeze({
            "normal_reducer": {"my_type": "normal"},
            "reducer_a": {
                "static": True,
                "action": ("AppendAction", "900")
                          }
        })
        self.assertEqual(
            expected_state,
            combined_reducer(static_action)
        )

    def test_combined_can_singledispatch_for_multiple_types(self):
        combined_reducer = combine_reducer((normal_reducer, reducer_a))
        dyn_action = DynamicAction()
        expected_state = freeze({
            "normal_reducer": {"my_type": "normal"},
            "reducer_a": {
                "static": True,
                "dynamic": "dynamo"
            }
        })
        self.assertEqual(expected_state, combined_reducer(dyn_action))

    def test_combined_will_fallback_to_default_by_unknown_action(self):
        combined_reducer = combine_reducer((normal_reducer, reducer_a))
        unknown_action = create_action_type("unknown")
        expected_state = freeze({
            "normal_reducer": {"my_type": "normal"},
            "reducer_a": {"static": True}
        })
        self.assertEqual(
            expected_state,
            combined_reducer(unknown_action)
        )

    def test_store_can_handle_combined_reducers_with_singledispatch(self):
        combined = combine_reducer([reducer_a, normal_reducer])
        expected_state = freeze({
            "normal_reducer": {"my_type": "normal"},
            "reducer_a": {"static": True}
        })
        store = create_store(combined)
        self.assertEqual(
            expected_state,
            store.state
        )

        dyn_action = DynamicAction()
        expected_state = freeze({
            "normal_reducer": {"my_type": "normal"},
            "reducer_a": {
                "static": True,
                "dynamic": "dynamo"
            }
        })
        actual_state = store.dispatch(dyn_action)
        self.assertEqual(
            expected_state,
            actual_state
        )
