from __future__ import absolute_import, unicode_literals
import collections


def create_action_type(action_name):
    ActionType = collections.namedtuple(action_name, ("payload", "type"))
    ActionType.__new__.__defaults__ = (None, action_name)
    return ActionType


def create_typed_action_creator(action_type):
    _ActionType = create_action_type(action_type)

    def _action_creator(payload=None, subtype=None):
        subtype = subtype if subtype is not None else action_type
        return _ActionType(payload, subtype)

    return _ActionType, _action_creator
