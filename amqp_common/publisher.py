#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from .broker_interface import BrokerInterfaceSync, Credentials, ExchangeTypes
from .rate import Rate


class PublisherSync(BrokerInterfaceSync):

    def __init__(self, topic, *args, **kwargs):
        """
        Constructor.

        @param topic: Topic name to publish
        @type topic: string

        """
        BrokerInterfaceSync.__init__(self, *args, **kwargs)
        self.connect()
        self.setup_exchange(self._topic_exchange, ExchangeTypes.Topic)
        self._topic = topic

    def publish(self, msg):
        self.logger.debug("[x] - Sent %r:%r" % (self._topic, msg))
        self._channel.basic_publish(exchange=self._topic_exchange,
                                    routing_key=self._topic,
                                    body=self._serialize_data(msg))

    def pub_loop(self, data_bind, hz):
        self._rate = Rate(hz)
        while True:
            try:
                self.publish(data_bind)
                self._rate.sleep()
            except KeyboardInterrupt as exc:
                print(exc)
                break

    def _serialize_data(self, data):
        """
        TODO: Make Class. Allow different implementation of serialization
            classes.
        """
        return json.dumps(data)


if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
    rate = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    message = ' '.join(sys.argv[3:]) or 'Hello World!'

    try:
        pub = PublisherSync(topic, creds=Credentials('invalid', 'invalid'))
    except Exception:
        pub = PublisherSync(topic, creds=Credentials('guest', 'guest'))

    pub.pub_loop(message, rate)
