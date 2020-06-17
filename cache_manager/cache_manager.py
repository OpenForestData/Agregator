import json

import redis

from agregator_ofd.settings.common import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD


class CacheManager:
    """
    Class responsible for cache management
    """

    # TODO: Cache should be done as decorator for each function of repository

    def __init__(self):
        self.__cache_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB),
                                          password=REDIS_PASSWORD)

    def __save_to_cache(self, identifier: str, value: str) -> bool:
        return True

    def __get_from_cache(self, identifiers: list) -> str:
        return ""

    def get(self, name, identification: str):
        cached_value = self.__cache_client.hget(name, identification)
        if cached_value:
            return json.loads(cached_value)
        return None

    def set(self, name, identification: str, serializable_value=None):
        value = json.dumps(serializable_value)
        self.__cache_client.hset(name, key=identification, value=value)
        return True
