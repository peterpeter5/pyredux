from __future__ import absolute_import, unicode_literals

from pyredux.Actions import ActionBase


class NoSubscriptionFoundError(Exception):
    def __init__(self, *args, **kwargs):
        super(NoSubscriptionFoundError, self).__init__(*args, **kwargs)


class StoreInitAction(ActionBase):
    action_type = "@@INTERNAL_INIT_REDUX_STORE!!DONT_MATCH_ME!@"

    def __init__(self):
        super(StoreInitAction, self).__init__(self.action_type)