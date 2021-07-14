# Delete a session

Revoke a session.

Authentication: User Password

```sql
WITH
    auth_user AS (
        SELECT user_id
        FROM user
        WHERE
            user_id = :auth_user_id
            AND password = :auth_password
    )

DELETE FROM
    session
WHERE
    user_id IN (SELECT user_id FROM auth_user)
    AND session_id = :session_id
-- Requires SQlite 3.35
-- RETURNING session_id
;
```
