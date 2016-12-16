from __future__ import absolute_import, unicode_literals

from pyredux.Actions import create_action_type


class NoSubscriptionFoundError(Exception):
    pass


class WrongFormattedReducerArgs(Exception):
    pass


initial_action_type = "INTERNAL_INIT_REDUX_STORE"
StoreInitAction = create_action_type(initial_action_type)
