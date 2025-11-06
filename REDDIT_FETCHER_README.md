# Reddit Fetcher Module

A comprehensive Reddit post fetching module using PRAW (Python Reddit API Wrapper) for extracting post data to generate video scripts.

## Features

- **Fetch posts by ID or URL** - Get any Reddit post using its ID or full URL
- **Fetch multiple posts from subreddits** - Retrieve posts with various sorting methods
- **Comprehensive data extraction** - Title, body, comments, media, awards, metadata
- **Flexible configuration** - Customize comment limits, sorting, filtering
- **Media support** - Extract images, videos, galleries, and external links
- **JSON export** - Save post data for later use
- **Error handling** - Robust exception handling with custom error types
- **Clean text processing** - Remove markdown and format text for video scripts

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Reddit API credentials

To use the Reddit API, you need to create a Reddit application:

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **name**: Your application name (e.g., "Video Script Generator")
   - **App type**: Select "script"
   - **description**: Optional description
   - **about url**: Leave blank
   - **redirect uri**: Enter `http://localhost:8080`
4. Click "Create app"
5. Copy your **client_id** (under the app name) and **client_secret**

### 3. Configure credentials

Edit `reddit_config.py` and add your credentials:

```python
REDDIT_CONFIG = {
    "client_id": "YOUR_CLIENT_ID_HERE",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "user_agent": "RedditVideoScript/1.0 (by /u/YourUsername)",
}
```

**Alternative: Use environment variables**

```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="RedditVideoScript/1.0"
```

## Quick Start

### Fetch a post by ID

```python
from reddit_fetcher import RedditFetcher

fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

print(post_data['title'])
print(post_data['body'])
print(f"Score: {post_data['score']}")
```

### Fetch a post by URL

```python
url = "https://www.reddit.com/r/AskReddit/comments/example/"
post_data = fetcher.fetch_post_by_url(url)
```

### Fetch posts from a subreddit

```python
posts = fetcher.fetch_posts_from_subreddit(
    subreddit_name="AskReddit",
    sort_method="hot",
    limit=10
)

for post in posts:
    print(f"{post['title']} - {post['score']} upvotes")
```

## Usage Examples

### Example 1: Get post summary

```python
from reddit_fetcher import RedditFetcher

fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

# Print human-readable summary
print(fetcher.get_post_summary(post_data))
```

### Example 2: Export to JSON

```python
post_data = fetcher.fetch_post_by_id("abc123")
fetcher.export_to_json(post_data, "reddit_post.json")
```

### Example 3: Custom options

```python
custom_options = {
    "max_comments": 20,
    "comment_sort": "top",
    "min_comment_score": 10,
    "include_awards": True,
}

fetcher = RedditFetcher(options=custom_options)
post_data = fetcher.fetch_post_by_id("abc123")
```

### Example 4: Analyze media content

```python
post_data = fetcher.fetch_post_by_id("abc123")

if post_data['media']['has_media']:
    print(f"Media type: {post_data['media']['media_type']}")
    print(f"URLs: {post_data['media']['urls']}")
```

### Example 5: Process comments

```python
post_data = fetcher.fetch_post_by_id("abc123")

for comment in post_data['comments']:
    print(f"[{comment['score']}] {comment['author']}: {comment['body']}")
```

## Data Structure

The `fetch_post_by_id()` and related methods return a dictionary with the following structure:

```python
{
    # Basic information
    "id": "abc123",
    "title": "Post title",
    "author": "username",
    "subreddit": "AskReddit",
    "url": "https://reddit.com/r/AskReddit/...",

    # Timestamps
    "created_utc": 1234567890,
    "created_datetime": "2024-01-01T12:00:00",

    # Stats
    "score": 1234,
    "upvote_ratio": 0.95,
    "num_comments": 567,

    # Content
    "body": "Clean post text...",
    "selftext": "Original markdown text...",

    # Media
    "media": {
        "has_media": True,
        "media_type": "image",
        "urls": ["https://..."]
    },

    # Comments
    "comments": [
        {
            "id": "comment_id",
            "author": "commenter",
            "body": "Comment text...",
            "score": 100,
            "created_utc": 1234567890,
            "is_submitter": False,
            "depth": 0
        }
    ],

    # Awards (if enabled)
    "awards": [
        {
            "name": "Gold",
            "count": 2,
            "coin_price": 500
        }
    ],

    # Flags
    "is_self": True,
    "is_video": False,
    "over_18": False,
    "spoiler": False,
    "locked": False
}
```

## Configuration Options

### reddit_config.py

