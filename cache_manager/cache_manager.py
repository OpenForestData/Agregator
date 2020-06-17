import json

import redis

from agregator_ofd.settings.common import REDIS_HOST, REDIS_PORT, REDIS_DB


class CacheManager:
    """
    Class responsible for cache management
    """

    def __init__(self):
        self.__cache_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def __save_to_cache(self, identifier: str, value: str) -> bool:
        return True

    def __get_from_cache(self, identifiers: list) -> str:
        return ""

    def get(self, name, identification: str):
        return None

    def set(self, name, identification: str, serializable_value=None):
        value = json.dumps(serializable_value)
        self.__cache_client.hset(name, key=identification, value=value)
        return True
