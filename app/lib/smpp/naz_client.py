import json
import naz
import redis
from django.conf import settings
from utils.logging import get_logger
logger = get_logger(__name__)


class RedisOutboundQueue(naz.q.BaseOutboundQueue):
    """
    This implements a basic FIFO queue using redis.

    Basically we use the redis command LPUSH to push messages onto the queue &
    BRPOP to pull them off. (https://redis.io/commands/lpush,
    https://redis.io/commands/brpop)

    Note that in practice, you would probaly want to use a non-blocking redis
    client eg https://github.com/aio-libs/aioredis
    """
    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT):
        self.redis_instance = redis.StrictRedis(
            host=host, port=port, db=0, password=None
        )
        self.queue_name = settings.SMPP_OUTBOUND_QUEUE

    async def enqueue(self, item):
        self.redis_instance.lpush(self.queue_name, json.dumps(item))

    async def dequeue(self):
        val = self.redis_instance.brpop(self.queue_name)
        return json.loads(val[1].decode())


OutboundQueue = RedisOutboundQueue()
