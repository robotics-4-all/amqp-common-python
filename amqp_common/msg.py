# -*- coding: utf-8 -*-

import time


class AbstractMessage(object):

    __slots__ = []

    def __init__(self):
        pass

    def serialize(self):
        return {k: getattr(self, k) for k in self.__slots__ if
                not k.startswith('_')}


class HeaderMsg(AbstractMessage):

    __slots__ = [
        'seq',
        'timestamp'
    ]

    counter = 0

    def __init__(self, seq=None, timestamp=None):
        HeaderMsg.counter = HeaderMsg.counter + 1 if seq is None else seq
        self.seq = HeaderMsg.counter
        self.timestamp = int(time.time()) if timestamp is None else timestamp
