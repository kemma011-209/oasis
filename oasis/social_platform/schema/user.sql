-- This is the schema definition for the user table
-- Phase 3A: Added profile_image_prompt and cover_image_prompt for multimodal support
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER,
    user_name TEXT,
    name TEXT,
    bio TEXT,
    created_at DATETIME,
    num_followings INTEGER DEFAULT 0,
    num_followers INTEGER DEFAULT 0,
    profile_image_prompt TEXT DEFAULT NULL,  -- Optional profile picture prompt (Phase 3A)
    cover_image_prompt TEXT DEFAULT NULL  -- Optional cover photo prompt (Phase 3A)
);
