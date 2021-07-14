# Get list(s)

Get the given list(s) by `list_id`. If no `list_id` is given, then all lists will be returned for the user.

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
    split_list_ids_wip(list_id, str) AS (
        SELECT '', :str_list_ids||','
        UNION ALL
            SELECT
                substr(str, 0, instr(str, ','))
              , substr(str, instr(str, ',') + 1)
            FROM split_list_ids_wip
            WHERE str != ''
    ),
    input_list_ids AS (
        SELECT list_id FROM split_list_ids_wip WHERE list_id != ''
    )

SELECT
    user_list.role
  , list.list_id
  , list.title
  , list.last_modified
  , item.item_id
  , item.content
FROM user_list
JOIN auth_user USING (user_id)
JOIN list USING (list_id)
LEFT JOIN item USING (list_id)
WHERE
    :str_list_ids IS NULL
    OR list_id IN (SELECT list_id FROM input_list_ids)
;
```
