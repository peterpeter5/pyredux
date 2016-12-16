from __future__ import absolute_import, unicode_literals
import collections


def create_action_type(action_name):
    ActionType = collections.namedtuple(action_name, ("payload", "type"))
    ActionType.__new__.__defaults__ = (None, action_name)
    return ActionType
