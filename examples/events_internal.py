#!/usr/bin/env python3

import amqp_common
from pprint import pprint
import time


def callback(msg, meta):
    pprint(msg)
    # pprint(meta)
    pprint(meta['properties'].headers)


def main(rkey='connection.created', host='155.207.33.189', port='5672',
         vhost='/', username='bot', password='b0t', debug=True):
    sub = amqp_common.SubscriberSync(
        rkey, on_message=callback,
        exchange='amq.rabbitmq.event',
        connection_params=amqp_common.ConnectionParameters(
            host=host, port=port, vhost=vhost),
        creds=amqp_common.Credentials(username, password),
        debug=debug
    )
    sub.run_threaded()
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
