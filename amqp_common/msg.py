# -*- coding: utf-8 -*-

import time
import json
import base64


class Message(object):
    """Abstract Message Class."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        for key, value in kwargs.iteritems():
            if hasattr(self.req, key):
                setattr(self.req, key, value)
            else:
                raise AttributeError(''.join(self.__class__.__name__ +
                    ' object does not have a property named ' + str(key)))

    def _to_dict(self):
        """Serialize message object to a dict."""
        _d = {}
        for k in self.__slots__:
            if not k.startswith('_'):
                _prop = getattr(self, k)
                if isinstance(_prop, Message):
                    _d[k] = _prop._to_dict()
                else:
                    _d[k] = _prop
        return _d

    def _from_dict(self, data_dict):
        """Fill message data fields from dict key-value pairs."""
        for key, val in data_dict.items():
            setattr(self, key, val)

    def serialize_json(self):
        return json.dumps(self._to_dict())

    def serialize(self):
        return self._to_dict()

    def __eq__(self, other):
        """! Equality method """
        return self.serialize() == other.serialize()


class HeaderMessage(Message):
    """Header message class."""

    __slots__ = ['seq', 'timestamp', 'sender_id']

    counter = 0

    def __init__(self, seq=None, timestamp=None, sender_id=''):
        """Constructor."""
        HeaderMessage.counter = HeaderMessage.counter + 1 if seq is None else seq
        self.seq = HeaderMessage.counter
        self.timestamp = int(time.time()) if timestamp is None else timestamp
        self.sender_id = sender_id


class FileMessage(Message):

    __slots__ = ['filename', 'header', 'data']

    def __init__(self, filename='', data=[]):
        self.filename = filename
        self.data = data
        self.header = HeaderMessage()

    def load_from_file(self, filepath):
        with open(filepath, 'rb') as f:
            fdata = f.read()
            b64 = base64.b64encode(fdata)
            self.data = b64
