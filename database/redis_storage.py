from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from core.config import settings

def get_redis_storage():
    """Инициализация Redis storage для FSM"""
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return RedisStorage(redis=redis)