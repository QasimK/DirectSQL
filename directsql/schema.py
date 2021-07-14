from typing import Any, Callable, Tuple, List

from .exceptions import InvalidParameters


def compose(*funcs):
    *funcs, penultimate, last = funcs
    if funcs:
        penultimate = compose(*funcs, penultimate)
    return lambda *args, **kwargs: penultimate(last(*args, **kwargs))


def from_querystring(key: str) -> Tuple[str, List[str]]:
    def inner(query_params, headers):
        return key, query_params.get(key)

    return inner


def from_header(key: str) -> Tuple[str, str]:
    def inner(query_params, headers):
        return key, headers.get(key)

    return inner


def required(tup: Tuple[str, Any]) -> Tuple[str, Any]:
    key, value = tup
    if value is None:
        raise InvalidParameters(f"{key} requires a value")

    return key, value


def one(tup: Tuple[str, List[str]]) -> Tuple[str, str]:
    key, values = tup
    if values is None:
        return key, values

    if len(values) != 1:
        raise InvalidParameters(f"{key} expected exactly one querystring value")

    [value] = values
    return key, value


def integer(gt=None, ge=None, lt=None, le=None) -> Callable:
    def validate(tup: Tuple[str, Any]) -> Tuple[str, int]:
        key, value = tup
        if value is None:
            return key, value

        if not _is_int(value):
            raise InvalidParameters(f"{key} must be an integer")

        value = int(value)
        if gt is not None and value <= gt:
            raise InvalidParameters(f"{key} must be strictly greater than {gt}")

        if ge is not None and value < ge:
            raise InvalidParameters(f"{key} must be greater than or equal to {ge}")

        if lt is not None and value >= lt:
            raise InvalidParameters(f"{key} must be strictly less than {lt}")

        if le is not None and value > le:
            raise InvalidParameters(f"{key} must be less than or equal to {le}")

        return key, int(value)

    return validate


def _is_int(s):
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()


def integers(gt=None, ge=None, lt=None, le=None) -> Callable:
    def validate(tup: Tuple[str, List[str]]) -> List[int]:
        key, values = tup
        if values is None:
            return key, values

        validator = integer(gt=gt, ge=ge, lt=lt, le=le)
        result = [validator((key, value))[1] for value in values]
        return key, result

    return validate


def str_list(tup: Tuple[str, List[Any]]) -> Tuple[str, List[str]]:
    key, values = tup
    if values is None:
        return key, values

    result = ",".join((str(value) for value in values))
    return key, result
