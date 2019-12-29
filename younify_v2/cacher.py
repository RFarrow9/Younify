from dataclasses import dataclass, field
from typing import Dict
from singleton_decorator import singleton

"""""

Holds the caching object singleton.

This object is responsible for storing and retrieving cache objects. We use a serialised (pickled) list of json objects that
represent the cache.

This caches results of API calls that have been made, along with the complete list of songs by that artist.
"""""


@singleton
@dataclass
class CacheLayer:
    cache: Dict = field(default_factory=dict)
    file: str = None

    def __post_init__(self):
        self.get_cache_from_file()

    def get_cache_from_file(self):
        pass

    def put_cache_in_file(self):
        pass

    def get_artist_cache(self) -> bool:
        return True

    def put_artist_cache(self) -> None:
        pass
