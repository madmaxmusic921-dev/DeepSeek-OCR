"""
Reddit Fetcher Module

This module provides comprehensive Reddit post fetching capabilities using PRAW.
It extracts post metadata, content, comments, and media URLs for video script generation.

Example:
    fetcher = RedditFetcher()
    post_data = fetcher.fetch_post_by_id("abc123")
    print(post_data['title'])
"""

import praw
import prawcore
import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

try:
    from reddit_config import REDDIT_CONFIG, FETCH_OPTIONS, SUBREDDIT_FETCH_OPTIONS
except ImportError:
    print("Warning: reddit_config.py not found. Using default configuration.")
    REDDIT_CONFIG = {
        "client_id": os.getenv("REDDIT_CLIENT_ID", ""),
        "client_secret": os.getenv("REDDIT_CLIENT_SECRET", ""),
        "user_agent": os.getenv("REDDIT_USER_AGENT", "RedditVideoScript/1.0"),
    }
    FETCH_OPTIONS = {
        "max_comments": 10,
        "comment_sort": "best",
        "max_comment_depth": 2,
        "min_comment_score": 5,
        "include_awards": True,
        "download_media": False,
        "media_dir": "./reddit_media",
    }
    SUBREDDIT_FETCH_OPTIONS = {
        "limit": 10,
        "time_filter": "week",
        "sort_method": "hot",
    }


class RedditFetcherError(Exception):
    """Base exception for Reddit Fetcher errors"""
    pass


class RedditConnectionError(RedditFetcherError):
    """Raised when connection to Reddit API fails"""
    pass


class RedditPostNotFoundError(RedditFetcherError):
    """Raised when a post cannot be found"""
    pass


