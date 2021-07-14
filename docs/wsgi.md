# WSGI

Specification: <https://www.python.org/dev/peps/pep-0333/#environ-variables>

## env

The environ dictionary contains, among other things:

* `REQUEST_METHOD` e.g. GET
* `QUERY_STRING` e.g. "a=1"
* `HTTP_X` e.g. `HTTP_AUTHORIZATION` for the `Authorization` header
