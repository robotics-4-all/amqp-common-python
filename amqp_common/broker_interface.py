#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pika
#  import ssl

from .r4a_logger import create_logger, LoggingLevel


class ConnectionParameters(object):
    """AMQP Connection parameters."""

    __slots__ = [
        'host', 'port', 'secure', 'vhost', 'reconnect_attempts', 'retry_delay',
        'timeout', 'heartbeat'
    ]

    def __init__(self,
                 host='127.0.0.1',
                 port='5672',
                 secure=False,
                 vhost='/',
                 reconnect_attempts=5,
                 retry_delay=2.0,
                 timeout=10.0,
                 blocked_connection_timeout=None,
                 heartbeat=120):
        """
        Constructor.

        @param host: Hostname of AMQP broker
        @type host: string

        @param port: AMQP broker listening port
        @type port: string

        @param secure: Enable SSL/TLS - AMQPS
        @type secure: boolean

        @param reconnect_attempts: TODO
        @type reconnect_attempts: int

        @param retry_delay: Time delay between reconnect attempts
        @type retry_delay: float

        @param timeout: Connection timeout value.
        @type timeout: float

        @param heartbeat: Set time period for sending heartbeat packages.
            Heartbeat packages denote that the connection is alive in
            both ends. Value is set in seconds.
        @type heartbeat: int
        """
        self.host = host
        self.port = port
        self.secure = secure
        self.vhost = vhost
        self.reconnect_attempts = reconnect_attempts
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.blocked_connection_timeout = blocked_connection_timeout
        self.heartbeat = heartbeat


class ExchangeTypes(object):
    """AMQP Exchange Types."""

    __slots__ = ['Topic', 'Direct', 'Fanout', 'Default']

    Topic = 'topic'
    Direct = 'direct'
    Fanout = 'fanout'
    Default = ''


class Credentials(object):
    """Connection credentials for authn/authz."""

    __slots__ = ['username', 'password']

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


class SharedConnection(object):
    """Shared Connection."""

    def __init__(self):
        """Constructor."""
        pass


