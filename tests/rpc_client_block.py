#!/usr/bin/env python3

import time

from amqp_common import ConnectionParameters, RpcClient, Credentials


if __name__ == "__main__":

    conn_params = ConnectionParameters(
        host='r4a-platform.ddns.net',
        # port=port,
        # vhost=vhost
    )
    conn_params.credentials = Credentials('bot', 'bot')

    rpc_client = RpcClient('test_rpc_client_blocked',
                           connection_params=conn_params)
    data = {}
    while True:
        print('Calling RPC')
        resp = rpc_client.call(data, timeout=30)
        print('Response: {}'.format(resp))
        time.sleep(2)
        rpc_client.process_amqp_events()
