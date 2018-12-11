#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
