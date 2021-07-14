# Delete list

Delete the given lists by `list_id`. At least one list id must be given.

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
    ),
    delete_list_ids AS (
        SELECT list_id
        FROM user_list
        WHERE
            user_id IN (SELECT user_id FROM auth_user)
            AND list_id IN (SELECT list_id FROM input_list_ids)
            AND role = 'OWNER'
    )

DELETE FROM list
WHERE list_id IN (SELECT list_id FROM delete_list_ids)
-- RETURNING list_id
```
