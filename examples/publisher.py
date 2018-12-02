#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import amqp_common


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
    rate = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    data = {
        'a': 10,
        'b': 20
    }

    try:
        pub = amqp_common.PublisherSync(
            topic, creds=amqp_common.Credentials('invalid', 'invalid'))
    except Exception:
        pub = amqp_common.PublisherSync(
            topic, creds=amqp_common.Credentials('guest', 'guest'))

    pub.pub_loop(data, rate)
