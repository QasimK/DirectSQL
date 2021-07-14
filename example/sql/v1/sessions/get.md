# Get sessions

Return all (active) sessions.

Authentication: Session token.

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

SELECT
    session_id
  , last_contact
FROM
    session
WHERE
    user_id IN (SELECT user_id FROM auth_user)
;
```
