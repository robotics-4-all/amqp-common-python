#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import time
import argparse

import amqp_common

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AMQP SharedConnection CLI.')
    parser.add_argument(
        '--hz',
        dest='hz',
        help='Publishing frequency',
        type=float,
        default=1.0)
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
        '--channels',
        dest='num_channels',
        help='Number of channels to open.',
        default=9)
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
    topic = 'test'
    debug = True if args.debug else False
    num_channels = args.num_channels

    data = {'a': 10, 'b': 20}

    conn_params = amqp_common.ConnectionParameters(
        host=host, port=port, vhost=vhost)
    conn_params.credentials = amqp_common.Credentials(username, password)
    conn = amqp_common.SharedConnection(conn_params)

    pubs = []
    rpc_servers = []
    rpc_clients = []
    for i in range(int(num_channels / 3)):
        pub = amqp_common.PublisherSync(topic, connection=conn, debug=debug)
        rpc_name = 'rpc-' + str(long(time.time() * 1000))
        rpc_server = amqp_common.RpcServer(
            rpc_name, connection_params=conn_params, debug=debug)
        rpc_server.run_threaded()
        rpc_client = amqp_common.RpcClient(
            rpc_name, connection=conn, debug=debug)

        pubs.append(pub)
        rpc_servers.append(rpc_server)
        rpc_clients.append(rpc_client)

    rate = amqp_common.Rate(int(hz))
    while True:
        for p in pubs:
            p.publish(data)
        for c in rpc_clients:
            resp = c.call(data)
            print('RESPONSE: {}'.format(resp))
        rate.sleep()
