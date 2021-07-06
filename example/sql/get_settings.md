# Get Settings

Return the settings for the user.

**NOTE:** The user must already exist.

```sql
SELECT
    *
FROM
    user_settings
WHERE
    user_id = :user_id
;
```
