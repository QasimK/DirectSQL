from email.utils import formatdate, format_datetime
from functools import partial
from pathlib import Path
import logging
import urllib.parse

from directsql import types
from directsql import converters
from directsql.openapi import generate_openapi_yaml

logger = logging.getLogger(__name__)


def application(env, start_response, cache, executor):
    lookup_name = f'{env["REQUEST_METHOD"]} {env["PATH_INFO"]}'
    cached_query = cache.get(lookup_name)
    if not cached_query:
        logger.debug("404: %s. Have %s", lookup_name, cache)
        print(cache)
        start_response("404 NOT FOUND", [("Content-Type", "text/html")])
        return [b"404 URL NOT FOUND"]

    query_params = urllib.parse.parse_qs(env["QUERY_STRING"])
    headers = {key[5:]: value for key, value in env.items() if key.startswith("HTTP_")}

    output_params = {}
    for key, validator in cached_query.schema.items():
        output_params[key] = validator(query_params, headers)[1]

    for param_mapping in cached_query.param_mappings:
        new_params = param_mapping(query_params, headers)
        output_params.update(new_params)

    date = formatdate(timeval=None, localtime=False, usegmt=True)
    rows = executor(cached_query.sql, output_params)

    if not rows:
        start_response("204 NO CONTENT", [])
        return [b""]

    last_modified = None
    if cached_query.last_modified:
        last_modified = cached_query.last_modified(rows)
        last_modified = format_datetime(last_modified, usegmt=True)

    result, encoding = converters.convert(rows, env.get("HTTP_ACCEPT"))
    length = len(result)

    headers = [
        ("Content-Length", str(length)),
        ("Content-Type", encoding),
        ("Date", date),
    ]
    if last_modified:
        headers.append(("Last-Modified", last_modified))

    start_response("200 OK", headers)
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
    path = prefix_path + name.replace("_", "-").rstrip(".md")

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
        param_mappings=query.param_mappings,
        last_modified=query.last_modified,
    )