class RedditFetcher:
    """
    Fetches Reddit posts and extracts data for video script generation.

    Attributes:
        reddit: PRAW Reddit instance
        options: Dictionary of fetching options
    """

    def __init__(self, config: Optional[Dict] = None, options: Optional[Dict] = None):
        """
        Initialize the Reddit Fetcher.

        Args:
            config: Reddit API configuration (client_id, client_secret, user_agent)
            options: Fetching options (max_comments, comment_sort, etc.)

        Raises:
            RedditConnectionError: If connection to Reddit API fails
        """
        self.config = config or REDDIT_CONFIG
        self.options = {**FETCH_OPTIONS, **(options or {})}

        try:
            self.reddit = praw.Reddit(
                client_id=self.config["client_id"],
                client_secret=self.config["client_secret"],
                user_agent=self.config["user_agent"],
            )
            # Test connection
            self.reddit.user.me()
        except prawcore.exceptions.ResponseException as e:
            raise RedditConnectionError(f"Failed to connect to Reddit API: {e}")
        except Exception as e:
            # Handle cases where authentication is not required for read-only
            if "client_id" in str(e) or "401" in str(e):
                raise RedditConnectionError(
                    f"Invalid Reddit API credentials. Please check reddit_config.py: {e}"
                )

    def fetch_post_by_id(self, post_id: str) -> Dict[str, Any]:
        """
        Fetch a Reddit post by its ID.

        Args:
            post_id: Reddit post ID (e.g., "abc123")

        Returns:
            Dictionary containing post data

        Raises:
            RedditPostNotFoundError: If post cannot be found
        """
        try:
            submission = self.reddit.submission(id=post_id)
            # Force fetch to check if post exists
            _ = submission.title
            return self._extract_post_data(submission)
        except prawcore.exceptions.NotFound:
            raise RedditPostNotFoundError(f"Post with ID '{post_id}' not found")
        except Exception as e:
            raise RedditFetcherError(f"Error fetching post: {e}")

    def fetch_post_by_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch a Reddit post by its URL.

        Args:
            url: Full Reddit post URL

        Returns:
            Dictionary containing post data

        Raises:
            RedditPostNotFoundError: If post cannot be found
        """
        try:
            submission = self.reddit.submission(url=url)
            _ = submission.title
            return self._extract_post_data(submission)
        except prawcore.exceptions.NotFound:
            raise RedditPostNotFoundError(f"Post at URL '{url}' not found")
        except Exception as e:
            raise RedditFetcherError(f"Error fetching post from URL: {e}")

    def fetch_posts_from_subreddit(
        self,
        subreddit_name: str,
        sort_method: Optional[str] = None,
        limit: Optional[int] = None,
        time_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch multiple posts from a subreddit.

        Args:
            subreddit_name: Name of subreddit (without r/)
            sort_method: "hot", "new", "rising", "top", "controversial"
            limit: Number of posts to fetch
            time_filter: "all", "day", "hour", "month", "week", "year"

        Returns:
            List of dictionaries containing post data
        """
        sort_method = sort_method or SUBREDDIT_FETCH_OPTIONS["sort_method"]
        limit = limit or SUBREDDIT_FETCH_OPTIONS["limit"]
        time_filter = time_filter or SUBREDDIT_FETCH_OPTIONS["time_filter"]

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            # Get submissions based on sort method
            if sort_method == "hot":
                submissions = subreddit.hot(limit=limit)
            elif sort_method == "new":
                submissions = subreddit.new(limit=limit)
            elif sort_method == "rising":
                submissions = subreddit.rising(limit=limit)
            elif sort_method == "top":
                submissions = subreddit.top(time_filter=time_filter, limit=limit)
            elif sort_method == "controversial":
                submissions = subreddit.controversial(time_filter=time_filter, limit=limit)
            else:
                raise ValueError(f"Invalid sort method: {sort_method}")

            posts = []
            for submission in submissions:
                try:
                    posts.append(self._extract_post_data(submission))
                except Exception as e:
                    print(f"Warning: Failed to extract post {submission.id}: {e}")
                    continue

            return posts

        except prawcore.exceptions.NotFound:
            raise RedditFetcherError(f"Subreddit '{subreddit_name}' not found")
        except Exception as e:
            raise RedditFetcherError(f"Error fetching posts from subreddit: {e}")

    def _extract_post_data(self, submission) -> Dict[str, Any]:
        """
        Extract comprehensive data from a Reddit submission.

        Args:
            submission: PRAW Submission object

        Returns:
            Dictionary with all post data
        """
        # Basic post information
        post_data = {
            "id": submission.id,
            "title": submission.title,
            "author": str(submission.author) if submission.author else "[deleted]",
            "subreddit": str(submission.subreddit),
            "url": f"https://reddit.com{submission.permalink}",
            "created_utc": submission.created_utc,
            "created_datetime": datetime.fromtimestamp(submission.created_utc).isoformat(),
            "score": submission.score,
            "upvote_ratio": submission.upvote_ratio,
            "num_comments": submission.num_comments,
            "is_self": submission.is_self,
            "is_video": submission.is_video,
            "over_18": submission.over_18,
            "spoiler": submission.spoiler,
            "locked": submission.locked,
            "distinguished": submission.distinguished,
        }

        # Post content
        if submission.is_self:
            post_data["selftext"] = submission.selftext
            post_data["selftext_html"] = submission.selftext_html
            post_data["body"] = self._clean_text(submission.selftext)
        else:
            post_data["selftext"] = ""
            post_data["body"] = ""

        # Media information
        post_data["media"] = self._extract_media_info(submission)

        # Flair information
        post_data["link_flair_text"] = submission.link_flair_text
        post_data["author_flair_text"] = submission.author_flair_text

        # Awards (if enabled)
        if self.options["include_awards"]:
            post_data["awards"] = self._extract_awards(submission)
            post_data["total_awards_received"] = submission.total_awards_received

        # Comments
        post_data["comments"] = self._extract_comments(submission)

        return post_data

    def _extract_media_info(self, submission) -> Dict[str, Any]:
        """Extract media URLs and information from submission."""
        media_info = {
            "has_media": False,
            "media_type": None,
            "urls": [],
        }

        # Check for Reddit-hosted images
        if hasattr(submission, "url") and submission.url:
            parsed = urlparse(submission.url)
            if any(
                ext in submission.url.lower()
                for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
            ):
                media_info["has_media"] = True
                media_info["media_type"] = "image"
                media_info["urls"].append(submission.url)

        # Check for Reddit-hosted videos
        if submission.is_video:
            media_info["has_media"] = True
            media_info["media_type"] = "video"
            if hasattr(submission, "media") and submission.media:
                if "reddit_video" in submission.media:
                    media_info["urls"].append(
                        submission.media["reddit_video"]["fallback_url"]
                    )

        # Check for external video embeds (YouTube, etc.)
        if hasattr(submission, "media") and submission.media:
            if "oembed" in submission.media:
                media_info["has_media"] = True
                media_info["media_type"] = "embed"
                media_info["embed_provider"] = submission.media["oembed"].get(
                    "provider_name", "unknown"
                )

        # Check for galleries
        if hasattr(submission, "is_gallery") and submission.is_gallery:
            media_info["has_media"] = True
            media_info["media_type"] = "gallery"
            if hasattr(submission, "media_metadata"):
                for item_id, item in submission.media_metadata.items():
                    if "s" in item and "u" in item["s"]:
                        media_info["urls"].append(item["s"]["u"])

        # Link posts
        if not submission.is_self and not media_info["has_media"]:
            media_info["has_media"] = True
            media_info["media_type"] = "link"
            media_info["urls"].append(submission.url)

        return media_info

    def _extract_comments(self, submission) -> List[Dict[str, Any]]:
        """Extract top comments from submission."""
        comments_data = []

        # Sort comments
        submission.comment_sort = self.options["comment_sort"]
        submission.comments.replace_more(limit=0)  # Remove "load more" comments

        for comment in submission.comments.list()[: self.options["max_comments"]]:
            if not hasattr(comment, "body"):
                continue

            # Filter by score
            if comment.score < self.options["min_comment_score"]:
                continue

            comment_data = {
                "id": comment.id,
                "author": str(comment.author) if comment.author else "[deleted]",
                "body": self._clean_text(comment.body),
                "score": comment.score,
                "created_utc": comment.created_utc,
                "is_submitter": comment.is_submitter,
                "distinguished": comment.distinguished,
                "depth": comment.depth if hasattr(comment, "depth") else 0,
            }

            comments_data.append(comment_data)

        return comments_data

    def _extract_awards(self, submission) -> List[Dict[str, Any]]:
        """Extract award information from submission."""
        awards = []
        if hasattr(submission, "all_awardings"):
            for award in submission.all_awardings:
                awards.append(
                    {
                        "name": award.get("name", "Unknown"),
                        "count": award.get("count", 0),
                        "coin_price": award.get("coin_price", 0),
                    }
                )
        return awards

    def _clean_text(self, text: str) -> str:
        """
        Clean text for better readability in video scripts.

        Removes extra whitespace, fixes formatting, and handles markdown.
        """
        if not text:
            return ""

        # Remove excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove markdown links but keep text
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

        # Remove markdown formatting
        text = re.sub(r"[*_~`]", "", text)

        # Clean up whitespace
        text = text.strip()

        return text

    def export_to_json(self, post_data: Dict[str, Any], filepath: str) -> None:
        """
        Export post data to JSON file.

        Args:
            post_data: Dictionary containing post data
            filepath: Path to save JSON file
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(post_data, f, indent=2, ensure_ascii=False)
            print(f"Post data exported to: {filepath}")
        except Exception as e:
            raise RedditFetcherError(f"Failed to export to JSON: {e}")

    def get_post_summary(self, post_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of post data.

        Args:
            post_data: Dictionary containing post data

        Returns:
            Formatted string summary
        """
        summary = f"""
Reddit Post Summary
{'=' * 60}
Title: {post_data['title']}
Subreddit: r/{post_data['subreddit']}
Author: u/{post_data['author']}
URL: {post_data['url']}

Stats:
  - Score: {post_data['score']} (Upvote ratio: {post_data['upvote_ratio']:.1%})
  - Comments: {post_data['num_comments']}
  - Created: {post_data['created_datetime']}

Content Type: {'Self Post' if post_data['is_self'] else 'Link Post'}
Media: {post_data['media']['media_type'] if post_data['media']['has_media'] else 'None'}

"""

        if post_data["body"]:
            summary += f"Body Preview:\n{post_data['body'][:200]}...\n\n"

        if post_data["comments"]:
            summary += f"Top Comments ({len(post_data['comments'])}):\n"
            for i, comment in enumerate(post_data["comments"][:3], 1):
                summary += f"  {i}. [{comment['score']}↑] u/{comment['author']}: "
                summary += f"{comment['body'][:100]}...\n"

        return summary


# Convenience functions
def fetch_post(post_id: str, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Quick function to fetch a single post by ID.

    Args:
        post_id: Reddit post ID
        config: Optional Reddit API configuration

    Returns:
        Dictionary containing post data
    """
    fetcher = RedditFetcher(config=config)
    return fetcher.fetch_post_by_id(post_id)


def fetch_post_from_url(url: str, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Quick function to fetch a single post by URL.

    Args:
        url: Full Reddit post URL
        config: Optional Reddit API configuration

    Returns:
        Dictionary containing post data
    """
    fetcher = RedditFetcher(config=config)
    return fetcher.fetch_post_by_url(url)


if __name__ == "__main__":
    # Example usage
    print("Reddit Fetcher Module")
    print("=" * 60)
    print("\nThis module provides Reddit post fetching capabilities.")
    print("See examples/reddit_fetcher_example.py for usage examples.")
