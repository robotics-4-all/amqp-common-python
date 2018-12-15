#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from .broker_interface import BrokerInterfaceSync, Credentials, ExchangeTypes
from .rate import Rate


class PublisherSync(BrokerInterfaceSync):

    def __init__(self, topic, exchange='amq.topic', *args, **kwargs):
        """
        Constructor.

        @param topic: Topic name to publish
        @type topic: string

        """
        self._topic_exchange = exchange
        self._topic = topic
        self._name = topic
        BrokerInterfaceSync.__init__(self, *args, **kwargs)
        self.connect()
        self.setup_exchange(self._topic_exchange, ExchangeTypes.Topic)

    def publish(self, msg):
        """
        Publish message once.

        @param msg: Message to publish.
        @type msg: dict

        """
        self.logger.debug('[x] - Sent %r:%r' % (self._topic, msg))
        self._channel.basic_publish(exchange=self._topic_exchange,
                                    routing_key=self._topic,
                                    body=self._serialize_data(msg))

    def pub_loop(self, data_bind, hz):
        """
        Publish message frequenntly.

        @param data_bind: Bind to data for publishing.
        @type data_bind: dict

        @param hz: Publishing frequency.
        @type hz: float

        """
        if hz == 0.0:  # Publish once and return
            self.publish(data_bind)
            return
        elif hz < 0:
            self.logger.exception('Frequency must be in range [0+, inf]')
            raise ValueError('Frequency must be in range [0, inf]')
        self._rate = Rate(hz)
        while True:
            try:
                self.publish(data_bind)
                self._rate.sleep()
            except KeyboardInterrupt:
                self.logger.exception('Process received keyboard interrupt')
                break

    def _serialize_data(self, data):
        """
        TODO: Make Class. Allow different implementation of serialization
            classes.
        """
        return json.dumps(data)
