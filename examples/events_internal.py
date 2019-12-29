#!/usr/bin/env python3

import amqp_common
from pprint import pprint
import time
import json


def callback_1(msg, meta):
    print('[*] - Received CONNECTION CREATED EVENT!')
    print(meta['properties'].headers['host'])
    pprint(meta['properties'].headers)

def callback_2(msg, meta):
    print('[*] - Received CHANNEL CREATED EVENT!')
    print(meta['properties'].headers)
    pprint(meta['properties'].headers)

def main(rkey='connection.created',
         host='155.207.33.189',
         port='5672',
         vhost='/',
         username='bot',
         password='b0t',
         debug=True
         ):
    con_params = amqp_common.ConnectionParameters(host=host,
                                                  port=port,
                                                  vhost=vhost
                                                  )
    creds = amqp_common.Credentials(username, password)
    con_params.credentials = creds
    el = amqp_common.InternalEventListener(con_params, debug=debug)
    el.listen(amqp_common.InternalEventType.Connection.CREATED, callback_1)
    el.listen(amqp_common.InternalEventType.Channel.CREATED, callback_2)
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
