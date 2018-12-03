#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
from threading import Thread

from .broker_interface import BrokerInterfaceSync, Credentials, ExchangeTypes


class SubscriberSync(BrokerInterfaceSync):

    def __init__(self, topic, *args, **kwargs):
        """
        TODO!!
        """
        BrokerInterfaceSync.__init__(self, *args, **kwargs)
        self._topic = topic
        self._queue_name = None
        self.connect()
        self.on_msg_callback = kwargs.pop('callback')
        self.setup_exchange(self._topic_exchange, ExchangeTypes.Topic)
        # Create a queue
        self._queue_name = self.create_queue()
        # Bind queue to the Topic exchange
        self.bind_queue(self._topic_exchange, self._queue_name,
                        self._topic)

    def run(self, callback=None):
        """
        TODO!!
        """
        if callback is not None:
            self._callback = callback
        # Start loop
        self._consume()

    def run_threaded(self):
        self.loop_thread = Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def _consume(self):
        """
        TODO!!
        """
        self._channel.basic_consume(self._on_msg_callback_wrapper,
                                    queue=self._queue_name,
                                    no_ack=True)
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt as exc:
            print(exc)

    def _on_msg_callback_wrapper(self, ch, method, properties, body):
        msg = self._deserialize_data(body)
        self.logger.debug("[x] Received data - %r:%r" % (method.routing_key, msg))
        if self.on_msg_callback is not None:
            meta = {
                'channel': ch,
                'method': method,
                'properties': properties
            }
            self.on_msg_callback(msg, meta)

    def _deserialize_data(self, data):
        """
        DeSerialize data.
        TODO: Make class. ALlow for different implementations.

        @param data: Data to deserialize.
        @type data: dict|int|bool
        """
        return json.loads(data)



if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
    try:
        sub = SubscriberSync(topic, creds=Credentials('invalid', 'invalid'))
    except Exception:
        sub = SubscriberSync(topic, creds=Credentials('guest', 'guest'))
    sub.run()
