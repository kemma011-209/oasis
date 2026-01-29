# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
from enum import Enum


class ActionType(Enum):
    EXIT = "exit"
    REFRESH = "refresh"
    SEARCH_USER = "search_user"
    SEARCH_POSTS = "search_posts"
    CREATE_POST = "create_post"
    LIKE_POST = "like_post"
    UNLIKE_POST = "unlike_post"
    DISLIKE_POST = "dislike_post"
    UNDO_DISLIKE_POST = "undo_dislike_post"
    REPORT_POST = "report_post"
    FOLLOW = "follow"
    UNFOLLOW = "unfollow"
    MUTE = "mute"
    UNMUTE = "unmute"
    TREND = "trend"
    SIGNUP = "sign_up"
    REPOST = "repost"
    QUOTE_POST = "quote_post"
    UPDATE_REC_TABLE = "update_rec_table"
    CREATE_COMMENT = "create_comment"
    LIKE_COMMENT = "like_comment"
    UNLIKE_COMMENT = "unlike_comment"
    DISLIKE_COMMENT = "dislike_comment"
    UNDO_DISLIKE_COMMENT = "undo_dislike_comment"
    DO_NOTHING = "do_nothing"
    PURCHASE_PRODUCT = "purchase_product"
    INTERVIEW = "interview"
    JOIN_GROUP = "join_group"
    LEAVE_GROUP = "leave_group"
    SEND_TO_GROUP = "send_to_group"
    CREATE_GROUP = "create_group"
    LISTEN_FROM_GROUP = "listen_from_group"

    # Facebook-style actions
    SEND_FRIEND_REQUEST = "send_friend_request"
    ACCEPT_FRIEND_REQUEST = "accept_friend_request"
    REJECT_FRIEND_REQUEST = "reject_friend_request"
    UNFRIEND = "unfriend"
    GET_FRIEND_REQUESTS = "get_friend_requests"
    GET_FRIENDS = "get_friends"
    REACT_TO_POST = "react_to_post"
    REMOVE_REACTION = "remove_reaction"
    CREATE_GROUP_POST = "create_group_post"
    SHARE_TO_GROUP = "share_to_group"

    @classmethod
    def get_default_twitter_actions(cls):
        return [
            cls.CREATE_POST,
            cls.LIKE_POST,
            cls.REPOST,
            cls.FOLLOW,
            cls.DO_NOTHING,
            cls.QUOTE_POST,
        ]

    @classmethod
    def get_default_reddit_actions(cls):
        return [
            cls.LIKE_POST,
            cls.DISLIKE_POST,
            cls.CREATE_POST,
            cls.CREATE_COMMENT,
            cls.LIKE_COMMENT,
            cls.DISLIKE_COMMENT,
            cls.SEARCH_POSTS,
            cls.SEARCH_USER,
            cls.TREND,
            cls.REFRESH,
            cls.DO_NOTHING,
            cls.FOLLOW,
            cls.MUTE,
        ]

    @classmethod
    def get_default_facebook_actions(cls):
        """Get default actions for Facebook-style platform."""
        return [
            cls.CREATE_POST,
            cls.CREATE_GROUP_POST,
            cls.REACT_TO_POST,
            cls.SEND_FRIEND_REQUEST,
            cls.ACCEPT_FRIEND_REQUEST,
            cls.CREATE_COMMENT,
            cls.JOIN_GROUP,
            cls.SHARE_TO_GROUP,
            cls.REFRESH,
            cls.DO_NOTHING,
        ]


class RecsysType(Enum):
    TWITTER = "twitter"
    TWHIN = "twhin-bert"
    REDDIT = "reddit"
    RANDOM = "random"
    FACEBOOK = "facebook"  # Prioritizes friends + group content


class DefaultPlatformType(Enum):
    TWITTER = "twitter"
    REDDIT = "reddit"
    FACEBOOK = "facebook"
