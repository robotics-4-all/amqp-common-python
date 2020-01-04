#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools

import time
import uuid
import json
import threading

from .amqp_transport import (AMQPTransportSync, ExchangeTypes,
                             MessageProperties)


class RpcServer(AMQPTransportSync):
    def __init__(self, rpc_name, exchange='', on_request=None, *args,
                 **kwargs):
        """Constructor.

        @param rpc_name: The name of the RPC
        @type rpc_name: string
        """
        self._name = rpc_name
        self._rpc_name = rpc_name
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

    def process_requests(self):
        self.connection.process_data_events()
        # self.conection.add_callback_threadsafe(
        #         functools.partial(self.connection.process_data_events))

    def run_threaded(self):
        """Run RPC Server in a separate thread."""
        self.loop_thread = threading.Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()
        # self.connection.add_callback_threadsafe(
        #         functools.partial(self._consume))
        # self.connection.add_callback_threadsafe(
        #         functools.partial(self._channel.start_consuming))
        # self.connection.add_callback_threadsafe(
        #         functools.partial(self.run))

    def run_async(self):
        self._consume()

    def _consume(self):
        self.consumer_tag = self._channel.basic_consume(
            self._rpc_queue,
            self._on_request_wrapper)
        self.logger.info('[x] - RPC Endpoint ready: {}'.format(self._rpc_name))

    def _on_request_wrapper(self, ch, method, properties, body):
        try:
            msg = self._deserialize_data(body)
            meta = {'channel': ch, 'method': method, 'properties': properties}
            if self.on_request is not None:
                resp = self.on_request(msg, meta)
            else:
                resp = {'error': 'Not Implemented'}
        except Exception as e:
            self.logger.exception('')
            resp = {'error': str(e)}
        if resp is None:
            resp = {}

        _data, _ctype, _encoding = self._parse_resp(resp)

        msg_props = MessageProperties(
            correlation_id=properties.correlation_id,
            content_type=_ctype,
            content_encoding=_encoding,
            timestamp=(1.0 * (time.time() + 0.5) * 1000),
            message_id=0,
            # user_id="",
            # app_id="",
        )

        ch.basic_publish(
            exchange=self._exchange,
            routing_key=properties.reply_to,
            properties=msg_props,
            body=_data)
        # Acknowledge receivving the message.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _parse_resp(self, data):
        """
        Dummy at the moment. Only check if it is of type dictionary.
        """
        _d = ""
        _ctype = ""
        _encoding = 'utf8'
        if isinstance(data, dict):
            _d = json.dumps(data)
            _ctype = 'application/json'
        elif isinstance(data, str):
            _d = data
            _ctype = 'text/plain'
        elif isinstance(data, unicode):
            _d = data
            _ctype = 'text/plain'
        else:
            raise TypeError('Msg should be either string of dict')
        return _d, _ctype, _encoding


    def _deserialize_data(self, data):
        """
        DeSerialize data.

        @param data: Data to deserialize.
        @type data: dict|int|bool
        """
        _d = {}
        try:
            _d = json.loads(data)
        except Exception:
            _d = data
        return _d

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

    def _on_response(self, ch, method, props, body):
        """Handle on-response event."""
        self.logger.debug(
            'Received Response:' + '\n- [*] Body: %s' + '\n- [*] Method: %s' +
            '\n- [*] Properties: %s' + '\n- [*] Channel: %s', body, method,
            props, ch)

        self._response = body

    def gen_corr_id(self):
        """Generate correlationID."""
        return str(uuid.uuid4())

    def call(self, msg, background=False, immediate=False, timeout=5.0):
        """Call RPC."""
        data, ctype, encoding = self._parse_msg(msg)
        self._response = None
        self._corr_id = self.gen_corr_id()
        try:
            # Direct reply-to implementation
            rpc_props = MessageProperties(
                content_type=ctype,
                content_encoding=encoding,
                timestamp=(1.0 * (time.time() + 0.5) * 1000),
                message_id=0,
                # user_id="",
                # app_id="",
                reply_to='amq.rabbitmq.reply-to'
            )

            self._channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._rpc_name,
                mandatory=False,
                properties=rpc_props,
                body=data)

            start_t = time.time()
            self._wait_for_response(timeout)
            elapsed_t = time.time() - start_t
            self._delay = elapsed_t

            if self._response is None:
                resp = {'error': 'RPC Response timeout'}
            else:
                resp = self._deserialize_data(self._response)
            return resp
        except KeyboardInterrupt as e:
            raise (e)
        except Exception:
            self.logger.exception('Exception thrown in rpc call')
            return {}

    def _wait_for_response(self, timeout):
        self.logger.debug('Waiting for response from [%s]...', self._rpc_name)
        self._connection.process_data_events(time_limit=timeout)

    def _deserialize_data(self, data):
        """
        De-serialize data.

        TODO: Make Deserialization classes. Maybe merge with serializatio
            classes. Allow for different implementations.

        @param data: Data to serialize.
        @type data: dict|int|bool
        """
        resp = None
        try:
            resp = json.loads(data)
        except Exception:
            resp = data
        resp = data.decode()
        return resp

    def _parse_msg(self, data):
        """
        Dummy at the moment. Only check if it is of type dictionary.
        """
        _raw = ""
        _ctype = ""
        _encoding = 'utf8'
        if isinstance(data, dict):
            _raw = json.dumps(data)
            _ctype = 'application/json'
        elif isinstance(data, str):
            _raw = data
            _ctype = 'text/plain'
        elif isinstance(data, unicode):
            _raw = data
            _ctype = 'text/plain'
        else:
            raise TypeError('Msg should be either string of dict')
        return _raw, _ctype, _encoding

