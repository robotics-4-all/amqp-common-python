#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import uuid
import json
import pika
from .broker_interface import BrokerInterfaceSync


class RpcClient(BrokerInterfaceSync):

    def __init__(self, rpc_name, *args, **kwargs):
        """
        Constructor.

        @param rpc_name: The name of the RPC
        @type rpc_name: string
        """
        BrokerInterfaceSync.__init__(self, *args, **kwargs)
        self.connect()
        self._rpc_name = rpc_name
        self._corr_id = None
        self._response = None
        self._exchange = ''  # TODO: pop from kwargs
        self._callback_queue = self.create_queue()
        self.logger.debug('Created callback queue: [{}]'.format(
            self._callback_queue))

        self._channel.basic_consume(self.on_response, no_ack=True,
                                    queue=self._callback_queue)
        self.logger.debug('Listening to messages from queue: [{}]'.format(
            self._callback_queue))

    def on_response(self, ch, method, props, body):
        if self._corr_id == props.correlation_id:
            self._response = body

    def gen_corr_id(self):
        return str(uuid.uuid4())

    def call(self, msg, background=False):
        if not self._validate_data(msg):
            raise TypeError("Should be of type dict")
        self._response = None
        self._corr_id = self.gen_corr_id()
        self._channel.basic_publish(exchange=self._exchange,
                                    routing_key=self._rpc_name,
                                    properties=pika.BasicProperties(
                                        reply_to=self._callback_queue,
                                        correlation_id=self._corr_id,
                                    ),
                                    body=self._serialize_data(msg))
        self._wait_for_response()
        resp = self._deserialize_data(self._response)
        return resp

    def _wait_for_response(self):
        while self._response is None:
            self._connection.process_data_events()

    def _serialize_data(self, data):
        """
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


if __name__ == "__main__":
    rpc_client = RpcClient('rpc_mult')
    resp = rpc_client.call({'a': 2, 'b': 4})
    print(resp)
