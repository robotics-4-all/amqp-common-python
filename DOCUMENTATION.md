[Top](#){#top}
<div id="container">

<div id="sidebar">

Index
=====

-   ### [Classes](#header-classes)

    -   <span
        class="class_name">[ConnectionParameters](#amqp_common.ConnectionParameters)</span>
        -   [\_\_init\_\_](#amqp_common.ConnectionParameters.__init__)
    -   <span
        class="class_name">[Credentials](#amqp_common.Credentials)</span>
        -   [\_\_init\_\_](#amqp_common.Credentials.__init__)
    -   <span
        class="class_name">[PublisherSync](#amqp_common.PublisherSync)</span>
        -   [\_\_init\_\_](#amqp_common.PublisherSync.__init__)
        -   [bind\_queue](#amqp_common.PublisherSync.bind_queue)
        -   [connect](#amqp_common.PublisherSync.connect)
        -   [create\_queue](#amqp_common.PublisherSync.create_queue)
        -   [pub\_loop](#amqp_common.PublisherSync.pub_loop)
        -   [publish](#amqp_common.PublisherSync.publish)
        -   [setup\_exchange](#amqp_common.PublisherSync.setup_exchange)
    -   <span
        class="class_name">[RpcClient](#amqp_common.RpcClient)</span>
        -   [\_\_init\_\_](#amqp_common.RpcClient.__init__)
        -   [bind\_queue](#amqp_common.RpcClient.bind_queue)
        -   [call](#amqp_common.RpcClient.call)
        -   [connect](#amqp_common.RpcClient.connect)
        -   [create\_queue](#amqp_common.RpcClient.create_queue)
        -   [gen\_corr\_id](#amqp_common.RpcClient.gen_corr_id)
        -   [setup\_exchange](#amqp_common.RpcClient.setup_exchange)
    -   <span
        class="class_name">[RpcServer](#amqp_common.RpcServer)</span>
        -   [\_\_init\_\_](#amqp_common.RpcServer.__init__)
        -   [bind\_queue](#amqp_common.RpcServer.bind_queue)
        -   [connect](#amqp_common.RpcServer.connect)
        -   [create\_queue](#amqp_common.RpcServer.create_queue)
        -   [run](#amqp_common.RpcServer.run)
        -   [run\_threaded](#amqp_common.RpcServer.run_threaded)
        -   [setup\_exchange](#amqp_common.RpcServer.setup_exchange)
    -   <span
        class="class_name">[SubscriberSync](#amqp_common.SubscriberSync)</span>
        -   [\_\_init\_\_](#amqp_common.SubscriberSync.__init__)
        -   [bind\_queue](#amqp_common.SubscriberSync.bind_queue)
        -   [connect](#amqp_common.SubscriberSync.connect)
        -   [create\_queue](#amqp_common.SubscriberSync.create_queue)
        -   [run](#amqp_common.SubscriberSync.run)
        -   [run\_threaded](#amqp_common.SubscriberSync.run_threaded)
        -   [setup\_exchange](#amqp_common.SubscriberSync.setup_exchange)

</div>

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common" class="source">

<div class="codehilite">

    from __future__ import absolute_import


    from .publisher import PublisherSync
    from .subscriber import SubscriberSync
    from .rpc_client import RpcClient
    from .rpc_server import RpcServer
    from .broker_interface import Credentials, ConnectionParameters

    __all__ = [
        'PublisherSync',
        'SubscriberSync',
        'RpcClient',
        'RpcServer',
        'Credentials',
        'ConnectionParameters'
    ]

</div>

</div>

<div id="section-items" class="section">

Classes {#header-classes .section-title}
-------

<div class="item">

class <span class="ident">ConnectionParameters</span>

<div class="desc">

AMQP Connection parameters.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.ConnectionParameters" class="source">

<div class="codehilite">

    class ConnectionParameters(object):
        """AMQP Connection parameters."""

        def __init__(self,
                     host='127.0.0.1',
                     port='5672',
                     secure=False,
                     vhost='/',
                     reconnect_attempts=5,
                     retry_delay=2.0,
                     timeout=10.0):
            """
            Constructor.

            @param host: Hostname of AMQP broker
            @type host: string

            @param port: AMQP broker listening port
            @type port: string

            @param secure: Enable SSL/TLS - AMQPS
            @type secure: boolean
            """
            self.host = host
            self.port = port
            self.secure = secure
            self.vhost = vhost
            self.reconnect_attempts = reconnect_attempts
            self.retry_delay = retry_delay
            self.timeout = timeout

</div>

</div>

</div>

<div class="class">

### Ancestors (in MRO)

-   [ConnectionParameters](#amqp_common.ConnectionParameters)
-   \_\_builtin\_\_.object

### Instance variables

<div class="item">

var <span class="ident">host</span>

<div class="source_cont">

</div>

</div>

<div class="item">

var <span class="ident">port</span>

<div class="source_cont">

</div>

</div>

<div class="item">

var <span class="ident">reconnect\_attempts</span>

<div class="source_cont">

</div>

</div>

<div class="item">

var <span class="ident">retry\_delay</span>

<div class="source_cont">

</div>

</div>

<div class="item">

var <span class="ident">secure</span>

<div class="source_cont">

</div>

</div>

<div class="item">

var <span class="ident">timeout</span>

<div class="source_cont">

</div>

</div>

<div class="item">

var <span class="ident">vhost</span>

<div class="source_cont">

</div>

</div>

### Methods

<div class="item">

<div id="amqp_common.ConnectionParameters.__init__" class="name def">

def <span class="ident">\_\_init\_\_</span>(

self, host='127.0.0.1', port='5672', secure=False, vhost='/',
reconnect\_attempts=5, retry\_delay=2.0, timeout=10.0)

</div>

<div class="desc">

Constructor.

@param host: Hostname of AMQP broker @type host: string

@param port: AMQP broker listening port @type port: string

@param secure: Enable SSL/TLS - AMQPS @type secure: boolean

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.ConnectionParameters.__init__"
class="source">

<div class="codehilite">

    def __init__(self,
                 host='127.0.0.1',
                 port='5672',
                 secure=False,
                 vhost='/',
                 reconnect_attempts=5,
                 retry_delay=2.0,
                 timeout=10.0):
        """
        Constructor.
        @param host: Hostname of AMQP broker
        @type host: string
        @param port: AMQP broker listening port
        @type port: string
        @param secure: Enable SSL/TLS - AMQPS
        @type secure: boolean
        """
        self.host = host
        self.port = port
        self.secure = secure
        self.vhost = vhost
        self.reconnect_attempts = reconnect_attempts
        self.retry_delay = retry_delay
        self.timeout = timeout

</div>

</div>

</div>

</div>

</div>

</div>

<div class="item">

class <span class="ident">Credentials</span>

<div class="desc">

Connection credentials for authn/authz.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.Credentials" class="source">

<div class="codehilite">

    class Credentials(object):
        """Connection credentials for authn/authz."""

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

</div>

</div>

</div>

<div class="class">

### Ancestors (in MRO)

-   [Credentials](#amqp_common.Credentials)
-   \_\_builtin\_\_.object

### Instance variables

<div class="item">

var <span class="ident">password</span>

<div class="source_cont">

</div>

</div>

<div class="item">

var <span class="ident">username</span>

<div class="source_cont">

</div>

</div>

### Methods

<div class="item">

<div id="amqp_common.Credentials.__init__" class="name def">

def <span class="ident">\_\_init\_\_</span>(

self, username='guest', password='guest')

</div>

<div class="desc">

Constructor.

@param username: Client username to login @type username: string

@param password: Client password @type password: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.Credentials.__init__" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

</div>

</div>

<div class="item">

class <span class="ident">PublisherSync</span>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync" class="source">

<div class="codehilite">

    class PublisherSync(BrokerInterfaceSync):

        def __init__(self, topic, exchange='amq.topic', *args, **kwargs):
            """
            Constructor.

            @param topic: Topic name to publish
            @type topic: string

            """
            BrokerInterfaceSync.__init__(self, *args, **kwargs)
            self._topic_exchange = exchange
            self._topic = topic
            self.connect()
            self.setup_exchange(self._topic_exchange, ExchangeTypes.Topic)

        def publish(self, msg):
            self.logger.debug('[x] - Sent %r:%r' % (self._topic, msg))
            self._channel.basic_publish(exchange=self._topic_exchange,
                                        routing_key=self._topic,
                                        body=self._serialize_data(msg))

        def pub_loop(self, data_bind, hz):
            self._rate = Rate(hz)
            while True:
                try:
                    self.publish(data_bind)
                    self._rate.sleep()
                except KeyboardInterrupt as exc:
                    print(exc)
                    break

        def _serialize_data(self, data):
            """
            TODO: Make Class. Allow different implementation of serialization
                classes.
            """
            return json.dumps(data)

</div>

</div>

</div>

<div class="class">

### Ancestors (in MRO)

-   [PublisherSync](#amqp_common.PublisherSync)
-   amqp\_common.broker\_interface.BrokerInterfaceSync
-   \_\_builtin\_\_.object

### Methods

<div class="item">

<div id="amqp_common.PublisherSync.__init__" class="name def">

def <span class="ident">\_\_init\_\_</span>(

self, topic, exchange='amq.topic', \*args, \*\*kwargs)

</div>

<div class="desc">

Constructor.

@param topic: Topic name to publish @type topic: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync.__init__" class="source">

<div class="codehilite">

    def __init__(self, topic, exchange='amq.topic', *args, **kwargs):
        """
        Constructor.
        @param topic: Topic name to publish
        @type topic: string
        """
        BrokerInterfaceSync.__init__(self, *args, **kwargs)
        self._topic_exchange = exchange
        self._topic = topic
        self.connect()
        self.setup_exchange(self._topic_exchange, ExchangeTypes.Topic)

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.PublisherSync.bind_queue" class="name def">

def <span class="ident">bind\_queue</span>(

self, exchange\_name, queue\_name, bind\_key)

</div>

<div class="desc">

Bind a queue to and exchange using a bind-key.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param queue\_name: The name of the queue. @type queue\_name: string

@param bind\_key: The binding key name. @type bind\_key: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync.bind_queue" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.PublisherSync.connect" class="name def">

def <span class="ident">connect</span>(

self)

</div>

<div class="desc">

Connect to the AMQP broker.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync.connect" class="source">

<div class="codehilite">

    def connect(self):
        """Connect to the AMQP broker."""
        host = self.connection_params.host
        port = self.connection_params.port
        vhost = self.connection_params.vhost
        reconnect_attempts = self.connection_params.reconnect_attempts
        timeout = self.connection_params.timeout
        retry_delay = self.connection_params.retry_delay
        secure = self.connection_params.secure
        self._connect_params = pika.ConnectionParameters(
            host=host, port=port,
            credentials=self._creds_pika,
            connection_attempts=reconnect_attempts,
            retry_delay=retry_delay,
            blocked_connection_timeout=timeout,
            socket_timeout=timeout
        )
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
        return True

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.PublisherSync.create_queue" class="name def">

def <span class="ident">create\_queue</span>(

self, queue\_name='', exclusive=True)

</div>

<div class="desc">

Create a new queue.

@param queue\_name: The name of the queue. @type queue\_name: string

@param exclusive: Only allow access by the current connection. @type
exclusive: bool

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync.create_queue" class="source">

<div class="codehilite">

    def create_queue(self, queue_name='', exclusive=True):
        """
        Create a new queue.
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
        self.logger.info('Created queue [{}]'.format(queue_name))
        return queue_name

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.PublisherSync.pub_loop" class="name def">

def <span class="ident">pub\_loop</span>(

self, data\_bind, hz)

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync.pub_loop" class="source">

<div class="codehilite">

    def pub_loop(self, data_bind, hz):
        self._rate = Rate(hz)
        while True:
            try:
                self.publish(data_bind)
                self._rate.sleep()
            except KeyboardInterrupt as exc:
                print(exc)
                break

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.PublisherSync.publish" class="name def">

def <span class="ident">publish</span>(

self, msg)

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync.publish" class="source">

<div class="codehilite">

    def publish(self, msg):
        self.logger.debug('[x] - Sent %r:%r' % (self._topic, msg))
        self._channel.basic_publish(exchange=self._topic_exchange,
                                    routing_key=self._topic,
                                    body=self._serialize_data(msg))

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.PublisherSync.setup_exchange" class="name def">

def <span class="ident">setup\_exchange</span>(

self, exchange\_name, exchange\_type)

</div>

<div class="desc">

Create a new exchange.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param exchange\_type: The type of the exchange (e.g. 'topic'). @type
exchange\_type: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.PublisherSync.setup_exchange"
class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

</div>

</div>

<div class="item">

class <span class="ident">RpcClient</span>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient" class="source">

<div class="codehilite">

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
            self._exchange = ExchangeTypes.Default

            self._channel.basic_consume(self._on_response,
                                        no_ack=True,
                                        queue='amq.rabbitmq.reply-to')

        def _on_response(self, ch, method, props, body):
            """Handle on-response event."""
            self.logger.debug('Received Request:' +
                              '\n- [*] Method: %s' +
                              '\n- [*] Properties: %s' +
                              '\n- [*] Channel: %s', method,
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

</div>

</div>

</div>

<div class="class">

### Ancestors (in MRO)

-   [RpcClient](#amqp_common.RpcClient)
-   amqp\_common.broker\_interface.BrokerInterfaceSync
-   \_\_builtin\_\_.object

### Methods

<div class="item">

<div id="amqp_common.RpcClient.__init__" class="name def">

def <span class="ident">\_\_init\_\_</span>(

self, rpc\_name, \*args, \*\*kwargs)

</div>

<div class="desc">

Constructor.

@param rpc\_name: The name of the RPC @type rpc\_name: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient.__init__" class="source">

<div class="codehilite">

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
        self._exchange = ExchangeTypes.Default
        self._channel.basic_consume(self._on_response,
                                    no_ack=True,
                                    queue='amq.rabbitmq.reply-to')

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcClient.bind_queue" class="name def">

def <span class="ident">bind\_queue</span>(

self, exchange\_name, queue\_name, bind\_key)

</div>

<div class="desc">

Bind a queue to and exchange using a bind-key.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param queue\_name: The name of the queue. @type queue\_name: string

@param bind\_key: The binding key name. @type bind\_key: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient.bind_queue" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcClient.call" class="name def">

def <span class="ident">call</span>(

self, msg, background=False, immediate=False, timeout=5.0)

</div>

<div class="desc">

Call RPC.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient.call" class="source">

<div class="codehilite">

    def call(self, msg, background=False, immediate=False, timeout=5.0):
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

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcClient.connect" class="name def">

def <span class="ident">connect</span>(

self)

</div>

<div class="desc">

Connect to the AMQP broker.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient.connect" class="source">

<div class="codehilite">

    def connect(self):
        """Connect to the AMQP broker."""
        host = self.connection_params.host
        port = self.connection_params.port
        vhost = self.connection_params.vhost
        reconnect_attempts = self.connection_params.reconnect_attempts
        timeout = self.connection_params.timeout
        retry_delay = self.connection_params.retry_delay
        secure = self.connection_params.secure
        self._connect_params = pika.ConnectionParameters(
            host=host, port=port,
            credentials=self._creds_pika,
            connection_attempts=reconnect_attempts,
            retry_delay=retry_delay,
            blocked_connection_timeout=timeout,
            socket_timeout=timeout
        )
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
        return True

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcClient.create_queue" class="name def">

def <span class="ident">create\_queue</span>(

self, queue\_name='', exclusive=True)

</div>

<div class="desc">

Create a new queue.

@param queue\_name: The name of the queue. @type queue\_name: string

@param exclusive: Only allow access by the current connection. @type
exclusive: bool

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient.create_queue" class="source">

<div class="codehilite">

    def create_queue(self, queue_name='', exclusive=True):
        """
        Create a new queue.
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
        self.logger.info('Created queue [{}]'.format(queue_name))
        return queue_name

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcClient.gen_corr_id" class="name def">

def <span class="ident">gen\_corr\_id</span>(

self)

</div>

<div class="desc">

Generate correlationID.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient.gen_corr_id" class="source">

<div class="codehilite">

    def gen_corr_id(self):
        """Generate correlationID."""
        return str(uuid.uuid4())

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcClient.setup_exchange" class="name def">

def <span class="ident">setup\_exchange</span>(

self, exchange\_name, exchange\_type)

</div>

<div class="desc">

Create a new exchange.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param exchange\_type: The type of the exchange (e.g. 'topic'). @type
exchange\_type: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcClient.setup_exchange" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

</div>

</div>

<div class="item">

class <span class="ident">RpcServer</span>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer" class="source">

<div class="codehilite">

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
            """."""
            self._channel.basic_consume(self._on_request_wrapper,
                                        queue=self._rpc_queue)
            self.logger.info('[x] - Awaiting RPC requests')
            self._channel.start_consuming()

        def run_threaded(self):
            """Run RPC Server in a separate thread."""
            self.loop_thread = Thread(target=self.run)
            self.loop_thread.daemon = True
            self.loop_thread.start()

        def _on_request_wrapper(self, ch, method, properties, body):
            self.logger.debug('Received Request:' +
                              '\n- [*] Method: %s' +
                              '\n- [*] Properties: %s' +
                              '\n- [*] Channel: %s', method,
                              properties, ch)
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
            pub_props = pika.BasicProperties(
                correlation_id=properties.correlation_id)
            ch.basic_publish(exchange=self._exchange,
                             routing_key=properties.reply_to,
                             properties=pub_props,
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

</div>

</div>

</div>

<div class="class">

### Ancestors (in MRO)

-   [RpcServer](#amqp_common.RpcServer)
-   amqp\_common.broker\_interface.BrokerInterfaceSync
-   \_\_builtin\_\_.object

### Instance variables

<div class="item">

var <span class="ident">on\_request</span>

<div class="source_cont">

</div>

</div>

### Methods

<div class="item">

<div id="amqp_common.RpcServer.__init__" class="name def">

def <span class="ident">\_\_init\_\_</span>(

self, rpc\_name, exchange='', on\_request=None, \*args, \*\*kwargs)

</div>

<div class="desc">

Constructor.

@param rpc\_name: The name of the RPC @type rpc\_name: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer.__init__" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcServer.bind_queue" class="name def">

def <span class="ident">bind\_queue</span>(

self, exchange\_name, queue\_name, bind\_key)

</div>

<div class="desc">

Bind a queue to and exchange using a bind-key.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param queue\_name: The name of the queue. @type queue\_name: string

@param bind\_key: The binding key name. @type bind\_key: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer.bind_queue" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcServer.connect" class="name def">

def <span class="ident">connect</span>(

self)

</div>

<div class="desc">

Connect to the AMQP broker.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer.connect" class="source">

<div class="codehilite">

    def connect(self):
        """Connect to the AMQP broker."""
        host = self.connection_params.host
        port = self.connection_params.port
        vhost = self.connection_params.vhost
        reconnect_attempts = self.connection_params.reconnect_attempts
        timeout = self.connection_params.timeout
        retry_delay = self.connection_params.retry_delay
        secure = self.connection_params.secure
        self._connect_params = pika.ConnectionParameters(
            host=host, port=port,
            credentials=self._creds_pika,
            connection_attempts=reconnect_attempts,
            retry_delay=retry_delay,
            blocked_connection_timeout=timeout,
            socket_timeout=timeout
        )
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
        return True

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcServer.create_queue" class="name def">

def <span class="ident">create\_queue</span>(

self, queue\_name='', exclusive=True)

</div>

<div class="desc">

Create a new queue.

@param queue\_name: The name of the queue. @type queue\_name: string

@param exclusive: Only allow access by the current connection. @type
exclusive: bool

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer.create_queue" class="source">

<div class="codehilite">

    def create_queue(self, queue_name='', exclusive=True):
        """
        Create a new queue.
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
        self.logger.info('Created queue [{}]'.format(queue_name))
        return queue_name

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcServer.run" class="name def">

def <span class="ident">run</span>(

self)

</div>

<div class="desc">

.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer.run" class="source">

<div class="codehilite">

    def run(self):
        """."""
        self._channel.basic_consume(self._on_request_wrapper,
                                    queue=self._rpc_queue)
        self.logger.info('[x] - Awaiting RPC requests')
        self._channel.start_consuming()

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcServer.run_threaded" class="name def">

def <span class="ident">run\_threaded</span>(

self)

</div>

<div class="desc">

Run RPC Server in a separate thread.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer.run_threaded" class="source">

<div class="codehilite">

    def run_threaded(self):
        """Run RPC Server in a separate thread."""
        self.loop_thread = Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.RpcServer.setup_exchange" class="name def">

def <span class="ident">setup\_exchange</span>(

self, exchange\_name, exchange\_type)

</div>

<div class="desc">

Create a new exchange.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param exchange\_type: The type of the exchange (e.g. 'topic'). @type
exchange\_type: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.RpcServer.setup_exchange" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

</div>

</div>

<div class="item">

class <span class="ident">SubscriberSync</span>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync" class="source">

<div class="codehilite">

    class SubscriberSync(BrokerInterfaceSync):

        def __init__(self, topic, on_message=None, exchange='amq.topic',
                     *args, **kwargs):
            """
            TODO!!

            @param connection_params: AMQP Connection Parameters
            @type connection_params: ConnectionParameters
            """
            BrokerInterfaceSync.__init__(self, *args, **kwargs)
            self._topic = topic
            self._topic_exchange = exchange
            self._queue_name = None
            self.connect()
            self.on_msg_callback = on_message
            self.setup_exchange(self._topic_exchange, ExchangeTypes.Topic)
            # Create a queue
            self._queue_name = self.create_queue()
            # Bind queue to the Topic exchange
            self.bind_queue(self._topic_exchange, self._queue_name,
                            self._topic)

        def run(self, callback=None):
            """
            TODO!!
            """
            if callback is not None:
                self._callback = callback
            # Start loop
            self._consume()

        def run_threaded(self):
            self.loop_thread = Thread(target=self.run)
            self.loop_thread.daemon = True
            self.loop_thread.start()

        def _consume(self):
            """
            TODO!!
            """
            self._channel.basic_consume(self._on_msg_callback_wrapper,
                                        queue=self._queue_name,
                                        no_ack=True)
            try:
                self._channel.start_consuming()
            except KeyboardInterrupt as exc:
                print(exc)

        def _on_msg_callback_wrapper(self, ch, method, properties, body):
            msg = self._deserialize_data(body)
            self.logger.debug("[x] Received data - %r:%r" % (method.routing_key, msg))
            if self.on_msg_callback is not None:
                meta = {
                    'channel': ch,
                    'method': method,
                    'properties': properties
                }
                self.on_msg_callback(msg, meta)

        def _deserialize_data(self, data):
            """
            DeSerialize data.
            TODO: Make class. ALlow for different implementations.

            @param data: Data to deserialize.
            @type data: dict|int|bool
            """
            return json.loads(data)

</div>

</div>

</div>

<div class="class">

### Ancestors (in MRO)

-   [SubscriberSync](#amqp_common.SubscriberSync)
-   amqp\_common.broker\_interface.BrokerInterfaceSync
-   \_\_builtin\_\_.object

### Instance variables

<div class="item">

var <span class="ident">on\_msg\_callback</span>

<div class="source_cont">

</div>

</div>

### Methods

<div class="item">

<div id="amqp_common.SubscriberSync.__init__" class="name def">

def <span class="ident">\_\_init\_\_</span>(

self, topic, on\_message=None, exchange='amq.topic', \*args, \*\*kwargs)

</div>

<div class="desc">

TODO!!

@param connection\_params: AMQP Connection Parameters @type
connection\_params: ConnectionParameters

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync.__init__" class="source">

<div class="codehilite">

    def __init__(self, topic, on_message=None, exchange='amq.topic',
                 *args, **kwargs):
        """
        TODO!!
        @param connection_params: AMQP Connection Parameters
        @type connection_params: ConnectionParameters
        """
        BrokerInterfaceSync.__init__(self, *args, **kwargs)
        self._topic = topic
        self._topic_exchange = exchange
        self._queue_name = None
        self.connect()
        self.on_msg_callback = on_message
        self.setup_exchange(self._topic_exchange, ExchangeTypes.Topic)
        # Create a queue
        self._queue_name = self.create_queue()
        # Bind queue to the Topic exchange
        self.bind_queue(self._topic_exchange, self._queue_name,
                        self._topic)

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.SubscriberSync.bind_queue" class="name def">

def <span class="ident">bind\_queue</span>(

self, exchange\_name, queue\_name, bind\_key)

</div>

<div class="desc">

Bind a queue to and exchange using a bind-key.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param queue\_name: The name of the queue. @type queue\_name: string

@param bind\_key: The binding key name. @type bind\_key: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync.bind_queue" class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.SubscriberSync.connect" class="name def">

def <span class="ident">connect</span>(

self)

</div>

<div class="desc">

Connect to the AMQP broker.

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync.connect" class="source">

<div class="codehilite">

    def connect(self):
        """Connect to the AMQP broker."""
        host = self.connection_params.host
        port = self.connection_params.port
        vhost = self.connection_params.vhost
        reconnect_attempts = self.connection_params.reconnect_attempts
        timeout = self.connection_params.timeout
        retry_delay = self.connection_params.retry_delay
        secure = self.connection_params.secure
        self._connect_params = pika.ConnectionParameters(
            host=host, port=port,
            credentials=self._creds_pika,
            connection_attempts=reconnect_attempts,
            retry_delay=retry_delay,
            blocked_connection_timeout=timeout,
            socket_timeout=timeout
        )
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
        return True

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.SubscriberSync.create_queue" class="name def">

def <span class="ident">create\_queue</span>(

self, queue\_name='', exclusive=True)

</div>

<div class="desc">

Create a new queue.

@param queue\_name: The name of the queue. @type queue\_name: string

@param exclusive: Only allow access by the current connection. @type
exclusive: bool

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync.create_queue" class="source">

<div class="codehilite">

    def create_queue(self, queue_name='', exclusive=True):
        """
        Create a new queue.
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
        self.logger.info('Created queue [{}]'.format(queue_name))
        return queue_name

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.SubscriberSync.run" class="name def">

def <span class="ident">run</span>(

self, callback=None)

</div>

<div class="desc">

TODO!!

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync.run" class="source">

<div class="codehilite">

    def run(self, callback=None):
        """
        TODO!!
        """
        if callback is not None:
            self._callback = callback
        # Start loop
        self._consume()

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.SubscriberSync.run_threaded" class="name def">

def <span class="ident">run\_threaded</span>(

self)

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync.run_threaded" class="source">

<div class="codehilite">

    def run_threaded(self):
        self.loop_thread = Thread(target=self.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()

</div>

</div>

</div>

</div>

<div class="item">

<div id="amqp_common.SubscriberSync.setup_exchange" class="name def">

def <span class="ident">setup\_exchange</span>(

self, exchange\_name, exchange\_type)

</div>

<div class="desc">

Create a new exchange.

@param exchange\_name: The name of the exchange (e.g. com.logging).
@type exchange\_name: string

@param exchange\_type: The type of the exchange (e.g. 'topic'). @type
exchange\_type: string

</div>

<div class="source_cont">

[Show source ≡](javascript:void(0);)

<div id="source-amqp_common.SubscriberSync.setup_exchange"
class="source">

<div class="codehilite">

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

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="clear">

</div>

Documentation generated by [pdoc
0.3.2](https://github.com/BurntSushi/pdoc)

pdoc is in the public domain with the [UNLICENSE](http://unlicense.org)

Design by [Kailash Nadh](http://nadh.in)

</div>
