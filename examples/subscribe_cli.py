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

import argparse
import time
import json

import amqp_common


def callback(msg, meta):
    try:
        channel = meta['channel']
        method = meta['method']
        props = meta['properties']
        print('[*] - Channel={}'.format(channel))
        print('[*] - Method={}'.format(method))
        print('[*] - Properties={}'.format(props))
        print('[*] - Data -->')
        print(json.dumps(msg, indent=4))

        timestamp_send = float(str(meta['properties']['timestamp_producer']))
        timestamp_broker = float(str(meta['properties']['timestamp_broker']))

        timestamp_now = 1.0 * (time.time() + 0.5) * 1000

        m2m_delay = 1.0 * (timestamp_now - timestamp_send)
        # m2c_delay = 1.0 * (int(timestamp_broker) - timestamp_send)

        # print('[*] - Network M2C Delay: {}'.format(m2c_delay))
        print('[*] - Network M2M Delay: {} ms'.format(m2m_delay))
    except Exception as e:
        print(e)


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
