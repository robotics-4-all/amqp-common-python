#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time

import amqp_common


def callback(msg, meta):
    channel = meta['channel']
    method = meta['method']
    props = meta['properties']
    #  print('[*] - Channel={}'.format(channel))
    #  print('[*] - Method={}'.format(method))
    print('[*] - Properties={}'.format(props))
    #  print('[*] - Data={}'.format(msg))


if __name__ == '__main__':
    topic = sys.argv[1] if len(sys.argv) > 1 else 'dummy'
    sub = amqp_common.SubscriberSync(
        topic, on_message=callback,
        connection_params=amqp_common.ConnectionParameters(
            host='155.207.33.185', port='5672'), vhost='/poutses',
        creds=amqp_common.Credentials('bot', 'b0t'))
    sub.run_threaded()
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
