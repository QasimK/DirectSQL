# Create a new list

Create a new list owned by the user.

```sql
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
    fn_add_list (user_id, title)
SELECT
    auth_user.user_id
  , :title
FROM
    auth_user
-- Requires SQlite 3.35
-- RETURNING list_id
;
```
