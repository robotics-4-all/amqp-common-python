#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import amqp_common


def callback(msg, meta):
    channel = meta['channel']
    method = meta['method']
    props = meta['properties']
    print('[*] - Channel={}'.format(channel))
    print('[*] - Method={}'.format(method))
    print('[*] - Properties={}'.format(props))
    print('[*] - Data={}'.format(msg))

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
    try:
        sub = amqp_common.SubscriberSync(
            topic, callback=callback,
            creds=amqp_common.Credentials('invalid', 'invalid'))
    except Exception:
        sub = amqp_common.SubscriberSync(
            topic, callback=callback,
            creds=amqp_common.Credentials('guest', 'guest'))
    sub.run()
