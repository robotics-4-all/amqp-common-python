#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from threading import Thread, Semaphore
from collections import deque
import json
import time

from .amqp_transport import (AMQPTransportSync, Credentials, ExchangeTypes,
                             MessageProperties)
from .rate import Rate


class PublisherSync(AMQPTransportSync):
    def __init__(self, topic, exchange='amq.topic', *args, **kwargs):
        """
        Constructor.

        @param topic: Topic name to publish
        @type topic: string

        """
        self._topic_exchange = exchange
        self._topic = topic
        self._name = topic
        AMQPTransportSync.__init__(self, *args, **kwargs)
        self.connect()
        self.create_exchange(self._topic_exchange, ExchangeTypes.Topic)

    def publish(self, msg):
        """
        Publish message once.
        TODO: 1) Add message publishing timestamp
              2) Add Content-Type (handled at the application layer)
              3) Add Content-Encoding (handled at the application layer)

        @param msg: Message to publish.
        @type msg: dict

        """
        content_type = None
        if isinstance(msg, dict):
            content_type = 'application/json'
            content_encoding = 'utf8'
        elif isinstance(msg, str):
            content_type = 'text/plain'
            content_encoding = 'utf8'
        #  elif isinstance(msg, unicode):
        #  content_type = 'text/plain'

        msg_props = MessageProperties(
            content_type=content_type,
            content_encoding=content_encoding,
            timestamp=int(time.time()))

        self.logger.debug('[x] - Sent %r:%r' % (self._topic, msg))
        self._channel.basic_publish(
            exchange=self._topic_exchange,
            routing_key=self._topic,
            properties=msg_props,
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


class SubscriberSync(AMQPTransportSync):
    """Subscriber implementation in AMQP protocol."""

    FREQ_CALC_SAMPLES_MAX = 100

    def __init__(self,
                 topic,
                 on_message=None,
                 exchange='amq.topic',
                 queue_size=10,
                 message_ttl=60000,
                 overflow='drop-head',
                 *args,
                 **kwargs):
        """
        Constructor.

        @param topic: The name of the (virtual) Topic.
        @type: string

        @param on_message: Function to execute when on-message event fires.
        @type on_message: function

        @param connection_params: AMQP Connection Parameters
        @type connection_params: ConnectionParameters
        """
        self._name = topic
        AMQPTransportSync.__init__(self, *args, **kwargs)
        self._topic = topic
        self._topic_exchange = exchange
        self._queue_name = None
        self._queue_size = queue_size
        self._message_ttl = message_ttl
        self._overflow = overflow
        self.connect()
        if on_message is not None:
            self.onmessage = on_message
        self.create_exchange(self._topic_exchange, ExchangeTypes.Topic)
        # Create a queue
        self._queue_name = self.create_queue(
            queue_size=self._queue_size,
            message_ttl=self._message_ttl,
            overflow_behaviour=self._overflow)
        # Bind queue to the Topic exchange
        self.bind_queue(self._topic_exchange, self._queue_name, self._topic)
        self._last_msg_ts = None
        self._msg_freq_fifo = deque(maxlen=self.FREQ_CALC_SAMPLES_MAX)
        self._hz = 0
        self._sem = Semaphore()

    @property
    def hz(self):
        """Incoming mesasge frequency."""
        return self._hz

    def run(self):
        """Start Subscriber."""
        self._consume()

    def run_threaded(self):
        """Execute subscriber in a separate thread."""
        self.loop_thread = Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def _consume(self):
        """Start AMQP consumer (aka Subscriber)."""
        self._channel.basic_consume(
            self._on_msg_callback_wrapper, queue=self._queue_name, no_ack=True)
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt as exc:
            # Log error with traceback
            self.logger.error(exc, exc_info=True)

    def _on_msg_callback_wrapper(self, ch, method, properties, body):
        #  ts_send = properties.headers['timestamp_in_ms']
        #  ts_send = properties.timestamp
        #  msg_trans_delay = ts - ts_send
        #  print(msg_trans_delay)
        msg = self._deserialize_data(body)

        self._sem.acquire()
        self._calc_msg_frequency()
        self._sem.release()

        if self.onmessage is not None:
            meta = {'channel': ch, 'method': method, 'properties': properties}
            self.onmessage(msg, meta)

    def _calc_msg_frequency(self):
        ts = time.time()
        if self._last_msg_ts is not None:
            diff = ts - self._last_msg_ts
            if diff < 10e-3:
                self._last_msg_ts = ts
                return
            else:
                hz = 1.0 / float(diff)
                self._msg_freq_fifo.appendleft(hz)
                hz_list = [s for s in self._msg_freq_fifo if s != 0]
                _sum = sum(hz_list)
                self._hz = _sum / len(hz_list)
        self._last_msg_ts = ts

    def _deserialize_data(self, data):
        """
        Deserialize data.

        TODO: Make class. ALlow for different implementations.

        @param data: Data to deserialize.
        @type data: dict|int|bool
        """
        return json.loads(data)
