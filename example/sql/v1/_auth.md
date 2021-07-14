# Authentication CTEs

## Authentication: User Password

Given: `auth_user_id`, and `auth_password`

```sql
WITH
    auth_user AS (
        SELECT user_id
        FROM user
        WHERE
            user_id = :auth_user_id
            AND password = :auth_password
    )
```

## Authentication: Session Token

Given: `auth_user_id`, and `auth_token`

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
```
