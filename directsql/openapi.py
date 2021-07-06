"""Generate an OpenAPI specification.

Override anything you want using the dict representation.
"""
from directsql import types
import yaml


def generate_openapi_yaml(cached_queries) -> str:
    """Return an OpenAPI specification as a string."""
    return yaml.dump(generate_openapi_dict(cached_queries))


def generate_openapi_dict(cached_queries) -> dict:
    """Return a dict that can be dumped as a YAML OpenAPI specification."""
    path_dicts = [_get_paths_dict(cached_query) for cached_query in cached_queries]
    paths = {}
    for data in path_dicts:
        for path, path_data in data.items():
            for method, method_data in path_data.items():
                paths_path_data = paths.setdefault(path, {})
                paths_path_data[method] = method_data

    return {
        "openapi": "3.0.3",
        "info": {
            "title": "DirectSQL REST API",
            "version": "1.0",
        },
        "paths": paths,
    }


def _get_paths_dict(cached_query: types.CachedQuery) -> dict:
    return {
        f"/{cached_query.path}": {
            cached_query.method.lower(): {
                "parameters": [],
                "operationId": _camel_case(cached_query.name),
                "summary": cached_query.name,
                "description": cached_query.description,
                "responses": {
                    "200": {
                        "description": "200 OK",
                        "content": {
                            "text/tsv": {},
                            "text/csv": {},
                            "application/json": {},
                        },
                    }
                },
            }
        },
    }


def _camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + "".join(i.capitalize() for i in s[1:])
