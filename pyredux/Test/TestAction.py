from __future__ import absolute_import, unicode_literals
import unittest

from pyredux import Actions


class TestActionCreator(unittest.TestCase):

    def test_create_new_action_with_default_args(self):
        Action = Actions.create_action_type("Action42")
        new_action = Action("just unittest")
        self.assertEqual(new_action.type, "Action42")
        self.assertEqual(new_action.payload, "just unittest")
        self.assertIsInstance(new_action, Action)

    def test_create_new_action_with_empty_payload(self):
        action_type = "A_hell_of_an_action"
        MyAction = Actions.create_action_type(action_type)
        new_action = MyAction()
        self.assertEqual(new_action.type, action_type)
        self.assertEqual(new_action.payload, None)
        self.assertIsInstance(new_action, MyAction)

    def test_create_actions_of_different_subtypes_from_same_base(self):
        default_action_type = "ActionBase"
        ActionBase = Actions.create_action_type(default_action_type)
        action_a = ActionBase("payload", "A_Action")
        action_b = ActionBase(type="B_Action", payload="b_payload")
        self.assertIsInstance(action_b, ActionBase)
        self.assertEqual(action_b.type, "B_Action")
        self.assertEqual(action_b.payload, "b_payload")

        self.assertIsInstance(action_a, ActionBase)
        self.assertEqual(action_a.type, "A_Action")
        self.assertEqual(action_a.payload, "payload")