#!/usr/bin/env python3
from typing import Any, Optional
from collections import OrderedDict

class LRUCache:
    """
    A Least Recently Used (LRU) cache keeps items in the cache until it reaches its size
    and/or item limit (only item in our case). In which case, it removes an item that was accessed
    least recently.
    An item is considered accessed whenever `has`, `get`, or `set` is called with its key.

    Implement the LRU cache here and use the unit tests to check your implementation.
    """

    def __init__(self, item_limit: int):
        # TODO: implement this function
        # try:
        # if item_limit <=0:
        #     raise ValueError("Capacity must be greater than 0")
        self.cache = OrderedDict()
        self.item_limit = item_limit
        # except:
        #     raise NotImplementedError()

    def has(self, key: str) -> bool:
        # TODO: implement this function
            if key in self.cache:
                self.cache.move_to_end(key)
                return True
            return False
        # except:
        #     raise NotImplementedError()

    def get(self, key: str) -> Optional[Any]:
        # TODO: implement this function
        # try:
        if key not in self.cache:
            return None
        
        self.cache.move_to_end(key)
        return self.cache[key]
        # except:
        #     raise NotImplementedError()

    def set(self, key: str, value: Any):
        # TODO: implement this function
        # try:
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.item_limit:
            self.cache.popitem(last=False)
        # except:
        #     raise NotImplementedError()
