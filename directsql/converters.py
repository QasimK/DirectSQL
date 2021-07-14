"""Convert a database response into an HTML response."""
import csv
import json
import io
from typing import Optional, Tuple


def convert(rows: list, accept: Optional[str]) -> Tuple[bytes, str]:
    if accept.lower() == "application/csv":
        return convert_to_csv(rows), "text/csv; charset=UTF-8"
    if accept.lower() == "application/json":
        return convert_to_json(rows), "application/json; charset=UTF-8"
    else:
        return convert_to_tsv(rows), "text/tsv; charset=UTF-8"


def convert_to_tsv(rows: list) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output, delimiter="\t")
    writer.writerow(rows[0].keys())
    writer.writerows(rows)
    result = output.getvalue().encode("utf-8")
    return result


def convert_to_csv(rows: list) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(rows[0].keys())
    writer.writerows(rows)
    result = output.getvalue().encode("utf-8")
    return result


def convert_to_json(rows: list) -> bytes:
    data = [dict(row) for row in rows]
    result = json.dumps(data)
    return result.encode("utf-8")