```python
# API Credentials
REDDIT_CONFIG = {
    "client_id": "your_client_id",
    "client_secret": "your_secret",
    "user_agent": "app_name/version"
}

# Fetch Options
FETCH_OPTIONS = {
    "max_comments": 10,              # Max comments to fetch
    "comment_sort": "best",          # Sort method
    "max_comment_depth": 2,          # Comment tree depth
    "min_comment_score": 5,          # Minimum score filter
    "include_awards": True,          # Include award data
    "download_media": False,         # Download media files
    "media_dir": "./reddit_media"    # Media save directory
}

# Subreddit Fetch Options
SUBREDDIT_FETCH_OPTIONS = {
    "limit": 10,                     # Number of posts
    "time_filter": "week",           # Time filter
    "sort_method": "hot"             # Sort method
}
```

### Comment Sort Methods

- `"best"` - Reddit's best algorithm (default)
- `"top"` - Highest scored
- `"new"` - Newest first
- `"controversial"` - Most controversial
- `"old"` - Oldest first
- `"qa"` - Q&A mode

### Subreddit Sort Methods

- `"hot"` - Currently trending (default)
- `"new"` - Newest posts
- `"rising"` - Rising posts
- `"top"` - Top posts (use with time_filter)
- `"controversial"` - Controversial posts (use with time_filter)

### Time Filters

- `"hour"` - Past hour
- `"day"` - Past 24 hours
- `"week"` - Past week (default)
- `"month"` - Past month
- `"year"` - Past year
- `"all"` - All time

## Error Handling

The module provides custom exception types:

```python
from reddit_fetcher import (
    RedditFetcher,
    RedditFetcherError,
    RedditConnectionError,
    RedditPostNotFoundError
)

try:
    fetcher = RedditFetcher()
    post = fetcher.fetch_post_by_id("invalid_id")
except RedditConnectionError as e:
    print(f"API connection failed: {e}")
except RedditPostNotFoundError as e:
    print(f"Post not found: {e}")
except RedditFetcherError as e:
    print(f"General error: {e}")
```

## Running Examples

Run the example script:

```bash
python examples/reddit_fetcher_example.py
```

This provides interactive examples including:
1. Fetch by ID
2. Fetch by URL
3. Fetch from subreddit
4. Export to JSON
5. Custom options
6. Media analysis
7. Interactive mode

## Use Cases

### Video Script Generation

```python
fetcher = RedditFetcher()
post = fetcher.fetch_post_by_id("abc123")

# Create video script
script = f"""
INTRO: {post['title']}
Posted in r/{post['subreddit']} by {post['author']}

MAIN CONTENT:
{post['body']}

TOP COMMENTS:
"""

for comment in post['comments'][:3]:
    script += f"\n{comment['author']}: {comment['body']}\n"

print(script)
```

### Content Analysis

```python
posts = fetcher.fetch_posts_from_subreddit("AskReddit", limit=100)

# Analyze engagement
avg_score = sum(p['score'] for p in posts) / len(posts)
avg_comments = sum(p['num_comments'] for p in posts) / len(posts)

print(f"Average score: {avg_score}")
print(f"Average comments: {avg_comments}")
```

### Media Collection

```python
posts = fetcher.fetch_posts_from_subreddit("pics", limit=50)

image_urls = []
for post in posts:
    if post['media']['media_type'] == 'image':
        image_urls.extend(post['media']['urls'])

print(f"Found {len(image_urls)} images")
```

## Convenience Functions

Quick one-liners without creating a fetcher instance:

```python
from reddit_fetcher import fetch_post, fetch_post_from_url

# Fetch by ID
post = fetch_post("abc123")

# Fetch by URL
post = fetch_post_from_url("https://reddit.com/r/AskReddit/...")
```

## API Rate Limits

Reddit's API has rate limits:
- 60 requests per minute for authenticated users
- The module handles this automatically via PRAW
- For large-scale scraping, consider implementing delays

## Privacy and Ethics

- Respect Reddit's Terms of Service
- Don't scrape user data without permission
- Be mindful of subreddit rules
- Don't use for spam or harassment
- Consider user privacy when sharing fetched data

## Troubleshooting

### "Invalid credentials" error
- Check that your `client_id` and `client_secret` are correct
- Ensure your app type is set to "script"
- Verify `user_agent` is set properly

### "Post not found" error
- Verify the post ID or URL is correct
- Check if the post was deleted or removed
- Ensure the post is publicly accessible

### "Rate limit exceeded" error
- Reddit allows 60 requests/minute
- Add delays between requests
- Use batch fetching when possible

## Contributing

To extend the module:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This module is part of the DeepSeek-OCR project. See LICENSE file for details.

## Next Steps

After fetching Reddit posts, you can:
1. **Generate video scripts** - Convert post data to narration scripts
2. **Create visualizations** - Generate images from post content
3. **Add text-to-speech** - Convert scripts to audio
4. **Compose videos** - Combine media, audio, and subtitles

See the video script generation module for the next step in the pipeline.
