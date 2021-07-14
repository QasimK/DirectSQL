# Example App using DirectSQL

Another TODO app :)

## TODO

- Create user with POST body rather than query string password
- Hash password

## Running

```
cat migrations/01_initial.sql | sqlite3 db.sqlite3
```

Start `run.sh`

```
# Create user
curl -i -X POST "127.0.0.1:9091/v1/users?password=password"

# Create session
curl -i -X POST -H "Authorization: Basic MTpwYXNzd29yZA==" "127.0.0.1:9091/v1/sessions?token=mytoken123"

# Get sessions
curl -i -H "Authorization: Basic MTA6MTIz" "127.0.0.1:9091/v1/sessions"

# Delete session
curl -i -X DELETE -H "Authorization: Basic MTpwYXNzd29yZA==" "127.0.0.1:9091/v1/sessions?session_id=1"

# Add List
curl -i -X POST -H "Authorization: Basic MTA6MTIz" "127.0.0.1:9091/v1/lists?title=mylist"
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
