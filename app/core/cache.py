"""_summary_

Returns:
    _type_: _description_
"""
from datetime import datetime, timedelta

class Cache:
    """_summary_

    Returns:
        _type_: _description_
    """
    cache = None
    default_time = None

    def __init__(self, default_time=3):
        """_summary_

        Args:
            default_time (int, optional): _description_. Defaults to 3.
        """
        self.cache = {}
        self.default_time = timedelta(seconds=default_time)

    def hash_key(self, val):
        """_summary_

        Args:
            val (_type_): _description_

        Returns:
            _type_: _description_
        """
        return hash(val)

    def add(self, key, val, timeout=None):
        """_summary_

        Args:
            key (_type_): _description_
            val (_type_): _description_
            timeout (_type_, optional): _description_. Defaults to None.
        """
        expire = datetime.now() + (timedelta(seconds=timeout) if timeout else self.default_time)
        self.cache[self.hash_key(key)] = expire, val

    def get(self, key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        key = self.hash_key(key)
        if key in self.cache:
            if datetime.now() < self.cache[key][0]:
                return self.cache[key][1]
            else:
                self.cache.pop(key)
        return None

local_cache = Cache(60)
