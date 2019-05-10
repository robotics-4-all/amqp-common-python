#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json


class MessageSerializer(object):
    def __init__(self):
        pass

    def serialize(self, msg):
        raise NotImplementedError()

    def deserialize(self, data):
        raise NotImplementedError()


class JSONSerializer(object):
    def __init__(self):
        pass

    def serialize(self, msg):
        return json.dumps(msg._to_dict())

    def deserialize(self, data, msg_cls):
        msg = msg_cls()
        if isinstance(data, dict):
            msg._from_dict(data)
        else:
            raise TypeError('data must be of type dict')
        return msg
