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
        '--heartbeat',
        dest='heartbeat',
        help='Heartbeat timeout value',
        type=int,
        default=60)
    parser.add_argument(
        '--socket-timeout',
        dest='socket_timeout',
        help='Socket timeout value',
        type=float,
        default=120)
    parser.add_argument(
        '--blocked-connection-timeout',
        dest='blocked_connection_timeout',
        help='BlockedConnection timeout value',
        type=float,
        default=120)
    parser.add_argument(
        '--sleep',
        dest='sleep',
        help='Sleep for time',
        type=float,
        default=120)
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
    hz = 1
    host = args.host
    port = args.port
    vhost = args.vhost
    username = args.username
    password = args.password
    heartbeat = args.heartbeat
    socket_timeout = args.socket_timeout
    blocked_connection_timeout = args.blocked_connection_timeout
    sleep_time = args.sleep

    debug = True if args.debug else False

    data = {'a': 10, 'b': 20}

    conn_params = amqp_common.ConnectionParameters(
        host=host,
        port=port,
        vhost=vhost,
        timeout=socket_timeout,
        heartbeat_timeout=heartbeat,
        blocked_connection_timeout=blocked_connection_timeout)

    conn_params.credentials = amqp_common.Credentials(username, password)
    conn = amqp_common.SharedConnection(conn_params)

    pubs = []
    rpc_servers = []
    rpc_clients = []
    for i in range(20):
        pub = amqp_common.PublisherSync('test', connection=conn, debug=debug)
        rpc_name = 'rpc-' + str(long(time.time() * 1000))
        rpc_server = amqp_common.RpcServer(
            rpc_name, connection_params=conn_params, debug=debug)
        rpc_server.run_threaded()
        rpc_client = amqp_common.RpcClient(
            rpc_name, connection=conn, debug=debug)

        pubs.append(pub)
        rpc_servers.append(rpc_server)
        rpc_clients.append(rpc_client)

    rate = amqp_common.Rate((1.0 / sleep_time))
    while True:
        for p in pubs:
            p.publish(data)
        for c in rpc_clients:
            resp = c.call(data)
            print('RESPONSE: {}'.format(resp))
        rate.sleep()
