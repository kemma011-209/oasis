-- Schema for mutual friendships (Facebook-style)
-- Stores bidirectional friend connections
-- Convention: user_id_1 < user_id_2 to prevent duplicate entries
CREATE TABLE IF NOT EXISTS friendship (
    friendship_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id_1 INTEGER NOT NULL,
    user_id_2 INTEGER NOT NULL,
    created_at DATETIME,
    FOREIGN KEY(user_id_1) REFERENCES user(user_id),
    FOREIGN KEY(user_id_2) REFERENCES user(user_id),
    UNIQUE(user_id_1, user_id_2)
);


