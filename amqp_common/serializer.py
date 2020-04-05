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

import json


class ContentType(object):
    json = 'application/json'
    raw_bytes = 'application/octet-stream'
    text = 'plain/text'


class Serializer(object):
    CONTENT_TYPE = 'None'
    CONTENT_ENCODING = 'None'

    @staticmethod
    def serialize(self, msg):
        raise NotImplementedError()

    @staticmethod
    def deserialize(self, data):
        raise NotImplementedError()


# class ByteSerializer(Serializer):
#     CONTENT_TYPE = 'application/octet-stream'
#     CONTENT_ENCODING = 'utf8'


class JSONSerializer(Serializer):
    CONTENT_TYPE = 'application/json'
    CONTENT_ENCODING = 'utf8'

    @staticmethod
    def serialize(_dict):
        if not isinstance(_dict, dict):
            raise TypeError('Data are not in dict structure.')
        return json.dumps(_dict)

    @staticmethod
    def deserialize(data):
        return json.loads(data)
