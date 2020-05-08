[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d0a18bbcbc964af0871f55608a3b5b20)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=robotics-4-all/amqp-common-python&amp;utm_campaign=Badge_Grade)

# amqp-common-python
Higher-level features for AMQP, such as PubSub and RPC (server-client).
Thing wrapper around [pika](https://pika.readthedocs.io/en/stable/).

**ATTENTION**: Works with pika==1.1.0

# Installation


```bash
python setup.py install
```

or

```bash
pip install . --user
```


# RPC Client

In case of `RpcClient`, if the thread where it was created is blocked, then
heartbeats wont be sent, leading to a connection drop from the broker.

To avoid that, make sure you either invoke `call` or use the `process_amqp_events`
member method to explicitly sent heartbeat messages within a `heartbeat_timeout`
interval.


## Usage

```python
import time

from amqp_common import ConnectionParameters, RpcClient, Credentials


if __name__ == "__main__":

    conn_params = ConnectionParameters()
    conn_params.credentials = Credentials('bot', 'bot')

    rpc_client = RpcClient('test_rpc)',
                           connection_params=conn_params)
    data = {}
    print('Calling RPC...')
    resp = rpc_client.call(data, timeout=30)
    print('Response: {}'.format(response))

```

# Examples

Look at the `examples` folder as it ncludes various examples.
