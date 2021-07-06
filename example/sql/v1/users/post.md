# Create a new User

Create a new User, returning the User ID

```sql
INSERT INTO
    user (username, password)
VALUES
    (:username, :password)
-- Requires SQlite 3.35
-- RETURNING user_id
;
```
