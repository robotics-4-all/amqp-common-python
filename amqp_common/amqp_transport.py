#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
import atexit
import signal
import json

import pika
#  import ssl

from .r4a_logger import create_logger, LoggingLevel


class MessageProperties(pika.BasicProperties):
    def __init__(self,
                 content_type=None,
                 content_encoding=None,
                 timestamp=None,
                 correlation_id=None,
                 reply_to=None,
                 message_id=None,
                 user_id=None,
                 app_id=None):
        """Message Properties/Attribures used for sending and receiving messages.

        @param content_type:

        @param content_encoding:

        @param timestamp

        """
        if timestamp is None:
            timestamp = (time.time() + 0.5) * 1000
        timestamp = int(timestamp)
        super(MessageProperties, self).__init__(
            content_type=content_type,
            content_encoding=content_encoding,
            timestamp=timestamp,
            correlation_id=correlation_id,
            reply_to=reply_to,
            message_id=str(message_id) if message_id is not None else None,
            user_id=str(user_id) if user_id is not None else None,
            app_id=str(app_id) if app_id is not None else None
        )


class ConnectionParameters(pika.ConnectionParameters):
    """AMQP Connection parameters."""

    __slots__ = [
        'host', 'port', 'secure', 'vhost', 'reconnect_attempts', 'retry_delay',
        'timeout', 'heartbeat_timeout', 'blocked_connection_timeout', 'creds'
    ]

    def __init__(self,
                 host='127.0.0.1',
                 port='5672',
                 creds=None,
                 secure=False,
                 vhost='/',
                 reconnect_attempts=5,
                 retry_delay=2.0,
                 timeout=120,
                 blocked_connection_timeout=None,
                 heartbeat_timeout=60,
                 channel_max=128):
        """
        Constructor.

        @param host: Hostname of AMQP broker to connect to.
        @type host: string

        @param port: AMQP broker listening port.
        @type port: string

        @param creds: AUth Credentials.
        @type creds: Credentials

        @param secure: Enable SSL/TLS (AMQPS) - Not used!!
        @type secure: boolean

        @param reconnect_attempts: TODO
        @type reconnect_attempts: int

        @param retry_delay: Time delay between reconnect attempts.
        @type retry_delay: float

        @param timeout: Socket Connection timeout value.
        @type timeout: float

        @param timeout: Blocked Connection timeout value.
            Set the timeout, in seconds, that the connection may remain blocked
            (triggered by Connection.Blocked from broker). If the timeout expires
            before connection becomes unblocked, the connection will be torn down.
        @type timeout: float

        @param heartbeat_timeout: Controls AMQP heartbeat timeout negotiation
            during connection tuning. An integer value always overrides the value
            proposed by broker. Use 0 to deactivate heartbeats and None to always
            accept the broker's proposal. The value passed for timeout is also
            used to calculate an interval at which a heartbeat frame is sent to
            the broker. The interval is equal to the timeout value divided by two.
        @type heartbeat_timeout: int

        @param channel_max: The max permissible number of channels per connection.
            Defaults to 128
        @type channel_max: int
        """
        self.host = host
        self.port = port
        self.secure = secure
        self.vhost = vhost
        self.reconnect_attempts = reconnect_attempts
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.blocked_connection_timeout = blocked_connection_timeout
        self.heartbeat_timeout = heartbeat_timeout
        self.channel_max = channel_max

        if creds is None:
            creds = Credentials()

        super(ConnectionParameters, self).__init__(
            host=host,
            port=str(port),
            credentials=creds,
            connection_attempts=reconnect_attempts,
            retry_delay=retry_delay,
            blocked_connection_timeout=blocked_connection_timeout,
            socket_timeout=timeout,
            virtual_host=vhost,
            heartbeat=heartbeat_timeout,
            channel_max=channel_max)

    def __str__(self):
        _properties = {
            'host': self.host,
            'port': self.port,
            'vhost': self.vhost,
            'reconnect_attempts': self.reconnect_attempts,
            'retry_delay': self.retry_delay,
            'timeout': self.timeout,
            'blocked_connection_timeout': self.blocked_connection_timeout,
            'heartbeat_timeout': self.heartbeat_timeout,
            'channel_max': self.channel_max
        }
        _str = json.dumps(_properties)
        return _str


