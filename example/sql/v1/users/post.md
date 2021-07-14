# Create a new User

Create a new User, returning the User ID.

```sql
INSERT INTO
    user (password, name)
VALUES
    (:password, :name)
-- Requires SQlite 3.35
-- RETURNING user_id
;
```
