#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import amqp_common


if __name__ == "__main__":
    rpc_name = sys.argv[1] if len(sys.argv) > 1 else 'rpc_mult'
    rpc_client = amqp_common.RpcClient(rpc_name)
    data = {
        'a': 4,
        'b': 13
    }
    resp = rpc_client.call(data)
    print(resp)
