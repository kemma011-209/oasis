-- Schema for Facebook-style reactions
-- Supports: like, love, haha, wow, sad, angry
CREATE TABLE IF NOT EXISTS reaction (
    reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    reaction_type TEXT NOT NULL,  -- 'like', 'love', 'haha', 'wow', 'sad', 'angry'
    created_at DATETIME,
    FOREIGN KEY(post_id) REFERENCES post(post_id),
    FOREIGN KEY(user_id) REFERENCES user(user_id),
    UNIQUE(post_id, user_id)  -- One reaction per user per post
);


