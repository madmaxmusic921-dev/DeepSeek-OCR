#!/usr/bin/env python3
"""
Reddit Fetcher Example Script

This script demonstrates how to use the RedditFetcher module to:
1. Fetch a single post by ID
2. Fetch a post by URL
3. Fetch multiple posts from a subreddit
4. Export data to JSON
5. Generate summaries

Before running, make sure to:
1. Install dependencies: pip install -r requirements.txt
2. Configure your Reddit API credentials in reddit_config.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reddit_fetcher import RedditFetcher, RedditFetcherError


def example_1_fetch_by_id():
    """Example 1: Fetch a single post by ID"""
    print("\n" + "=" * 60)
    print("Example 1: Fetch Post by ID")
    print("=" * 60)

    fetcher = RedditFetcher()

    # Example post ID (you can replace with any Reddit post ID)
    post_id = "1234abc"  # Replace with actual post ID

    try:
        post_data = fetcher.fetch_post_by_id(post_id)
        print(fetcher.get_post_summary(post_data))

        # Access specific fields
        print(f"\nTitle: {post_data['title']}")
        print(f"Score: {post_data['score']}")
        print(f"Comments: {post_data['num_comments']}")

    except RedditFetcherError as e:
        print(f"Error: {e}")


def example_2_fetch_by_url():
    """Example 2: Fetch a post by URL"""
    print("\n" + "=" * 60)
    print("Example 2: Fetch Post by URL")
    print("=" * 60)

    fetcher = RedditFetcher()

    # Example Reddit URL
    url = "https://www.reddit.com/r/AskReddit/comments/example/"

    try:
        post_data = fetcher.fetch_post_by_url(url)
        print(fetcher.get_post_summary(post_data))

    except RedditFetcherError as e:
        print(f"Error: {e}")


def example_3_fetch_from_subreddit():
    """Example 3: Fetch multiple posts from a subreddit"""
    print("\n" + "=" * 60)
    print("Example 3: Fetch Posts from Subreddit")
    print("=" * 60)

    fetcher = RedditFetcher()

    subreddit = "AskReddit"  # Replace with any subreddit

    try:
        posts = fetcher.fetch_posts_from_subreddit(
            subreddit_name=subreddit, sort_method="hot", limit=5
        )

        print(f"\nFetched {len(posts)} posts from r/{subreddit}:\n")

        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
            print(f"   Score: {post['score']} | Comments: {post['num_comments']}")
            print(f"   URL: {post['url']}\n")

    except RedditFetcherError as e:
        print(f"Error: {e}")


def example_4_export_to_json():
    """Example 4: Export post data to JSON"""
    print("\n" + "=" * 60)
    print("Example 4: Export Post to JSON")
    print("=" * 60)

    fetcher = RedditFetcher()

    post_id = "1234abc"  # Replace with actual post ID

    try:
        post_data = fetcher.fetch_post_by_id(post_id)

        # Export to JSON file
        output_file = "reddit_post_data.json"
        fetcher.export_to_json(post_data, output_file)

        print(f"Post data exported to: {output_file}")

    except RedditFetcherError as e:
        print(f"Error: {e}")


def example_5_custom_options():
    """Example 5: Use custom fetching options"""
    print("\n" + "=" * 60)
    print("Example 5: Custom Fetching Options")
    print("=" * 60)

    # Custom options
    custom_options = {
        "max_comments": 20,  # Fetch more comments
        "comment_sort": "top",  # Sort by top instead of best
        "min_comment_score": 10,  # Higher minimum score
        "include_awards": True,
    }

    fetcher = RedditFetcher(options=custom_options)

    post_id = "1234abc"  # Replace with actual post ID

    try:
        post_data = fetcher.fetch_post_by_id(post_id)

        print(f"Fetched {len(post_data['comments'])} comments")
        print(f"Awards: {post_data.get('total_awards_received', 0)}")

        # Print top comments
        for comment in post_data["comments"][:5]:
            print(f"\n[{comment['score']}↑] {comment['author']}:")
            print(f"{comment['body'][:150]}...")

    except RedditFetcherError as e:
        print(f"Error: {e}")


def example_6_analyze_media():
    """Example 6: Analyze media content in posts"""
    print("\n" + "=" * 60)
    print("Example 6: Analyze Media Content")
    print("=" * 60)

    fetcher = RedditFetcher()

    subreddit = "pics"  # Image-heavy subreddit

    try:
        posts = fetcher.fetch_posts_from_subreddit(
            subreddit_name=subreddit, sort_method="hot", limit=10
        )

        media_stats = {
            "image": 0,
            "video": 0,
            "gallery": 0,
            "link": 0,
            "none": 0,
        }

        for post in posts:
            media_type = post["media"]["media_type"]
            if media_type:
                media_stats[media_type] = media_stats.get(media_type, 0) + 1
            else:
                media_stats["none"] += 1

        print(f"\nMedia distribution in r/{subreddit}:")
        for media_type, count in media_stats.items():
            print(f"  {media_type.capitalize()}: {count}")

        # Show posts with media
        print(f"\nPosts with media:")
        for post in posts:
            if post["media"]["has_media"]:
                print(f"\n- {post['title']}")
                print(f"  Type: {post['media']['media_type']}")
                if post["media"]["urls"]:
                    print(f"  URL: {post['media']['urls'][0]}")

    except RedditFetcherError as e:
        print(f"Error: {e}")


def interactive_mode():
    """Interactive mode: Let user input post ID or URL"""
    print("\n" + "=" * 60)
    print("Interactive Reddit Fetcher")
    print("=" * 60)

    fetcher = RedditFetcher()

    while True:
        print("\nOptions:")
        print("1. Fetch post by ID")
        print("2. Fetch post by URL")
        print("3. Fetch posts from subreddit")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            post_id = input("Enter Reddit post ID: ").strip()
            try:
                post_data = fetcher.fetch_post_by_id(post_id)
                print(fetcher.get_post_summary(post_data))

                # Ask if user wants to export
                export = input("\nExport to JSON? (y/n): ").strip().lower()
                if export == "y":
                    filename = f"reddit_post_{post_id}.json"
                    fetcher.export_to_json(post_data, filename)

            except RedditFetcherError as e:
                print(f"Error: {e}")

        elif choice == "2":
            url = input("Enter Reddit post URL: ").strip()
            try:
                post_data = fetcher.fetch_post_by_url(url)
                print(fetcher.get_post_summary(post_data))

            except RedditFetcherError as e:
                print(f"Error: {e}")

        elif choice == "3":
            subreddit = input("Enter subreddit name (without r/): ").strip()
            limit = input("Number of posts to fetch (default 10): ").strip()
            limit = int(limit) if limit else 10

            try:
                posts = fetcher.fetch_posts_from_subreddit(
                    subreddit_name=subreddit, limit=limit
                )

                for i, post in enumerate(posts, 1):
                    print(f"\n{i}. {post['title']}")
                    print(f"   Score: {post['score']} | Comments: {post['num_comments']}")

            except RedditFetcherError as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


def main():
    """Main function to run examples"""
    print("Reddit Fetcher Examples")
    print("=" * 60)

    print("\nAvailable examples:")
    print("1. Fetch post by ID")
    print("2. Fetch post by URL")
    print("3. Fetch posts from subreddit")
    print("4. Export to JSON")
    print("5. Custom options")
    print("6. Analyze media")
    print("7. Interactive mode")
    print("0. Run all examples")

    choice = input("\nSelect example to run (0-7): ").strip()

    if choice == "1":
        example_1_fetch_by_id()
    elif choice == "2":
        example_2_fetch_by_url()
    elif choice == "3":
        example_3_fetch_from_subreddit()
    elif choice == "4":
        example_4_export_to_json()
    elif choice == "5":
        example_5_custom_options()
    elif choice == "6":
        example_6_analyze_media()
    elif choice == "7":
        interactive_mode()
    elif choice == "0":
        example_1_fetch_by_id()
        example_2_fetch_by_url()
        example_3_fetch_from_subreddit()
        example_4_export_to_json()
        example_5_custom_options()
        example_6_analyze_media()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
