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


from __future__ import (
    division,
    print_function,
    unicode_literals
)

import sys
import argparse
import json

import amqp_common


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AMQP Publisher CLI.')
    parser.add_argument('topic', action='store', help='Topic to publish.')
    parser.add_argument(
        '--hz', dest='hz', help='Publishing frequency', type=int, default=2)
    parser.add_argument(
        '--host',
        dest='host',
        help='AMQP broker host (IP/Hostname)',
        default='localhost')
    parser.add_argument(
        '--port',
        dest='port',
        help='AMQP broker listening port',
        default='5672')
    parser.add_argument(
        '--vhost',
        dest='vhost',
        help='Virtual host to connect to.',
        default='/klpanagi')
    parser.add_argument(
        '--username',
        dest='username',
        help='Authentication username',
        default='bot')
    parser.add_argument(
        '--password',
        dest='password',
        help='Authentication password',
        default='b0t')
    parser.add_argument(
        '--data',
        dest='data',
        help='Data to send in json format',
        default='{\"data\": \"TEST\"}')
    parser.add_argument(
        '--debug',
        dest='debug',
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
    data = args.data
    data = json.loads(data)

    pub = amqp_common.PublisherSync(
        topic,
        connection_params=amqp_common.ConnectionParameters(
            host=host, port=port, vhost=vhost),
        creds=amqp_common.Credentials(username, password),
        debug=debug)

    rate = amqp_common.Rate(hz)
    while True:
        # Publish once
        pub.publish(data)
        rate.sleep()
