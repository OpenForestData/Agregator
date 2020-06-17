import inspect
import json

import redis

from agregator_ofd.settings.common import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, \
    REDIS_EXPIRES_TIME_IN_SECONDS
from functools import wraps


# TODO add loggers


class CacheManager:
    """
    Class responsible for cache management
    """

    def __init__(self):
        self.__cache_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB),
                                          password=REDIS_PASSWORD)

    def get(self, name: str):
        cached_value = self.__cache_client.get(f'{name}')
        if cached_value:
            return json.loads(cached_value)
        return None

    def set(self, name: str, serializable_value=None, expires=REDIS_EXPIRES_TIME_IN_SECONDS):
        value = json.dumps(serializable_value)
        self.__cache_client.set(name=f'{name}', value=value, ex=expires)
        return True


def cached(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_manager = CacheManager()

        #TODO based on signature check if self is
        key_parts = [func.__module__, args[0].__class__.__name__, func.__name__] + list(args[1:])
        key = '-'.join(key_parts)
        result = cache_manager.get(key)

        if result is None:
            value = func(*args, **kwargs)
            cache_manager.set(key, value, expires=REDIS_EXPIRES_TIME_IN_SECONDS)
        else:
            value = result

        return value

    return wrapper
