import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from redis import Redis


class Settings(BaseSettings):
    redis_password: SecretStr


settings = Settings()

client = Redis(
    host="chart-redis-master.default.svc.cluster.local",
    password=settings.redis_password.get_secret_value(),
    port=6379,
    decode_responses=False,
    socket_connect_timeout=0.1,
)

result_backend = Results(backend=RedisBackend(client=client))

broker = RedisBroker(client=client)
broker.add_middleware(result_backend)
dramatiq.set_broker(broker=broker)
