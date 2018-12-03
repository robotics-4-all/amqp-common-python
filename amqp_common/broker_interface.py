#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pika
import ssl
import sys
from .r4a_logger import create_logger


class ExchangeTypes(object):
    Topic = 'topic'
    Direct = 'direct'
    Fanout = 'fanout'


class Credentials(object):

    def __init__(self, username='guest', password='guest'):
        """
        Constructor.

        @param username: Client username to login
        @type username: string

        @param password: Client password
        @type password: string

        """
        self.username = username
        self.password = password


class BrokerInterfaceSync:
    DEFAULT_TOPIC_EXCHANGE = 'amq.topic'
    DEFAULT_TIMEOUT = 20.0
    DEFAULT_RETRY_DELAY = 2.0
    DEFAULT_RECONNECT_ATTEMPTS = 5
    DEFAULT_PORT = 5672
    DEFAULT_SSL_PORT = 5671
    DEFAULT_SSL = False
    DEFAULT_VIRTUAL_HOST = '/'
    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_CREDENTIALS = Credentials()

    if sys.version_info >= (3, 0):
        DEFAULT_SSL_OPTIONS = ssl.create_default_context()
        DEFAULT_SSL_OPTIONS.check_hostname = False
        DEFAULT_SSL_OPTIONS.verify_mode = ssl.CERT_NONE
    else:
        DEFAULT_SSL_OPTIONS = dict(
            cert_reqs=ssl.CERT_OPTIONAL
        )

    def __init__(self, *args, **kwargs):
        """
        TODO!!
        """
        self._connection = None
        self._channel = None
        self._closing = False
        self.logger = create_logger(self.__class__.__name__)

        self._host = self.DEFAULT_HOST
        if 'host' in kwargs:
            self._host = kwargs.pop('host')

        self._port = self.DEFAULT_PORT
        if 'port' in kwargs:
            self._port = kwargs.pop('port')

        self._credentials = self.DEFAULT_CREDENTIALS
        if 'creds' in kwargs:
            self._credentials = kwargs.pop('creds')

        self._reconnect_attempts = self.DEFAULT_RECONNECT_ATTEMPTS
        if 'reconnect_attempts' in kwargs:
            self._reconnect_attempts = kwargs.pop('reconnect_attempts')

        self._topic_exchange = self.DEFAULT_TOPIC_EXCHANGE
        if 'topic_exchange' in kwargs:
            self._topic_exchange = kwargs.pop('topic_exchange')

        self._ssl = self.DEFAULT_SSL
        if 'ssl' in kwargs:
            self._ssl = kwargs.pop('ssl')

        self._ssl_port = self.DEFAULT_SSL_PORT
        if 'ssl_port' in kwargs:
            self._ssl_port = kwargs.pop('ssl_port')

        self._retry_delay = self.DEFAULT_RETRY_DELAY
        if 'retry_delay' in kwargs:
            self._retry_delay = kwargs.pop('retry_delay')

        self._timeout = self.DEFAULT_TIMEOUT
        if 'timeout' in kwargs:
            self._timeout = kwargs.pop('timeout')

        self._ssl_options = self.DEFAULT_SSL_OPTIONS
        if 'ssl_options' in kwargs:
            self._ssl_options = kwargs.pop('ssl_options')

        if self._ssl:
            self._port = self._ssl_port

        self._creds_pika = pika.PlainCredentials(self._credentials.username,
                                                 self._credentials.password)

    def connect(self):
        """
        Connect to the AMQP broker.
        """
        self._connect_params = pika.ConnectionParameters(
            host=self._host, port=self._port,
            credentials=self._creds_pika,
            connection_attempts=self._reconnect_attempts,
            retry_delay=self._retry_delay,
            blocked_connection_timeout=self._timeout,
            socket_timeout=self._timeout
        )

        try:
            self._connection = pika.BlockingConnection(self._connect_params)
            self._channel = self._connection.channel()
        except Exception as exc:
            self.logger.exception('')
            raise exc
            return False
        self.logger.info("Connected to AMQP broker @ [{}:{}]".format(
            self._host, self._port))
        return True

    def setup_exchange(self, exchange_name, exchange_type):
        """
        Create a new exchange.

        @param exchange_name: The name of the exchange (e.g. com.logging).
        @type exchange_name: string

        @param exchange_type: The type of the exchange (e.g. 'topic').
        @type exchange_type: string
        """
        self.logger.info('Declaring exchange: [name={}, type={}]'.format(
            exchange_name, exchange_type))
        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type=exchange_type,
                                       passive=True)

    def create_queue(self, queue_name='', exclusive=True):
        """
        Creates a new queue.

        @param queue_name: The name of the queue.
        @type queue_name: string

        @param exclusive: Only allow access by the current connection.
        @type exclusive: bool
        """
        result = self._channel.queue_declare(exclusive=exclusive,
                                             queue=queue_name,
                                             durable=False,
                                             auto_delete=True)
        queue_name = result.method.queue
        self.logger.info("Created queue [{}]".format(queue_name))
        return queue_name

    def bind_queue(self, exchange_name, queue_name, bind_key):
        """
        Bind a queue to and exchange using a bind-key.

        @param exchange_name: The name of the exchange (e.g. com.logging).
        @type exchange_name: string

        @param queue_name: The name of the queue.
        @type queue_name: string

        @param bind_key: The binding key name.
        @type bind_key: string
        """
        self.logger.info('Subscribed to topic: {}'.format(bind_key))
        try:
            self._channel.queue_bind(exchange=exchange_name,
                                     queue=queue_name,
                                     routing_key=bind_key)
        except Exception:
            self.logger.exception()

    def __del__(self):
        try:
            self._connection.close()
        except Exception:
            pass


