import json


class RedisUtils:

    @staticmethod
    def make_cache_key(prefix: str, filters: dict) -> str:
        sorted_filters = dict(sorted(filters.items()))
        return f"{prefix}:{json.dumps(sorted_filters, default=str)}"


redis_utils = RedisUtils()