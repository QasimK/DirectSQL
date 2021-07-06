from .exceptions import InvalidParameters


def validate_int(gt=None, ge=None, lt=None, le=None):
    def validate(key, values, headers=None) -> int:
        if len(values) != 1:
            raise InvalidParameters(f"{key} expected exactly one integer")

        [value] = values
        if not _is_int(value):
            raise InvalidParameters(f"{key} must be an integer")

        if gt is not None and value <= gt:
            raise InvalidParameters(f"{key} must be strictly greater than {gt}")

        if ge is not None and value < ge:
            raise InvalidParameters(f"{key} must be greater than or equal to {ge}")

        if lt is not None and value >= lt:
            raise InvalidParameters(f"{key} must be strictly less than {lt}")

        if le is not None and value > le:
            raise InvalidParameters(f"{key} must be less than or equal to {le}")

        return int(value)

    return validate


def validate_one(key, values, headers=None) -> int:
    if len(values) != 1:
        raise InvalidParameters(f"{key} expected exactly one parameter")

    [value] = values
    return value


def _is_int(s):
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()
