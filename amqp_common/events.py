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

from .pubsub import SubscriberSync


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

    def __init__(self, exchange='events'):
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


class InternalEventType(object):
    class Queue(object):
        DELETED = 'queue.deleted'
        CREATED = 'queue.created'

    class Exchange(object):
        DELETED = 'exchange.deleted'
        CREATED = 'exchange.created'

    class Binding(object):
        DELETED = 'binding.deleted'
        CREATED = 'binding.created'

    class Connection(object):
        CREATED = 'connection.created'
        CLOSED = 'connection.closed'

    class Channel(object):
        CREATED = 'channel.created'
        CLOSED = 'channel.closed'

    class Consumer(object):
        DELETED = 'consumer.deleted'
        CREATED = 'consumer.created'

    class User(object):
        AUTH_OK = 'user.authentication.success'
        AUTH_FAILED = 'user.authentication.failure'
        CREATED = 'user.created'
        DELETED = 'user.deleted'
        PASSWORD_CHANGED = 'user.password.changed'
        PASSWORD_CLEARED = 'user.password.cleared'
        TAGS_SET = 'user.tags.set'


class EventListenerHandle(object):
    def __init__(self, event_name, sub_obj):
        self._event_name = event_name
        self._sub = sub_obj

    @property
    def event_name(self):
        return self._event_name

    def run(self):
        self._sub.run_threaded()

    def stop(self):
        raise NotImplementedError()


class InternalEventListener(object):

    def __init__(self, connection_params, debug=False):
        self.exchange = 'amq.rabbitmq.event'
        self.connection_params = connection_params
        self.debug = debug
        self.listener_map = {}

    def listen(self, event, callback):
        listener = self._create_listener(event, callback)
        listener.run()
        self._add_listener_to_map(listener)

    def _create_listener(self, event, callback):
        sub = SubscriberSync(
            event, on_message=callback,
            exchange=self.exchange,
            connection_params=self.connection_params,
            debug=self.debug
        )
        return EventListenerHandle(event, sub)

    def _add_listener_to_map(self, listener):
        self.listener_map[listener.event_name] = listener
