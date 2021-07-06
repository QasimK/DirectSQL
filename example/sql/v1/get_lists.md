# Get Lists

Return all lists for the given user.

**NOTE:** The user must already exist.

```sql
SELECT
    *
FROM
    lists
WHERE
    user_id = :user_id
;
```