class ExchangeTypes(object):
    """AMQP Exchange Types."""
    Topic = 'topic'
    Direct = 'direct'
    Fanout = 'fanout'
    Default = ''


class Credentials(pika.PlainCredentials):
    """Connection credentials for authn/authz.
    TODO: Inherit from pika.PlainCredentials
    """

    __slots__ = ['username', 'password']

    def __init__(self, username='guest', password='guest'):
        """
        Constructor.

        @param username: Client username to login
        @type username: string

        @param password: Client password
        @type password: string

        """
        super(Credentials, self).__init__(username=username, password=password)


class SharedConnection(pika.BlockingConnection):
    """Shared Connection."""

    def __init__(self, connection_params):
        """Constructor."""
        self._connection_params = connection_params
        self._pika_connection = None
        super(SharedConnection,
              self).__init__(parameters=self._connection_params)


class AMQPTransportSync(object):
    """Broker Interface."""

    def __init__(self, *args, **kwargs):
        """TODO."""
        self._connection = None
        self._channel = None
        self._closing = False
        self._debug = False
        self.logger = None

        if 'logger' in kwargs:
            self.logger = kwargs.pop('logger')
        else:
            self.logger = create_logger('{}-{}'.format(
                self.__class__.__name__, self._name))

        if 'debug' in kwargs:
            self.debug = kwargs.pop('debug')
        else:
            self.debug = False

        if 'connection_params' in kwargs:
            self.connection_params = kwargs.pop('connection_params')
        else:
            # Default Connection Parameters
            self.connection_params = ConnectionParameters()

        if 'creds' in kwargs:
            self.credentials = kwargs.pop('creds')
            self.connection_params.credentials = self.credentials
        else:
            self.credentials = self.connection_params.credentials

        if 'connection' in kwargs:
            self._connection = kwargs.pop('connection')

        # So that connections do not go zombie
        atexit.register(self._graceful_shutdown)
        #  signal.signal(signal.SIGTERM, self._signal_handler)
        #  signal.signal(signal.SIGINT, self._signal_handler)

    @property
    def channel(self):
        return self._channel

    @property
    def connection(self):
        return self._connection

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
        """Connect to the AMQP broker. Creates a new channel."""
        if self._connection is not None:
            self.logger.debug('Using allready existing connection [{}]'.format(
                self._connection))
            # Create a new communication channel
            self._channel = self._connection.channel()
            return True
        try:
            # Create a new connection
            self.logger.debug(
                    'Connecting to AMQP broker @ [{}:{}, vhost={}]...'.format(
                        self.connection_params.host,
                        self.connection_params.port,
                        self.connection_params.vhost))
            self.logger.debug('Connection parameters:')
            self.logger.debug(self.connection_params)
            self._connection = SharedConnection(self.connection_params)
            # Create a new communication channel
            self._channel = self._connection.channel()
            self.logger.info(
                    'Connected to AMQP broker @ [{}:{}, vhost={}]'.format(
                        self.connection_params.host,
                        self.connection_params.port,
                        self.connection_params.vhost))
        except pika.exceptions.ConnectionClosed:
            self.logger.debug('Connection timed out. Reconnecting...')
            return self.connect()
        except pika.exceptions.AMQPConnectionError:
            self.logger.debug('Connection error. Reconnecting...')
            return self.connect()
        except Exception as exc:
            self.logger.exception('')
            raise (exc)
        return self._channel

    def _signal_handler(self, signum, frame):
        self.logger.info('Signal received: ', signum)
        self._graceful_shutdown()

    def _graceful_shutdown(self):
        if not self.connection:
            return
        if self._channel.is_closed:
            # self.logger.warning('Channel is allready closed')
            return
        self.logger.debug('Invoking a graceful shutdown...')
        self._channel.stop_consuming()
        self._channel.close()
        self.logger.debug('Channel closed!')

    def create_exchange(self, exchange_name, exchange_type):
        """
        Create a new exchange.

        @param exchange_name: The name of the exchange (e.g. com.logging).
        @type exchange_name: string

        @param exchange_type: The type of the exchange (e.g. 'topic').
        @type exchange_type: string
        """
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            passive=True)

        self.logger.debug('Created exchange: [name={}, type={}]'.format(
            exchange_name, exchange_type))

    def create_queue(self,
                     queue_name='',
                     exclusive=True,
                     queue_size=10,
                     message_ttl=60000,
                     overflow_behaviour='drop-head',
                     expires=600000):
        """
        Create a new queue.

        @param queue_name: The name of the queue.
        @type queue_name: string

        @param exclusive: Only allow access by the current connection.
        @type exclusive: bool

        @param queue_size: The size of the queue
        @type queue_size: int

        @param message_ttl: Per-queue message time-to-live
            (https://www.rabbitmq.com/ttl.html#per-queue-message-ttl)
        @type message_ttl: int

        @param overflow_behaviour: Overflow behaviour - 'drop-head' ||
            'reject-publish'.
            https://www.rabbitmq.com/maxlength.html#overflow-behaviour
        @type overflow_behaviour: str

        @param expires: Queues will expire after a period of time only
            when they are not used (e.g. do not have consumers).
            This feature can be used together with the auto-delete
            queue property. The value is expressed in milliseconds (ms).
            Default value is 10 minutes.
            https://www.rabbitmq.com/ttl.html#queue-ttl
        """
        args = {
            'x-max-length': queue_size,
            'x-overflow': overflow_behaviour,
            'x-message-ttl': message_ttl,
            'x-expires': expires
        }

        result = self._channel.queue_declare(
            exclusive=exclusive,
            queue=queue_name,
            durable=False,
            auto_delete=True,
            arguments=args)
        queue_name = result.method.queue
        self.logger.debug('Created queue [{}] [size={}, ttl={}]'.format(
            queue_name, queue_size, message_ttl))
        return queue_name

    def delete_queue(self, queue_name):
        self._channel.queue_delete(queue=queue_name)

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

    def close(self):
        self._graceful_shutdown()

    def __del__(self):
        self._graceful_shutdown()


