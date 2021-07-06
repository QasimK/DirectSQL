from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    file: str
    schema: dict


@dataclass(frozen=True)
class CachedQuery:
    method: str
    path: str
    name: str
    description: str
    sql: str
    lookup_key: str
    schema: dict
