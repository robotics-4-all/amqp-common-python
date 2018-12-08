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

        self._channel.basic_consume(self.on_response,
                                    no_ack=True,
                                    queue='amq.rabbitmq.reply-to')

    def on_response(self, ch, method, props, body):
        self._response = body

    def gen_corr_id(self):
        """Generate correlationID."""
        return str(uuid.uuid4())

    def call(self, msg, background=False, immediate=False,
             on_response=None, timeout=2.0):
        """Call RPC."""
        if not self._validate_data(msg):
            raise TypeError('Should be of type dict')
        self._response = None
        self._corr_id = self.gen_corr_id()
        try:
            rpc_props = pika.BasicProperties(reply_to='amq.rabbitmq.reply-to')
            self._channel.basic_publish(exchange=self._exchange,
                                        routing_key=self._rpc_name,
                                        immediate=immediate,
                                        properties=rpc_props,
                                        body=self._serialize_data(msg))
            self._wait_for_response(timeout)
            if self._response is None:
                resp = {
                    'error': 'RPC Response timeout'
                }
            else:
                resp = self._deserialize_data(self._response)
            return resp
        except Exception as e:
            print(e)
            return {}

    def _wait_for_response(self, timeout):
        self.logger.debug('Waiting for response from [%s]...', self._rpc_name)
        self._connection.process_data_events(
            time_limit=timeout)

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
        print(type(data))
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
