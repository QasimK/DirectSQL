from pathlib import Path
from functools import partial
import logging
import urllib.parse
from email.utils import formatdate

from directsql import types
from directsql import converters
from directsql.openapi import generate_openapi_yaml

logger = logging.getLogger(__name__)


def application(env, start_response, cache, executor):
    lookup_name = f'{env["REQUEST_METHOD"]} {env["PATH_INFO"]}'
    cached_query = cache.get(lookup_name)
    if not cached_query:
        logger.debug("404: %s. Have %s", lookup_name, cache)
        start_response("404 NOT FOUND", [("Content-Type", "text/html")])
        return [b"404 URL NOT FOUND"]
    params = urllib.parse.parse_qs(env["QUERY_STRING"])

    final_params = {}
    for key, values in params.items():
        validator = cached_query.schema.get(key)
        if validator:
            # TODO: Convert env into headers
            final_params[key] = validator(key, values, env)
        else:
            final_params[key] = str(values)

    date = formatdate(timeval=None, localtime=False, usegmt=True)
    rows = executor(cached_query.sql, final_params)
    result, encoding = converters.convert(rows, env.get("HTTP_ACCEPT"))
    length = len(result)

    start_response(
        "200 OK",
        [
            ("Content-Length", str(length)),
            ("Content-Type", encoding),
            ("Date", date),
        ],
    )
    return [result]


def create_application(base: Path, queries, executor):
    cache = _build_cache(base, queries)
    with open("spec.yaml", "w") as fout:
        fout.write(generate_openapi_yaml(list(cache.values())))
    return partial(application, cache=cache, executor=executor)


def _build_cache(base: Path, queries):
    result = {}
    for query in queries:
        cached_query = _parse_query_file(base, query)
        result[cached_query.lookup_key] = cached_query

    return result


def _parse_query_file(base: Path, query: types.Query) -> types.CachedQuery:
    prefix_path, sep, other = str(query.file).rpartition("/")
    method, _, name = other.partition("_")
    method = method.rstrip(".md").upper()
    path = prefix_path + sep + name.replace("_", "-").rstrip(".md")

    content = (base / query.file).read_text()

    name = content.partition("\n")[0].lstrip(" #")
    description = content.partition("\n")[2].partition("```sql")[0].strip()
    sql = content.partition("```sql")[2].partition("```")[0].strip()

    return types.CachedQuery(
        method=method,
        path=path,
        name=name,
        description=description,
        sql=sql,
        lookup_key=f"{method} /{path}",
        schema=query.schema,
    )
