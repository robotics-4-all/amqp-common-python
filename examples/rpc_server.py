#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import amqp_common


def callback(msg, meta):
    print(msg)
    a = msg['a']
    b = msg['b']
    c = a * b
    return c


if __name__ == "__main__":
    rpc_name = sys.argv[1] if len(sys.argv) > 1 else 'rpc.mult'
    creds = amqp_common.Credentials(username='robot_1', password='r0b0t1')
    conn_params = amqp_common.ConnectionParameters(host='155.207.33.185',
                                                   port='5672')
    rpc_server = amqp_common.RpcServer(
        rpc_name, on_request=callback,
        connection_params=conn_params,
        creds=creds)
    rpc_server.run()
