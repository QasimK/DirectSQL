# Update a list

Update the attributes of a single existing list given by `list_id`.

Any of the following attributes can be optionally updated:

* `title`

```sql
WITH
    auth_user AS (
        SELECT user_id
        FROM session
        WHERE
            user_id = :auth_user_id
            AND token = :auth_token
        LIMIT 1
    ),
    auth_list AS (
        SELECT list_id
        FROM user_list
        JOIN auth_user USING (user_id)
        WHERE list_id = :list_id
    )

UPDATE list
SET
    title = COALESCE(:title, title)
WHERE
    list_id IN (SELECT list_id FROM auth_list)
    AND last_modified = :last_modified
    -- Any field is different
    AND title != COALESCE(:title, title)
;
```
