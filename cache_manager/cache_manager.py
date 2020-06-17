import json

import redis

from agregator_ofd.settings.common import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, \
    REDIS_EXPIRES_TIME_IN_SECONDS


class CacheManager:
    """
    Class responsible for cache management
    """

    # TODO: Cache should be done as decorator for each function with expiration time as argument

    def __init__(self):
        self.__cache_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB),
                                          password=REDIS_PASSWORD)

    def get(self, name, identification: str):
        cached_value = self.__cache_client.get(f'{name}_{identification}')
        if cached_value:
            return json.loads(cached_value)
        return None

    def set(self, name, identification: str, serializable_value=None):
        value = json.dumps(serializable_value)
        self.__cache_client.set(name=f'{name}_{identification}', value=value, ex=REDIS_EXPIRES_TIME_IN_SECONDS)
        return True
