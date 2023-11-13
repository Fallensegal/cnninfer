import dramatiq
from dramatiq.brokers.redis import RedisBroker
from redis import Redis

client = Redis(
    host="localhost", port=6379, decode_responses=True, socket_connect_timeout=0.1
)
broker = RedisBroker(client=client)
dramatiq.set_broker(broker=broker)
