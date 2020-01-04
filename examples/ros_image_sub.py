#!/usr/bin/env python
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


from __future__ import print_function

import sys
import time

import amqp_common
from PIL import Image
import io


def callback(msg, meta):
    channel = meta['channel']
    method = meta['method']
    props = meta['properties']
    width = int(msg['width'])
    height = int(msg['height'])
    # Extract and devode image data
    img_data = msg['data'].decode('base64')
    #  img = Image.frombytes('RGB', (width, height), img_data, 'raw')
    #  try:
        #  img.save('test.png')
    #  except:
        #  img.save(test.png)
        #  sys.exit(1)


if __name__ == '__main__':
    topic = sys.argv[1] if len(sys.argv) > 1 else 'robot_1.sensors.vision.camera.rgb.front'
    sub = amqp_common.SubscriberSync(
        topic, on_message=callback,
        connection_params=amqp_common.ConnectionParameters(
            host='155.207.33.185', port='5672'),
        creds=amqp_common.Credentials('bot', 'b0t'))
    sub.run_threaded()
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
