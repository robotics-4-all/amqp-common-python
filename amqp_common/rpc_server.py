#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pika
import json
from .broker_interface import BrokerInterfaceSync
from threading import Thread


class RpcServer(BrokerInterfaceSync):

    def __init__(self, rpc_name, exchange='', on_request=None,
                 *args, **kwargs):
        """Constructor.

        @param rpc_name: The name of the RPC
        @type rpc_name: string
        """
        BrokerInterfaceSync.__init__(self, *args, **kwargs)
        self.connect()
        self._rpc_name = rpc_name
        self._exchange = exchange
        # Bind on_request callback
        self.on_request = on_request
        self._rpc_queue = self.create_queue(rpc_name)
        self._channel.basic_qos(prefetch_count=1)

    def run(self):
        """TODO"""
        self._channel.basic_consume(self._on_request_wrapper,
                                    queue=self._rpc_queue)
        self.logger.info("[x] - Awaiting RPC requests")
        self._channel.start_consuming()

    def run_threaded(self):
        self.loop_thread = Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

    def _on_request_wrapper(self, ch, method, properties, body):
        try:
            msg = self._deserialize_data(body)
            meta = {
                'channel': ch,
                'method': method,
                'properties': properties
            }
            resp = self.on_request(msg, meta)
        except Exception as e:
            self.logger.exception('')
            resp = {'error': str(e)}
        resp_serial = self._serialize_data(resp)
        ch.basic_publish(exchange=self._exchange,
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=properties.correlation_id),
                         body=resp_serial)
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


if __name__ == "__main__":
    def callback(ch, method, props, body):
        body = json.loads(body)
        print(body)
        a = body['a']
        b = body['b']
        c = a * b
        return c
    rpc_server = RpcServer('rpc_mult')

    rpc_server.run(callback)
