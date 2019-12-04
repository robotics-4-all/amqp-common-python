#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools
import time
from os import path
import json
import uuid

from .amqp_transport import (AMQPTransportSync,
                             Credentials,
                             ExchangeTypes,
                             MessageProperties)


class Event(object):

    __slots__ = ['name', 'payload', 'header']

    def __init__(self, name, payload={}, headers={}):
        self.name = name
        self.payload = payload
        header = {
            'timestamp': -1,
            'seq': -1,
            'agent': 'amqp-common',
            'custom': {}
        }
        for k in headers:
            header['custom'].update(headers)
        self.header = header

    def to_dict(self):
        """Serialize message object to a dict."""
        _d = {}
        for k in self.__slots__:
            # Recursive object seriazilation to dictionary
            if not k.startswith('_'):
                _prop = getattr(self, k)
                _d[k] = _prop
        return _d

    def _inc_seq(self):
        self.header['seq'] += 1

    def _set_timestamp(self, ts=None):
        if ts is None:
            self.header['timestamp'] = (1.0 * (time.time() + 0.5) * 1000)
        else:  # TODO: Check if is integer
            self.header['timestamp'] = ts


class EventEmitterOptions(object):

    __slots__ = [
        'exchange',
        'exchange_type',
        'content_type',
        'content_encoding'
    ]

    def __init__(self, exchange='amq.topic'):
        self.exchange = exchange
        self.exchange_type = ExchangeTypes.Topic
        self.content_type = 'application/json'
        self.content_encoding = 'utf8'


class EventEmitter(AMQPTransportSync):

    def __init__(self, options=None, *args, **kwargs):
        if options is None:
            options = EventEmitterOptions()
        if isinstance(options, EventEmitterOptions):
            self.options = options
        else:
            raise TypeError(
                'options argument should be of type EventEmitterOptions'
            )
        self._name = str(uuid.uuid4())[0:5]
        AMQPTransportSync.__init__(self, *args, **kwargs)
        self.connect()
        self.create_exchange(self.options.exchange, self.options.exchange_type)

    def send_event(self, event):
        if not isinstance(event, Event):
            raise TypeError(
                'event argument should be of type Event'
            )

        ts = (1.0 * (time.time() + 0.5) * 1000)
        event._inc_seq()
        event._set_timestamp(ts)
        msg_props = MessageProperties(
            content_type=self.options.content_type,
            content_encoding=self.options.content_encoding,
            timestamp=ts)

        self.connection.add_callback_threadsafe(
            functools.partial(self._send, event, msg_props))
        self.connection.process_data_events()

    def _send(self, event, props):
        self.logger.debug('Sending event: <{}:{}>'.format(event.name,
                                                          event.payload)
                          )
        self._channel.basic_publish(
            exchange=self.options.exchange,
            routing_key=event.name,
            properties=props,
            body=json.dumps(event.to_dict())
        )
