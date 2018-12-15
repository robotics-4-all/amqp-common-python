#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import argparse

import amqp_common


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AMQP Publisher CLI.')
    parser.add_argument('topic', action='store',
                        help='Topic to publish.')
    parser.add_argument('--hz', dest='hz',
                        help='Publishing frequency',
                        type=int,
                        default=2)
    parser.add_argument('--host', dest='host',
                        help='AMQP broker host (IP/Hostname)',
                        default='localhost')
    parser.add_argument('--port', dest='port',
                        help='AMQP broker listening port',
                        default='5672')
    parser.add_argument('--vhost', dest='vhost',
                        help='Virtual host to connect to.',
                        default='/klpanagi')
    parser.add_argument('--username', dest='username',
                        help='Authentication username',
                        default='bot')
    parser.add_argument('--password', dest='password',
                        help='Authentication password',
                        default='b0t')
    parser.add_argument('--debug', dest='debug',
                        help='Enable debugging',
                        type=bool,
                        const=True,
                        nargs='?')

    args = parser.parse_args()
    hz = args.hz
    host = args.host
    port = args.port
    vhost = args.vhost
    username = args.username
    password = args.password
    topic = args.topic
    debug = True if args.debug else False

    data = {
        'a': 10,
        'b': 20
    }

    pub = amqp_common.PublisherSync(
        topic, connection_params=amqp_common.ConnectionParameters(
            host=host, port=port, vhost=vhost),
        creds=amqp_common.Credentials(username, password),
        debug=debug
    )

    # Publish once
    pub.publish(data)
    # Bind data and publish with frequency
    pub.pub_loop(data, hz)
