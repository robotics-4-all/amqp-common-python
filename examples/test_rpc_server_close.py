#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time
import argparse

import amqp_common

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AMQP SharedConnection CLI.')
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
        '--debug',
        dest='debug',
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
    iterations = 10

    debug = True if args.debug else False

    data = {'a': 10, 'b': 20}

    conn_params = amqp_common.ConnectionParameters(
        host=host, port=port, vhost=vhost)

    conn_params.credentials = amqp_common.Credentials(username, password)
    conn = amqp_common.SharedConnection(conn_params)

    rpc_name = 'rpc-test'
    for i in range(iterations):
        rpc_server = amqp_common.RpcServer(
            rpc_name, connection=conn, debug=debug)
        rpc_server.run_threaded()
        time.sleep(1)
        rpc_server.close()
        del rpc_server
