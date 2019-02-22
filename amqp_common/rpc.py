#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools

from threading import Thread

import uuid
import json

import pika

from .amqp_transport import (AMQPTransportSync, Credentials, ExchangeTypes,
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
        self.connect()
        self._exchange = exchange
        # Bind on_request callback
        self.on_request = on_request

        self._rpc_queue = self.create_queue(self._rpc_name)
        self._channel.basic_qos(prefetch_count=1)

    def is_alive(self):
        if self.connection is None:
            return False
        elif self.connection.is_open:
            return True
        else:
            return False

    def run(self):
        """."""
        self._channel.basic_consume(
            self._on_request_wrapper, queue=self._rpc_queue)
        self.logger.info('[x] - Awaiting RPC requests')
        self._channel.start_consuming()

    def process_requests(self):
        self.connection.process_data_events()

    def run_threaded(self):
        """Run RPC Server in a separate thread."""
        #  self.loop_thread = Thread(target=self.run)
        #  self.loop_thread.daemon = True
        #  self.loop_thread.start()
        #  self.add_callback_thread_safe(self.run)
        self.connection.add_callback_threadsafe(functools.partial(self.run))

    def run_async(self):
        self._channel.basic_consume(
            self._on_request_wrapper, queue=self._rpc_queue)
        self.logger.info('[x] - Awaiting RPC requests')

    def _on_request_wrapper(self, ch, method, properties, body):
        self.logger.debug(
            'Received Request:' + '\n- [*] Method: %s' +
            '\n- [*] Properties: %s' + '\n- [*] Channel: %s', method,
            properties, ch)
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
        resp_serial = self._serialize_data(resp)

        msg_props = MessageProperties(correlation_id=properties.correlation_id)

        ch.basic_publish(
            exchange=self._exchange,
            routing_key=properties.reply_to,
            properties=msg_props,
            body=resp_serial)
        # Acknowledge receivving the message.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _serialize_data(self, data):
        """
        Serialize data.
        TODO: Make class. ALlow for different implementations.

        @param data: Data to serialize.
        @type data: dict|int|bool
        """
        return json.dumps(data)

    def _deserialize_data(self, data):
        """
        DeSerialize data.
        TODO: Make class. ALlow for different implementations.

        @param data: Data to deserialize.
        @type data: dict|int|bool
        """
        return json.loads(data)

    def close(self):
        if self._channel.is_closed:
            self.logger.warning('Invoked close() on an already closed channel')
            return False
        self.delete_queue(self._rpc_queue)
        super(RpcServer, self).close()

    def __del__(self):
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

        self._channel.basic_consume(
            self._on_response, no_ack=True, queue='amq.rabbitmq.reply-to')

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
        if not self._validate_data(msg):
            raise TypeError('Should be of type dict')
        self._response = None
        self._corr_id = self.gen_corr_id()
        try:
            # Direct reply-to implementation
            rpc_props = MessageProperties(reply_to='amq.rabbitmq.reply-to')

            self._channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._rpc_name,
                immediate=immediate,
                properties=rpc_props,
                body=self._serialize_data(msg))

            self._wait_for_response(timeout)

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

    def _serialize_data(self, data):
        """
        Serialize data.

        TODO: Make Class. Allow different implementation of serialization
            classes.
        """
        return json.dumps(data)

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
            return resp
        except Exception:
            pass
        resp = data.decode()
        return resp

    def _validate_data(self, data):
        """
        Dummy at the moment. Only check if it is of type dictionary.
        """
        if isinstance(data, dict):
            return True
        else:
            return False
