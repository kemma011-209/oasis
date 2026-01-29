-- This is the schema definition for the comment table
-- Phase 3A: Added media_content for multimodal support (deferred image generation)
CREATE TABLE comment (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    user_id INTEGER,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    num_likes INTEGER DEFAULT 0,
    num_dislikes INTEGER DEFAULT 0,
    media_content TEXT DEFAULT NULL,  -- Optional image prompt (Phase 3A: faux image layer)
    FOREIGN KEY(post_id) REFERENCES post(post_id),
    FOREIGN KEY(user_id) REFERENCES user(user_id)
);
