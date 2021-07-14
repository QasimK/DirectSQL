from datetime import datetime, timezone
from typing import List


def max_last_modified_str(column_or_columns):
    """Use the maximum value of the given column(s) as the last modified."""
    if isinstance(column_or_columns, str):
        columns = [column_or_columns]
    else:
        columns = column_or_columns

    def get_last_modified(rows: list) -> datetime:
        max_ = None
        for row in rows:
            for column in columns:
                value = row[column]
                dt = datetime.fromisoformat(value)
                if max_ is None or dt > max_:
                    max_ = dt

        if max_:
            max_ = max_.replace(tzinfo=timezone.utc)
        return max_

    return get_last_modified
