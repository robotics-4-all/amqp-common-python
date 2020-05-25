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
    """Implementation of the Event object.

    Args:
        name (str): The name of the event.
        payload (dict): Dictionary payload of the event.
        headers (dict): Event headers to set.
    """

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
        """Set timestamp header"""
        if ts is None:
            self.header['timestamp'] = (1.0 * (time.time() + 0.5) * 1000)
        else:  # TODO: Check if is integer
            self.header['timestamp'] = ts


class EventEmitterOptions(object):
    """EventEmitterOptions class.

    Used to configure an EventEmitter.

    Args:
        exchange (str): The exchange to send the events.
        content_type (str): Set the MIME of the contents. Defaults to
            `application/json`.
        content_encoding (str): Set the encoding of the contents. Defaults
            to `utf8`.
    """

    __slots__ = [
        'exchange',
        'exchange_type',
        'content_type',
        'content_encoding'
    ]

    def __init__(self, exchange='events', content_type='application/json',
                 content_encoding='utf8'):
        self.exchange = exchange
        self.exchange_type = ExchangeTypes.Topic
        self.content_type = content_type
        self.content_encoding = content_encoding


class EventEmitter(AMQPTransportSync):
    """EventEmitter class.
    The `EventEmitter` class implements an event-based approach of communication.
    It uses a dedicated exchange and fires `Event` objects at specific URIs.
    An `Event` is defined by a name, the payload and headers. The relation
    between an event name and the uri is direct.

    Args:
        options (object): EventEmitterOptions instance.
        **kwargs: Keyword arguments for the constructor of the SubscriberSync.
    """

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
    """RabbitMQ Internal Event Types."""
    class Queue(object):
        """Queue Events."""
        DELETED = 'queue.deleted'
        CREATED = 'queue.created'

    class Exchange(object):
        """Exchange Events."""
        DELETED = 'exchange.deleted'
        CREATED = 'exchange.created'

    class Binding(object):
        """Binding Events."""
        DELETED = 'binding.deleted'
        CREATED = 'binding.created'

    class Connection(object):
        """Connection Events."""
        CREATED = 'connection.created'
        CLOSED = 'connection.closed'

    class Channel(object):
        """Channel Events."""
        CREATED = 'channel.created'
        CLOSED = 'channel.closed'

    class Consumer(object):
        """Consumer Events."""
        DELETED = 'consumer.deleted'
        CREATED = 'consumer.created'

    class User(object):
        """User Events."""
        AUTH_OK = 'user.authentication.success'
        AUTH_FAILED = 'user.authentication.failure'
        CREATED = 'user.created'
        DELETED = 'user.deleted'
        PASSWORD_CHANGED = 'user.password.changed'
        PASSWORD_CLEARED = 'user.password.cleared'
        TAGS_SET = 'user.tags.set'


class RabbitMQEventHandle(object):
    """RabbitMQ Internal Event Handle class.

    Args:
        event_name (str): The name of the internal event.
        sub_obj (object): SubscriberSync instance.
    """
    def __init__(self, event_name, sub_obj):
        self._event_name = event_name
        self._sub = sub_obj

    @property
    def event_name(self):
        return self._event_name

    def run(self):
        """Run subscriber in a separate thread."""
        self._sub.run_threaded()

    def stop(self):
        """Stop subscriber."""
        raise NotImplementedError()


class RabbitMQEventListener(object):
    """RabbitMQ Internal Event listener class
    This implementation provides means of listening to rabbitmq internal
    events and registener listeners/actors. RabbitMQ implements an
    internal event alerting subsystem and events are published on the
    `amq.rabbitmq.event` exchange.

    Args:
        connection_params (object): ConnectionParameters instance..
        debug (bool): Enable/Disable debug mode.
    """

    def __init__(self, connection_params, debug=False):
        """Constructor of the class."""
        self.exchange = 'amq.rabbitmq.event'
        self.connection_params = connection_params
        self.debug = debug
        self.listener_map = {}

    def listen(self, event, callback):
        """Listen to internal event.

        Args:
            event (str): The name of the event.
            callback (function): The callback function to register (actor).

        Returns:
            object: a RabbitMQEventHandle instance.

        """
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
        return RabbitMQEventHandle(event, sub)

    def _add_listener_to_map(self, listener):
        self.listener_map[listener.event_name] = listener
