BEGIN;

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
        CHECK (typeof(password) = 'text'),
    name TEXT NOT NULL
        CHECK (typeof(name) = 'text'),
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
    -- When the list aggregate was last modified
    last_modified TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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

CREATE TRIGGER tr_list_update
AFTER UPDATE ON list
FOR EACH ROW
WHEN NEW.last_modified = OLD.last_modified
BEGIN
    UPDATE list
    SET last_modified = CURRENT_TIMESTAMP
    WHERE list_id = NEW.list_id
    ;
END;

CREATE VIEW fn_add_list AS
    SELECT NULL AS user_id, list_id, title FROM list
;

CREATE TRIGGER tr_fn_add_list_insert
INSTEAD OF INSERT ON fn_add_list
FOR EACH ROW
BEGIN
    INSERT INTO list (title) VALUES (NEW.title);
    INSERT INTO user_list VALUES (NEW.user_id, last_insert_rowid(), "OWNER");
END;


CREATE TABLE item (
    item_id INTEGER PRIMARY KEY,
    list_id INTEGER NOT NULL
        REFERENCES list ON DELETE CASCADE ON UPDATE CASCADE,
    content TEXT NOT NULL
        CHECK (typeof(content) = 'text')
);
CREATE INDEX idx_item_list_id on item(list_id);

CREATE TRIGGER tr_item_insert
AFTER INSERT ON item
FOR EACH ROW
BEGIN
    UPDATE list
    SET last_modified = CURRENT_TIMESTAMP
    WHERE list_id = NEW.list_id
    ;
END;

CREATE TRIGGER tr_item_update
AFTER UPDATE ON item
FOR EACH ROW
BEGIN
    UPDATE list
    SET last_modified = CURRENT_TIMESTAMP
    WHERE list_id = NEW.list_id
    ;
END;


PRAGMA user_version = 1;

COMMIT;
