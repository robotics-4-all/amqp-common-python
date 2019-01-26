#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import time
import json

import amqp_common


def callback(msg, meta):
    channel = meta['channel']
    method = meta['method']
    props = meta['properties']
    print('[*] - Channel={}'.format(channel))
    print('[*] - Method={}'.format(method))
    print('[*] - Properties={}'.format(props))
    print('[*] - Data -->')
    print(json.dumps(msg, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AMQP Publisher CLI.')
    parser.add_argument('topic', action='store',
                        help='Topic to publish.')
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
    parser.add_argument('--queue-size', dest='queue_size',
                        help='Maximum queue size.',
                        type=int,
                        default=10)
    parser.add_argument('--debug', dest='debug',
                        help='Enable debugging',
                        type=bool,
                        const=True,
                        nargs='?')

    args = parser.parse_args()
    host = args.host
    port = args.port
    vhost = args.vhost
    username = args.username
    password = args.password
    topic = args.topic
    queue_size = args.queue_size
    debug = True if args.debug else False

    sub = amqp_common.SubscriberSync(
        topic, on_message=callback,
        connection_params=amqp_common.ConnectionParameters(
            host=host, port=port, vhost=vhost),
        queue_size=queue_size,
        creds=amqp_common.Credentials(username, password),
        debug=debug
    )
    sub.run_threaded()
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
