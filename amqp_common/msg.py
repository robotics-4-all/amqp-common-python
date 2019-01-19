# -*- coding: utf-8 -*-

import time


class Message(object):
    """Abstract Message Class."""

    __slots__ = []

    def __init__(self):
        """Constructor."""
        pass

    def _to_dict(self):
        """Serialize message object to a dict."""
        return {
            k: getattr(self, k)
            for k in self.__slots__ if not k.startswith('_')
        }

    def _from_dict(self, data_dict):
        """Fill message data fields from dict key-value pairs."""
        for key, val in data_dict.items():
            setattr(self, key, val)


class HeaderMsg(Message):
    """Header message class."""

    __slots__ = ['seq', 'timestamp' 'sender_id']

    counter = 0

    def __init__(self, seq=None, timestamp=None):
        """Constructor."""
        HeaderMsg.counter = HeaderMsg.counter + 1 if seq is None else seq
        self.seq = HeaderMsg.counter
        self.timestamp = int(time.time()) if timestamp is None else timestamp
        self.sender_id = 'not-specified'
