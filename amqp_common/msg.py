# -*- coding: utf-8 -*-
# Copyright (C) 2020  Panayiotou, Konstantinos <klpanagi@gmail.com>
# Author: Panayiotou, Konstantinos <klpanagi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

import time
from os import path
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
                raise AttributeError(
                        '{}{}{}'.join(
                            self.__class__.__name__,
                            ' object does not have a property named ',
                            str(key))
                        )

    def _to_dict(self):
        """Serialize message object to a dict."""
        _d = {}
        for k in self.__slots__:
            # Recursive object seriazilation to dictionary
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
        """Serialize Message to json string.

        Returns:
            [str]: String List.
        """
        _d = self._to_dict()
        return json.dumps(_d)

    def serialize_bytes(self):
        """Serialize Message to bytes.

        Returns:
            [byte]: Byte List.
        """
        return json.dumps(self._to_dict()).encode('utf-8')

    def to_dict(self):
        """Serialize Message to dictionary."""
        return self._to_dict()

    def _deserialize_from_json_string(self, data_str):
        try:
            return json.loads(data_str)
        except Exception:
            print('Could not deserialize json string data!!')

    def __eq__(self, other):
        """! Equality method """
        return self.serialize() == other.serialize()


class HeaderMessage(Message):
    """Implementation of the Header Message object."""

    __slots__ = ['seq', 'timestamp', 'sender_id']

    counter = 0

    def __init__(self, seq=None, timestamp=None, sender_id=''):
        """Constructor."""
        HeaderMessage.counter = HeaderMessage.counter + 1 if seq is None else seq
        self.seq = HeaderMessage.counter
        self.timestamp = int(time.time()) if timestamp is None else timestamp
        self.sender_id = sender_id


class FileMessage(Message):
    """Implementation of the File Message object."""

    __slots__ = ['filename', 'header', 'data']

    def __init__(self, filename='', data=[]):
        """Constructor."""
        self.filename = filename
        self.data = data
        self.header = HeaderMessage()

    def load_from_file(self, filepath):
        """Load raw bytes from file.

        Args:
            filepath (str): System Path of the file.
        """
        with open(filepath, 'rb') as f:
            fdata = f.read()
            b64 = base64.b64encode(fdata)
            self.data = b64.decode()
            self.filename = path.basename(filepath)
