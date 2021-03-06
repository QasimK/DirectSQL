# DirectSQL

Skip the REST API, because, god, I cannot write more CRUD.

## Features

* Auto-generate a REST API with an OpenAPI specification
* Query SQLite databases (with sensible defaults)
* Write your own executors for other database backends
* Request parameter validation and type conversion
* TSV, CSV, and JSON responses out of the box

## TODO

* Use SQLite Memory Mapped (must catch signal)
    * https://phiresky.github.io/blog/2020/sqlite-performance-tuning/
* POST with parameters in the body
* Return Problem Details error responses
    * Sqlite3 errors, e.g. sqlite3.IntegrityError: UNIQUE constraint failed: user.username
* Multi-threaded mode
* Host the OpenAPI specification
* Register adapters and converters for boolean, ...
* When fetching results do iter instead of fetchall()

## HTTP Headers

Consider using:

* Check Host Header (security)
* Authorization
* ETags (If-None-Match, POST: If-Match)
* Last-Modified (If-Modified-Since, POST: If-Unmodified-Since)
* Range (If-Range, Content-Range, Accept-Ranges); with units=rows, compare to cursors
* Cache-Control
* Server-Timing
* CORS
* OPTIONS; Allow header
* Transfer-Encoding: Chunked; iterator responses
* Content-Encoding? (GZip)
* Digest?
* Expect?
