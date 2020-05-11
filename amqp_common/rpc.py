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


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

import sys
import functools

if sys.version_info[0] >= 3:
    unicode = str

import time
import uuid
import json
import threading

from .amqp_transport import (
    AMQPTransportSync, ExchangeTypes, MessageProperties
)

from .serializer import JSONSerializer, ContentType
from .msg import Message


class RpcServer(AMQPTransportSync):
    """AMQP RPC Server implementation"""

    _SERIALIZER = JSONSerializer

    def __init__(self,
                 rpc_name,
                 exchange='',
                 on_request=None,
                 serializer=None,
                 *args,
                 **kwargs):
        """Constructor.

        @param rpc_name: The name of the RPC
        @type rpc_name: str

        @param exchange: The RPC exchange. Defaults to '' (Default exchange)
        @type exchange: str

        @param on_request: RPC callback. onrequest(msg, meta)
        @type on_request: function
        """
        self._name = rpc_name
        self._rpc_name = rpc_name

        if serializer is not None:
            self._SERIALIZER = serializer

        AMQPTransportSync.__init__(self, *args, **kwargs)
        self._exchange = exchange
        # Bind on_request callback
        self.on_request = on_request

    def is_alive(self):
        if self.connection is None:
            return False
        elif self.connection.is_open:
            return True
        else:
            return False

    def run(self):
        """."""
        self.connect()
        self._rpc_queue = self.create_queue(self._rpc_name)
        self._channel.basic_qos(prefetch_count=1, global_qos=False)
        self._consume()
        try:
            self._channel.start_consuming()
        except Exception as exc:
            self.logger.error(exc, exc_info=True)

    def process_amqp_events(self):
        self.connection.process_data_events()
        # self.conection.add_callback_threadsafe(
        #         functools.partial(self.connection.process_data_events))

    def run_threaded(self):
        """Run RPC Server in a separate thread."""
        self.loop_thread = threading.Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def run_async(self):
        self._consume()

    def _consume(self):
        self.consumer_tag = self._channel.basic_consume(
            self._rpc_queue,
            self._on_request_wrapper)
        self.logger.info('[x] - RPC Endpoint ready: {}'.format(self._rpc_name))

    def _on_request_wrapper(self, ch, method, properties, body):
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
        except Exception:
            self.logger.error("Could not calculate latency",
                              exc_info=True)

        try:
            _msg = self._deserialize_data(body, _ctype, _cencoding)
        except Exception:
            self.logger.error("Could not deserialize data",
                              exc_info=True)
            # Return data as is. Let callback handle with encoding...
            _msg = body

        if self.on_request is not None:
            _meta = {
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
            resp = self.on_request(_msg, _meta)
        else:
            resp = {
                'error': 'Not Implemented',
                'status': 501
            }

        try:
            _payload = None
            _encoding = None
            _type = None

            if isinstance(resp, dict):
                _payload = self._SERIALIZER.serialize(resp).encode('utf-8')
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

        except Exception as e:
            self.logger.error("Could not deserialize data",
                              exc_info=True)
            _payload = {
                'status': 501,
                'error': 'Internal server error: {}'.format(str(e))
            }

        _msg_props = MessageProperties(
            content_type=_type,
            content_encoding=_encoding,
        )

        ch.basic_publish(
            exchange=self._exchange,
            routing_key=properties.reply_to,
            properties=_msg_props,
            body=_payload)
        # Acknowledge receiving the message.
        ch.basic_ack(delivery_tag=method.delivery_tag)

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

    def close(self):
        if not self._channel:
            return
        if self._channel.is_closed:
            self.logger.warning('Channel was already closed!')
            return False
        self._channel.stop_consuming()
        # super(RpcServer, self).close()
        self.delete_queue(self._rpc_queue)
        return True

    def stop(self):
        return self.close()

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, value, traceback):
        self.close()


class RpcClient(AMQPTransportSync):
    """AMQP RPC Client Implementation."""
    _SERIALIZER = JSONSerializer

    def __init__(self, rpc_name, *args, **kwargs):
        """
        Constructor.

        @param rpc_name: The name of the RPC
        @type rpc_name: string
        """
        self._name = rpc_name
        self._rpc_name = rpc_name
        AMQPTransportSync.__init__(self, *args, **kwargs)
        self.connect()
        self._corr_id = None
        self._response = None
        self._exchange = ExchangeTypes.Default
        self._mean_delay = 0
        self._delay = 0
        self.onresponse = None

        self._consumer_tag = self._channel.basic_consume(
            'amq.rabbitmq.reply-to',
            self._on_response,
            exclusive=False,
            consumer_tag=None,
            auto_ack=True)

    @property
    def mean_delay(self):
        return self._mean_delay

    @property
    def delay(self):
        return self._delay

    def _on_response(self, ch, method, properties, body):
        _ctype = None
        _cencoding = None
        _ts_send = None
        _ts_broker = 0
        _dmode = None
        _msg = None
        _meta = None
        try:
            _ctype = properties.content_type
            _cencoding = properties.content_encoding
            if hasattr(self, 'headers'):
                if 'timestamp_in_ms' in properties.headers:
                    _ts_broker = properties.headers['timestamp_in_ms']

            _dmode = properties.delivery_mode
            _ts_send = properties.timestamp

            _meta = {
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
        except Exception:
            self.logger.error("Error parsing response from rpc server.",
                              exc_info=True)

        try:
            _msg = self._deserialize_data(body, _ctype, _cencoding)
        except Exception:
            self.logger.error("Could not deserialize data",
                              exc_info=True)
            _msg = body


        self._response = _msg
        self._response_meta = _meta

        if self.onresponse is not None:
            self.onresponse(_msg, _meta)

    def gen_corr_id(self):
        """Generate correlationID."""
        return str(uuid.uuid4())

    def call(self, msg, timeout=5.0):
        """Call RPC."""
        self._response = None
        self._corr_id = self.gen_corr_id()
        if isinstance(msg, Message):
            data = msg.to_dict()
        else:
            data = msg
        self._send_data(data)
        start_t = time.time()
        self._wait_for_response(timeout)
        elapsed_t = time.time() - start_t
        self._delay = elapsed_t

        if self._response is None:
            resp = {'error': 'RPC Response timeout'}
        else:
            resp = self._response
        return resp

    def _wait_for_response(self, timeout):
        self.logger.debug('Waiting for response from [%s]...', self._rpc_name)
        self._connection.process_data_events(time_limit=timeout)

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

        # Direct reply-to implementation
        _rpc_props = MessageProperties(
            content_type=_type,
            content_encoding=_encoding,
            # timestamp=(1.0 * (time.time() + 0.5) * 1000),
            message_id=0,
            # user_id="",
            # app_id="",
            reply_to='amq.rabbitmq.reply-to'
        )

        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._rpc_name,
            mandatory=False,
            properties=_rpc_props,
            body=_payload)

