-- Phase 3A: Added cover_image_prompt for multimodal support
CREATE TABLE IF NOT EXISTS `chat_group` (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    cover_image_prompt TEXT DEFAULT NULL  -- Optional group cover image prompt (Phase 3A)
);
