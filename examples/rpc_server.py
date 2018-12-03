#!/usr/bin/env python
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
    rpc_name = sys.argv[1] if len(sys.argv) > 1 else 'rpc_mult'
    rpc_server = amqp_common.RpcServer(rpc_name, on_request=callback)
    rpc_server.run()
