#!/usr/bin/env python3

import time

from amqp_common import ConnectionParameters, PublisherSync, Credentials


if __name__ == "__main__":

    heartbeat_timeout = 60

    conn_params = ConnectionParameters(
        host='r4a-platform.ddns.net',
        # port=port,
        # vhost=vhost
    )
    conn_params.credentials = Credentials('bot', 'bot')

    pub = PublisherSync('test_rpc_client_blocked',
                               connection_params=conn_params)
    data = {}
    while True:
        print('Publishing data')
        pub.publish(data)
        time.sleep(heartbeat_timeout - 5)
        pub.process_amqp_events()
        time.sleep(heartbeat_timeout - 5)

