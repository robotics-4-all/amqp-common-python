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
