# Create a new Session

Authenticate the user with their password to generate a token.

A token is used to authenticate with the remainder of the API.

This allows sessions to continue even when a password changes, and allows individual sessions to be revoked.

```sql
INSERT INTO
    session (user_id, token)
SELECT
    user_id
  , :token
FROM
    user
WHERE
    user_id = :auth_user_id
    AND password = :auth_password
-- Requires SQlite 3.35
-- RETURNING session_id
;
```