class BrokerInterfaceSync(object):
    """Broker Interface."""

    def __init__(self, *args, **kwargs):
        """TODO."""
        self._connection = None
        self._channel = None
        self._closing = False
        self.logger = create_logger('{}-{}'.format(self.__class__.__name__,
                                                   self._name))

        if 'debug' in kwargs:
            self.debug = kwargs.pop('debug')
        else:
            self.debug = False

        if 'creds' in kwargs:
            self.credentials = kwargs.pop('creds')
        else:
            self.credentials = Credentials()

        if 'connection_params' in kwargs:
            self.connection_params = kwargs.pop('connection_params')
        else:
            # Default Connection Parameters
            self.connection_params = ConnectionParameters()

        if 'connection' in kwargs:
            self._connection = kwargs.pop('connection')

        self._creds_pika = pika.PlainCredentials(self.credentials.username,
                                                 self.credentials.password)

    @property
    def debug(self):
        """Debug mode flag."""
        return self._debug

    @debug.setter
    def debug(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be boolean')
        self._debug = val
        if self._debug is True:
            self.logger.setLevel(LoggingLevel.DEBUG)
        else:
            self.logger.setLevel(LoggingLevel.INFO)

    def connect(self):
        """Connect to the AMQP broker."""
        host = self.connection_params.host
        port = self.connection_params.port
        vhost = self.connection_params.vhost
        reconnect_attempts = self.connection_params.reconnect_attempts
        timeout = self.connection_params.timeout
        blocked_connection_timeout = self.connection_params.blocked_connection_timeout
        retry_delay = self.connection_params.retry_delay
        # Meh, no secure at the moment, TODO!
        secure = self.connection_params.secure
        heartbeat = self.connection_params.heartbeat

        self._connect_params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=self._creds_pika,
            connection_attempts=reconnect_attempts,
            retry_delay=retry_delay,
            blocked_connection_timeout=blocked_connection_timeout,
            socket_timeout=timeout,
            virtual_host=vhost,
            heartbeat=heartbeat)

        try:
            if self._connection is None:
                # Create a new connection
                self._connection = pika.BlockingConnection(
                    self._connect_params)
            self._channel = self._connection.channel()
        except Exception as exc:
            self.logger.exception('')
            raise exc
            return False
        self.logger.info('Connected to AMQP broker @ [{}:{}]'.format(
            host, port))
        self.logger.info('Vhost -> {}'.format(vhost))
        return True

    def setup_exchange(self, exchange_name, exchange_type):
        """
        Create a new exchange.

        @param exchange_name: The name of the exchange (e.g. com.logging).
        @type exchange_name: string

        @param exchange_type: The type of the exchange (e.g. 'topic').
        @type exchange_type: string
        """
        self.logger.debug('Declaring exchange: [name={}, type={}]'.format(
            exchange_name, exchange_type))
        self._channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type, passive=True)

    def create_queue(self,
                     queue_name='',
                     exclusive=True,
                     queue_size=10,
                     queue_ttl=60000,
                     overflow_behaviour='drop-head'):
        """
        Create a new queue.

        - Overflow Behaviours: https://www.rabbitmq.com/maxlength.html#overflow-behaviour

        @param queue_name: The name of the queue.
        @type queue_name: string

        @param exclusive: Only allow access by the current connection.
        @type exclusive: bool

        @param queue_size: The size of the queue
        @type queue_size: int

        @param queue_ttl: Per-queue message time-to-live
            (https://www.rabbitmq.com/ttl.html)
        @type queue_ttl: int

        @param overflow_behaviour: Overflow behaviour - 'drop-head' ||
            'reject-publish'
        @type overflow_behaviour: str
        """
        args = {
            'x-max-length': queue_size,
            'x-overflow': overflow_behaviour,
            'x-message-ttl': queue_ttl
        }

        result = self._channel.queue_declare(
            exclusive=exclusive,
            queue=queue_name,
            durable=False,
            auto_delete=True,
            arguments=args)
        queue_name = result.method.queue
        self.logger.debug('Created queue [{}] [size={}, ttl={}]'.format(
            queue_name, queue_size, queue_ttl))
        return queue_name

    def queue_exists(self, queue_name):
        """
        TODO.

        https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.queue_declare
        """
        pass

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
            self._channel.queue_bind(
                exchange=exchange_name, queue=queue_name, routing_key=bind_key)
        except Exception:
            self.logger.exception()

    def __del__(self):
        """Destructor."""
        try:
            self._connection.close()
        except Exception:
            pass


class BrokerInterfaceAsync(object):
    CONNECTION_TIMEOUT_SEC = 5

    def __init__(self, host='127.0.0.1', port='5672', exchange='amq.topic'):
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
            pika.URLParameters(host=self.host, port=self.port),
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
        self.logger.warning('Channel %i was closed: (%s) %s', channel,
                            reply_code, reply_text)
        self._connection.close()

    def create_exchange(self, exchange_name, exchange_type):
        """
        Declare/Create an exchange.

        @param exchange_name: The name of the exchange
        @type exchange_name: string

        @param exchange_type: the type of the exchange
        @type exchange_type:
        """
        self.logger.debug('Declaring exchange {} [type={}]', exchange_name,
                          exchange_type)
        self._channel.exchange_declare(
            self.on_exchange_declareok,
            exchange=exchange_name,
            exchange_type=exchange_type)

    def _create_queue(self, queue_name=''):
        result = self._channel.queue_declare(exclusive=True, queue=queue_name)
        queue_name = result.method.queue
        self._queue_name = queue_name
        self.logger.info("Created queue [{}]".format(queue_name))
        return queue_name

    def _bind_queue(self, exchange_name, queue_name, bind_key):
        try:
            self._channel.queue_bind(
                exchange=exchange_name, queue=queue_name, routing_key=bind_key)
        except Exception:
            self.logger.exception()

    def __del__(self):
        self._connection.close()
