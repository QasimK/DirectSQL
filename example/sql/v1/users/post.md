# Create a new User

Create a new User, returning the User ID

```sql
INSERT INTO
    user (password)
VALUES
    (:password)
-- Requires SQlite 3.35
-- RETURNING user_id
;
```
