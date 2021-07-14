# Create a new list (TODO)

TODO: This can only work with executescript which cannot take parameters.

The list is automatically shared with the owner

```sql
BEGIN;

WITH
    auth_user AS (
        SELECT user_id
        FROM session
        WHERE
            user_id = :auth_user_id
            AND token = :auth_token
        LIMIT 1
    )

INSERT INTO
    list (title)
SELECT
    (:title)
FROM
    auth_user
-- Requires SQlite 3.35
-- RETURNING list_id
;

INSERT INTO
    user_list (user_id, list_id, role)
SELECT
    auth_user.user_id
  , last_insert_rowid()
  , "OWNER"
FROM
    auth_user
;

COMMIT;
```
