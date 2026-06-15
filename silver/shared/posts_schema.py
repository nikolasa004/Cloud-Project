POSTS_COLUMNS = [
    "post_id",
    "author_username",
    "platform",
    "content_text",
    "created_at",
    "post_type",
    "title",
    "score",
    "comment_count",
    "hashtags",
    "url",
    "source",
    "is_retweet",
]

POSTS_REQUIRED_COLUMNS = [
    "post_id",
    "author_username",
    "platform",
    "created_at",
    "post_type",
]

POSTS_PLATFORM_VALUES = {"HackerNews", "X"}