from __future__ import absolute_import, unicode_literals


class ActionBase(object):

    def __init__(self, action_type, payload=None):
        if action_type is None:
            raise NotImplementedError("Every Action needs a type!")
        self.__type = action_type
        self.__payload = payload

    @property
    def type(self):
        return self.__type

    @property
    def payload(self):
        return self.__payload