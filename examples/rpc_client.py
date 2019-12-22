#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import argparse
import json

import amqp_common

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AMQP RPC Client CLI.')
    parser.add_argument('rpc', action='store', help='RPC name to call.')

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
        '--timeout',
        dest='timeout',
        help='Response Timeout value',
        default=20)
    parser.add_argument(
        '--msg',
        dest='msg',
        help='Message to send',
        default='{}')
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
    rpc_name = args.rpc
    timeout = args.timeout
    hz = args.hz
    msg = args.msg
    debug = True if args.debug else False

    conn_params = amqp_common.ConnectionParameters(
        host=host, port=port, vhost=vhost)
    conn_params.credentials = amqp_common.Credentials(username, password)
    conn = amqp_common.SharedConnection(conn_params)

    rpc_client = amqp_common.RpcClient(rpc_name, connection=conn)

    msg = json.loads(msg)

    rpc_client.debug = True
    if hz == 0:
        resp = rpc_client.call(msg, timeout=timeout)
        print(resp)
        sys.exit(0)

    rate = amqp_common.Rate(hz)
    while True:
        resp = rpc_client.call(msg, timeout=timeout)
        print(resp)
        print("----------> Call execution time: {}".format(rpc_client.delay))
        rate.sleep()
