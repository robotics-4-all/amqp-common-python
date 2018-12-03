#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import amqp_common


if __name__ == "__main__":
    rpc_name = sys.argv[1] if len(sys.argv) > 1 else 'rpc_mult'

    creds = amqp_common.Credentials(username='robot_1', password='r0b0t1')
    conn_params = amqp_common.ConnectionParameters(host='155.207.33.185',
                                                   port='5672')
    rpc_client = amqp_common.RpcClient(
        rpc_name, creds=creds, connection_params=conn_params)
    data = {
        'a': 4,
        'b': 13
    }

    resp = rpc_client.call(data)
    print(resp)
