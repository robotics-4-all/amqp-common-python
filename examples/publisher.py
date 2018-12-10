#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import amqp_common


if __name__ == '__main__':
    topic = sys.argv[1] if len(sys.argv) > 1 else 'robot_1.dummy'
    rate = float(sys.argv[2]) if len(sys.argv) > 2 else 2
    data = {
        'a': 10,
        'b': 20
    }

    pub = amqp_common.PublisherSync(
        topic, connection_params=amqp_common.ConnectionParameters(
            host='155.207.33.185', port='5672'),
        creds=amqp_common.Credentials('robot_1', 'r0b0t1'))

    # Publish once
    pub.publish(data)
    # Bind data and publish with frequency
    pub.pub_loop(data, rate)
