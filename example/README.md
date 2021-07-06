# Example App using DirectSQL

Another TODO app :)

## Running

```
cat migrations/01_initial.sql | sqlite3 db.sqlite3
```

Start `run.sh`

```
curl -i -H "Token: 1" "127.0.0.1:9091/settings?user_id=1"
curl -X POST -i -H "Token: 1" "127.0.0.1:9091/settings?user_id=1&enable_dark_mode=true"
```

## Model

    Session >= Users x List <= Item


## API

- Create User / Register
- Change Password
- Delete User / Forget me
- Add Session / Login
- Delete Session / Logout
- Add List
- Share List
- Delete List (for me)
- Get Lists
- Add Item
- Update Item
- Delete Item
- Get Items
