from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class Query:
    file: str
    schema: dict
    param_mappings: list
    last_modified: Optional[Callable] = None


@dataclass(frozen=True)
class CachedQuery:
    method: str
    path: str
    name: str
    description: str
    sql: str
    lookup_key: str
    schema: dict
    param_mappings: list
    last_modified: Optional[Callable] = None