class BrokerInterfaceAsync(object):
    CONNECTION_TIMEOUT_SEC = 5

    def __init__(self, host='127.0.0.1', port='5672',
                 exchange='amq.topic'):
        self._connection = None
        self._channel = None
        self._closing = False
        self.logger = create_logger(self.__class__.__name__)
        self._exchange = 'amq.topic'
        self._host = host
        self._port = port
        super(BrokerInterfaceAsync, self).__init__()

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection
        """
        self.logger.info("Connecting to AMQP broker @ [{}:{}] ...".format(
            self._host, self._port))
        connection = pika.SelectConnection(
            pika.URLParameters(host=self.host,
                               port=self.port),
            self.on_connection_open,
            stop_ioloop_on_close=False)
        return connection

    def on_connection_open(self, unused_connection):
        """
        This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        self.logger.info('Connection established!')
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        """
        This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """
        self.logger.info('Adding connection close callback')
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """
        This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self.logger.warning(
                'Connection closed, reopening in 5 seconds: (%s) %s',
                reply_code, reply_text)
            self._connection.add_timeout(self.CONNECTION_TIMEOUT_SEC,
                                         self.reconnect)

    def reconnect(self):
        """
        Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:
            # Create a new connection
            self._connection = self.connect()
            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def open_channel(self):
        """
        Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        self.logger.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def _on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.
        IMPLEMENT IN INHERITED CLASSES!!!!!!!!

        :param pika.channel.Channel channel: The channel object

        """
        self.logger.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()

    def on_channel_open(self, channel):
        pass

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        self.logger.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self.logger.warning('Channel %i was closed: (%s) %s',
                            channel, reply_code, reply_text)
        self._connection.close()

    def create_exchange(self, exchange_name, exchange_type):
        self.logger.info('Declaring exchange {} [type={}]', exchange_name,
                         exchange_type)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange=exchange_name,
                                       exchange_type=exchange_type)

    def _create_queue(self, queue_name=''):
        result = self._channel.queue_declare(exclusive=True,
                                             queue=queue_name)
        queue_name = result.method.queue
        self._queue_name = queue_name
        self.logger.info("Created queue [{}]".format(queue_name))
        return queue_name

    def _bind_queue(self, exchange_name, queue_name, bind_key):
        try:
            self._channel.queue_bind(exchange=exchange_name,
                                     queue=queue_name,
                                     routing_key=bind_key)
        except Exception:
            self.logger.exception()

    def __del__(self):
        self._connection.close()
