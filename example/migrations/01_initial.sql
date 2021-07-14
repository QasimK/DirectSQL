BEGIN;

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
        CHECK (typeof(password) = 'text'),
    last_modified TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        CHECK (typeof(last_modified) = 'text')
        CHECK (last_modified == strftime('%Y-%m-%d %H:%M:%S', last_modified))
);
CREATE INDEX idx_user_idx on user(user_id);


CREATE TABLE session (
    session_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL
        REFERENCES user ON DELETE CASCADE ON UPDATE CASCADE,
    token TEXT NOT NULL
        CHECK (typeof(token) = 'text'),
    last_contact TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        CHECK (typeof(last_contact) = 'text')
        CHECK (last_contact == strftime('%Y-%m-%d %H:%M:%S', last_contact))
);
CREATE INDEX idx_session_user_id_index on session(user_id);


CREATE TABLE list (
    list_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
        CHECK (typeof(title) = 'text'),
    last_modified TEXT NOT NULL
        CHECK (typeof(last_modified) = 'text')
        CHECK (last_modified == strftime('%Y-%m-%d %H:%M:%S', last_modified))
);


CREATE TABLE user_list (
    user_id INTEGER NOT NULL
        REFERENCES user ON DELETE CASCADE ON UPDATE CASCADE,
    list_id INTEGER NOT NULL
        REFERENCES list ON DELETE CASCADE ON UPDATE CASCADE,
    role TEXT NOT NULL
        CHECK (role IN ('OWNER', 'WRITER', 'READER')),

    UNIQUE(user_id, list_id)
);
CREATE INDEX idx_user_list_user_id on user_list(user_id);
CREATE INDEX idx_user_list_list_id on user_list(list_id);


CREATE TABLE item (
    item_id INTEGER PRIMARY KEY,
    list_id INTEGER NOT NULL
        REFERENCES list ON DELETE CASCADE ON UPDATE CASCADE,
    content TEXT NOT NULL
        CHECK (typeof(content) = 'text')
);
CREATE INDEX idx_item_list_id on item(list_id);

PRAGMA user_version = 1;

COMMIT;
