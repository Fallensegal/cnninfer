import dramatiq
from dramatiq.brokers.redis import RedisBroker
from redis import Redis

def initialize_redis_broker(redis_client: Redis) -> None:
    redis_broker = RedisBroker(client=redis_client)
    dramatiq.set_broker(redis_broker)