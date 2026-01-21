-- Schema for group posts (Facebook-style)
-- Links posts to groups for group-only visibility
CREATE TABLE IF NOT EXISTS group_post (
    group_post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    shared_by INTEGER,  -- User who shared the post to the group (NULL if original)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(group_id) REFERENCES chat_group(group_id),
    FOREIGN KEY(post_id) REFERENCES post(post_id),
    FOREIGN KEY(shared_by) REFERENCES user(user_id)
);

