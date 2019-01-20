# Examples

## Publish CLI

```bash
./publish_cli.py --help

usage: publish_cli.py [-h] [--hz HZ] [--host HOST] [--port PORT]
                      [--vhost VHOST] [--username USERNAME]
                      [--password PASSWORD] [--debug [DEBUG]]
                      topic

AMQP Publisher CLI.

positional arguments:
  topic                Topic to publish.

optional arguments:
  -h, --help           show this help message and exit
  --hz HZ              Publishing frequency
  --host HOST          AMQP broker host (IP/Hostname)
  --port PORT          AMQP broker listening port
  --vhost VHOST        Virtual host to connect to.
  --username USERNAME  Authentication username
  --password PASSWORD  Authentication password
  --debug [DEBUG]      Enable debugging
```

Example:

```bash
./publish_cli.py dummy --host 155.207.33.185 --hz 2 --debug
```

## Subscribe CLI

```bash
./subscribe_cli.py --help

usage: subscribe_cli.py [-h] [--host HOST] [--port PORT] [--vhost VHOST]
                        [--username USERNAME] [--password PASSWORD]
                        [--queue-size QUEUE_SIZE] [--debug [DEBUG]]
                        topic

AMQP Publisher CLI.

positional arguments:
  topic                 Topic to publish.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           AMQP broker host (IP/Hostname)
  --port PORT           AMQP broker listening port
  --vhost VHOST         Virtual host to connect to.
  --username USERNAME   Authentication username
  --password PASSWORD   Authentication password
  --queue-size QUEUE_SIZE
                        Maximum queue size.
  --debug [DEBUG]       Enable debugging
```

Example:

```bash
./subscribe_cli.py dummy --host 155.207.33.185 --debug
```

## Topic Message Frequency tool

```bash
./hz_measure.py --help

usage: hz_measure.py [-h] [--host HOST] [--port PORT] [--vhost VHOST]
                     [--username USERNAME] [--password PASSWORD]
                     [--queue-size QUEUE_SIZE] [--debug [DEBUG]]
                     topic

AMQP Publisher CLI.

positional arguments:
  topic                 Topic to publish.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           AMQP broker host (IP/Hostname)
  --port PORT           AMQP broker listening port
  --vhost VHOST         Virtual host to connect to.
  --username USERNAME   Authentication username
  --password PASSWORD   Authentication password
  --queue-size QUEUE_SIZE
                        Maximum queue size.
  --debug [DEBUG]       Enable debugging


```

Example:

```bash
./hz_measure.py dummy --host 155.207.33.185 --debug
```
