# Create a new Session

Authenticate the user with their password to generate a token.

A token is used for all of the rest of the API.

This allows sessions to continue even when a password changes.

```sql
INSERT INTO
    session (user_id, token)
VALUES
    (:user_id, :token)
```

Validate the password against the users table somehow...