class AMQPTransportAsync(object):
    CONNECTION_TIMEOUT_SEC = 5

    def __init__(self, host='127.0.0.1', port='5672', exchange='amq.topic'):
        self._connection = None
        self._channel = None
        self._closing = False
        self.logger = create_logger(self.__class__.__name__)
        self._exchange = 'amq.topic'
        self._host = host
        self._port = port
        super(AMQPTransportAsync, self).__init__()

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
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
            stop_ioloop_on_close=False)
        self._connection = connection
        return connection

    def on_connection_open(self, unused_connection):
        """
        This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        self.logger.info('Connection established!')
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

    def on_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.
        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error
        """
        self.logger.info('Connection open failed: %s', err)
        self.reconnect()

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

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.
        IMPLEMENT IN INHERITED CLASSES!!!!!!!!

        :param pika.channel.Channel channel: The channel object

        """
        self.logger.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()


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

    def create_exchange(self, exchange_name, exchange_type, on_declareok):
        """
        Declare/Create an exchange.

        @param exchange_name: The name of the exchange
        @type exchange_name: string

        @param exchange_type: the type of the exchange
        @type exchange_type:
        """
        self.logger.debug('Declaring exchange {} [type={}]', exchange_name,
                exchange_type)
        cb = functools.partial(
            on_declareok, userdata=exchange_name)
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            callback=cb)

    def create_queue(self, queue_name=''):
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

    def set_qos(self, on_ok):
        """This method sets up the consumer prefetch to only be delivered
        one message at a time. The consumer must acknowledge this message
        before RabbitMQ will deliver another one. You should experiment
        with different prefetch values to achieve desired performance.
        """
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=on_ok)

    def __del__(self):
        self._connection.close()
