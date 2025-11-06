"""
Reddit API Configuration

To use the Reddit fetcher, you need to:
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" as the app type
4. Fill in the required fields
5. Copy your client_id and client_secret below

Alternatively, you can use environment variables:
- REDDIT_CLIENT_ID
- REDDIT_CLIENT_SECRET
- REDDIT_USER_AGENT
"""

import os

# Reddit API Credentials
REDDIT_CONFIG = {
    "client_id": os.getenv("REDDIT_CLIENT_ID", "YOUR_CLIENT_ID_HERE"),
    "client_secret": os.getenv("REDDIT_CLIENT_SECRET", "YOUR_CLIENT_SECRET_HERE"),
    "user_agent": os.getenv("REDDIT_USER_AGENT", "RedditVideoScript/1.0 (by /u/YourUsername)"),
}

# Fetching Options
FETCH_OPTIONS = {
    # Number of comments to fetch per post
    "max_comments": 10,

    # Comment sort method: "best", "top", "new", "controversial", "old", "qa"
    "comment_sort": "best",

    # Maximum comment depth to traverse
    "max_comment_depth": 2,

    # Minimum upvotes for a comment to be included
    "min_comment_score": 5,

    # Whether to include post awards information
    "include_awards": True,

    # Whether to download media (images/videos)
    "download_media": False,

    # Media download directory
    "media_dir": "./reddit_media",
}

# Subreddit Fetch Options
SUBREDDIT_FETCH_OPTIONS = {
    # Number of posts to fetch from subreddit
    "limit": 10,

    # Time filter: "all", "day", "hour", "month", "week", "year"
    "time_filter": "week",

    # Sort method: "hot", "new", "rising", "top", "controversial"
    "sort_method": "hot",
}
