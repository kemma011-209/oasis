-- Schema for friend requests (Facebook-style)
-- Stores pending, accepted, and rejected friend requests
CREATE TABLE IF NOT EXISTS friend_request (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',  -- 'pending', 'accepted', 'rejected'
    created_at DATETIME,
    responded_at DATETIME,
    FOREIGN KEY(sender_id) REFERENCES user(user_id),
    FOREIGN KEY(receiver_id) REFERENCES user(user_id)
);

