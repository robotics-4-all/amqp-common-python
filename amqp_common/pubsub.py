# -*- coding: utf-8 -*-
# Copyright (C) 2020  Panayiotou, Konstantinos <klpanagi@gmail.com>
# Author: Panayiotou, Konstantinos <klpanagi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import functools
from threading import Thread, Semaphore
from collections import deque
import json
import time

from .amqp_transport import (AMQPTransportSync, Credentials, ExchangeTypes,
                             MessageProperties)
from .rate import Rate
from .msg import Message
from .serializer import JSONSerializer, ContentType


class PublisherSync(AMQPTransportSync):
    """Publisher class.

    Args:
        topic (str): The topic uri to publish data.
        exchange (str): The exchange to publish data.
        **kwargs: The keyword arguments to pass to the base class
            (AMQPTransportSync).
    """

    _SERIALIZER = JSONSerializer

    def __init__(self, topic, exchange='amq.topic', serializer=None,
                 *args, **kwargs):
        """Constructor."""
        self._topic_exchange = exchange
        self._topic = topic
        self._name = topic
        if serializer is not None:
            self._SERIALIZER = serializer
        AMQPTransportSync.__init__(self, *args, **kwargs)
        self.connect()
        self.create_exchange(self._topic_exchange, ExchangeTypes.Topic)

    def publish(self, msg, thread_safe=True):
        """ Publish message once.

        Args:
            msg (dict|Message|str|bytes): Message/Data to publish.
        """
        if isinstance(msg, Message):
            data = msg.to_dict()
        else:
            data = msg

        if thread_safe:
            self.connection.add_callback_threadsafe(
                functools.partial(self._send_data, data))
        else:
            self._send_data(data)
        self.connection.process_data_events()

    def _send_data(self, data):
        _payload = None
        _encoding = None
        _type = None

        if isinstance(data, dict):
            _payload = self._SERIALIZER.serialize(data).encode('utf-8')
            _encoding = self._SERIALIZER.CONTENT_ENCODING
            _type = self._SERIALIZER.CONTENT_TYPE
        elif isinstance(data, str):
            _type = 'text/plain'
            _encoding = 'utf8'
            _payload = data
        elif isinstance(msg, bytes):
            _type = 'application/octet-stream'
            _encoding = 'utf8'
            _payload = data

        msg_props = MessageProperties(
            content_type=_type,
            content_encoding=_encoding,
            message_id=0,
        )

        self._channel.basic_publish(
            exchange=self._topic_exchange,
            routing_key=self._topic,
            properties=msg_props,
            body=_payload)
        self.logger.debug('Sent message to topic <{}>'.format(self._topic))

    def pub_loop(self, data_bind, hz):
        """Publish message frequenntly.

        Args:
            data_bind: Pass reference to the data to bind.
            hz (float): Publishing frequency.
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


class SubscriberSync(AMQPTransportSync):
    """Subscriber class.
    Implements the Subscriber endpoint of the PubSub communication pattern.

    Args:
        topic (str): The topic uri.
        on_message (function): The callback function. This function
            is fired when messages arrive at the registered topic.
        exchange (str): The name of the exchange. Defaults to `amq.topic`
        queue_size (int): The maximum queue size of the topic.
        message_ttl (int): Message Time-to-Live as specified by AMQP.
        overflow (str): queue overflow behavior. Specified by AMQP Protocol.
            Defaults to `drop-head`.
        **kwargs: The keyword arguments to pass to the base class
            (AMQPTransportSync).
    """

    FREQ_CALC_SAMPLES_MAX = 100

    def __init__(self, topic, on_message=None, exchange='amq.topic',
                 queue_size=10, message_ttl=60000, overflow='drop-head',
                 *args, **kwargs):
        """Constructor."""
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

        _exch_ex = self.exchange_exists(self._topic_exchange)
        if _exch_ex.method.NAME != 'Exchange.DeclareOk':
            self.create_exchange(self._topic_exchange, ExchangeTypes.Topic)

        # Create a queue. Set default idle expiration time to 5 mins
        self._queue_name = self.create_queue(
            queue_size=self._queue_size,
            message_ttl=self._message_ttl,
            overflow_behaviour=self._overflow,
            expires=300000)

        # Bind queue to the Topic exchange
        self.bind_queue(self._topic_exchange, self._queue_name, self._topic)
        self._last_msg_ts = None
        self._msg_freq_fifo = deque(maxlen=self.FREQ_CALC_SAMPLES_MAX)
        self._hz = 0
        self._sem = Semaphore()

    @property
    def hz(self):
        """Incoming message frequency."""
        return self._hz

    def run(self):
        """Start Subscriber. Blocking method."""
        self._consume()

    def run_threaded(self):
        """Execute subscriber in a separate thread."""
        self.loop_thread = Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def close(self):
        if self._channel.is_closed:
            self.logger.info('Invoked close() on an already closed channel')
            return False
        self.delete_queue(self._queue_name)
        super(SubscriberSync, self).close()

    def _consume(self, reliable=False):
        """Start AMQP consumer."""
        self._channel.basic_consume(
            self._queue_name,
            self._on_msg_callback_wrapper,
            exclusive=False,
            auto_ack=(not reliable))
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt as exc:
            # Log error with traceback
            self.logger.error(exc, exc_info=True)
        except Exception as exc:
            self.logger.error(exc, exc_info=True)
            raise exc

    def _on_msg_callback_wrapper(self, ch, method, properties, body):
        msg = {}
        _ctype = None
        _cencoding = None
        _ts_send = None
        _ts_broker = None
        _dmode = None
        try:
            _ctype = properties.content_type
            _cencoding = properties.content_encoding
            _ts_broker = properties.headers['timestamp_in_ms']
            _dmode = properties.delivery_mode
            _ts_send = properties.timestamp
            # _ts_broker = properties.timestamp

            msg = self._deserialize_data(body, _ctype, _cencoding)
        except Exception:
            self.logger.error("Could not deserialize data",
                              exc_info=True)
            # Return data as is. Let callback handle with encoding...
            msg = body

        try:
            self._sem.acquire()
            self._calc_msg_frequency()
            self._sem.release()
        except Exception:
            self.logger.error("Could not calculate message rate",
                              exc_info=True)

        if self.onmessage is not None:
            meta = {
                'channel': ch,
                'method': method,
                'properties': {
                    'content_type': _ctype,
                    'content_encoding': _cencoding,
                    'timestamp_broker': _ts_broker,
                    'timestamp_producer': _ts_send,
                    'delivery_mode': _dmode
                }
            }
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

    def _deserialize_data(self, data, content_type, content_encoding):
        """
        Deserialize wire data.

        @param data: Data to deserialize.
        @type data: dict|int|bool
        """
        _data = None
        if content_encoding is None:
            content_encoding = 'utf8'
        if content_type == ContentType.json:
            _data = JSONSerializer.deserialize(data)
        elif content_type == ContentType.text:
            _data = data.decode(content_encoding)
        elif content_type == ContentType.raw_bytes:
            _data = data
        return _data
