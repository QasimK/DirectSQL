# Update Settings

Set the settings for the given user

```sql
UPDATE user_settings
SET
    enable_dark_mode = :enable_dark_mode
WHERE
    user_id = :user_id
-- Requires SQlite 3.35
-- RETURNING *
;
```
