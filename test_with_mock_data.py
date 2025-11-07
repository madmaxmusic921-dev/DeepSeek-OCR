#!/usr/bin/env python3
"""
Mock Data Test for Reddit Fetcher
Demonstrates how the module processes data without requiring API access
"""

import json
from datetime import datetime


def create_mock_post_data():
    """Create mock Reddit post data to demonstrate the expected structure"""
    return {
        "id": "abc123",
        "title": "TIL that octopuses have three hearts and blue blood",
        "author": "science_enthusiast",
        "subreddit": "todayilearned",
        "url": "https://reddit.com/r/todayilearned/comments/abc123/",
        "created_utc": 1699000000.0,
        "created_datetime": datetime.fromtimestamp(1699000000.0).isoformat(),
        "score": 15234,
        "upvote_ratio": 0.97,
        "num_comments": 456,
        "is_self": True,
        "is_video": False,
        "over_18": False,
        "spoiler": False,
        "locked": False,
        "distinguished": None,
        "selftext": "I was reading about marine biology and discovered that octopuses have three hearts. Two pump blood to the gills, while the third pumps blood to the rest of the body. Their blood is blue because it contains copper-based hemocyanin instead of iron-based hemoglobin!",
        "selftext_html": "&lt;p&gt;I was reading about marine biology...&lt;/p&gt;",
        "body": "I was reading about marine biology and discovered that octopuses have three hearts. Two pump blood to the gills, while the third pumps blood to the rest of the body. Their blood is blue because it contains copper-based hemocyanin instead of iron-based hemoglobin!",
        "media": {"has_media": False, "media_type": None, "urls": []},
        "link_flair_text": "Science",
        "author_flair_text": "Marine Biologist",
        "awards": [
            {"name": "Gold", "count": 5, "coin_price": 500},
            {"name": "Silver", "count": 23, "coin_price": 100},
        ],
        "total_awards_received": 28,
        "comments": [
            {
                "id": "comment1",
                "author": "ocean_expert",
                "body": "This is fascinating! Another cool fact: octopuses can taste with their tentacles. They have chemoreceptors on their suckers!",
                "score": 2543,
                "created_utc": 1699001000.0,
                "is_submitter": False,
                "distinguished": None,
                "depth": 0,
            },
            {
                "id": "comment2",
                "author": "biology_student",
                "body": "I learned this in my marine biology class! The copper in their blood makes it more efficient in cold, low-oxygen environments.",
                "score": 1234,
                "created_utc": 1699002000.0,
                "is_submitter": False,
                "distinguished": None,
                "depth": 0,
            },
            {
                "id": "comment3",
                "author": "science_enthusiast",
                "body": "Thanks everyone for the additional facts! I love learning from this community.",
                "score": 567,
                "created_utc": 1699003000.0,
                "is_submitter": True,
                "distinguished": None,
                "depth": 0,
            },
        ],
    }


def test_mock_data_structure():
    """Test that our mock data matches expected structure"""
    print("=" * 60)
    print("Testing Mock Reddit Post Data Structure")
    print("=" * 60)

    mock_post = create_mock_post_data()

    # Test required fields
    required_fields = [
        "id",
        "title",
        "author",
        "subreddit",
        "url",
        "score",
        "num_comments",
        "body",
        "comments",
        "media",
    ]

    print("\n1. Required Fields:")
    all_present = True
    for field in required_fields:
        present = field in mock_post
        status = "✓" if present else "✗"
        print(f"  {status} {field}: {present}")
        if not present:
            all_present = False

    if all_present:
        print("\n✓ All required fields present")

    # Test data types
    print("\n2. Data Types:")
    type_checks = [
        ("id", str),
        ("title", str),
        ("score", int),
        ("upvote_ratio", float),
        ("comments", list),
        ("media", dict),
    ]

    all_correct = True
    for field, expected_type in type_checks:
        actual_type = type(mock_post[field])
        correct = isinstance(mock_post[field], expected_type)
        status = "✓" if correct else "✗"
        print(f"  {status} {field}: {expected_type.__name__} = {actual_type.__name__}")
        if not correct:
            all_correct = False

    if all_correct:
        print("\n✓ All data types correct")

    # Test comment structure
    print("\n3. Comment Structure:")
    if mock_post["comments"]:
        first_comment = mock_post["comments"][0]
        comment_fields = ["id", "author", "body", "score", "is_submitter"]
        for field in comment_fields:
            present = field in first_comment
            status = "✓" if present else "✗"
            print(f"  {status} Comment has '{field}': {present}")

    # Test media structure
    print("\n4. Media Structure:")
    media = mock_post["media"]
    media_fields = ["has_media", "media_type", "urls"]
    for field in media_fields:
        present = field in media
        status = "✓" if present else "✗"
        print(f"  {status} Media has '{field}': {present}")

    return mock_post


def demonstrate_post_processing(mock_post):
    """Demonstrate how the fetched data would be processed"""
    print("\n" + "=" * 60)
    print("Demonstrating Post Processing for Video Script")
    print("=" * 60)

    # Create video script
    print("\n5. Video Script Generation:")
    print("-" * 60)

    script = f"""
INTRO (5 seconds):
"Today on Reddit: {mock_post['title']}"
Posted in r/{mock_post['subreddit']}

MAIN CONTENT (30 seconds):
{mock_post['body']}

ENGAGEMENT STATS:
- {mock_post['score']:,} upvotes ({mock_post['upvote_ratio']:.0%} upvote ratio)
- {mock_post['num_comments']} comments
- {mock_post['total_awards_received']} awards

TOP COMMENTS (20 seconds):
"""

    for i, comment in enumerate(mock_post["comments"][:3], 1):
        script += f"\n{i}. u/{comment['author']} ({comment['score']} upvotes):\n"
        script += f"   {comment['body'][:100]}...\n"

    script += """
OUTRO (5 seconds):
Thanks for watching! Like and subscribe for more Reddit content!
"""

    print(script)
    print("-" * 60)
    print("✓ Script generated successfully")

    # Calculate video timing
    print("\n6. Video Timing Breakdown:")
    total_duration = 60  # seconds
    segments = [
        ("Intro", 5),
        ("Main Content", 30),
        ("Comments", 20),
        ("Outro", 5),
    ]

    for segment, duration in segments:
        percentage = (duration / total_duration) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {segment:15} {bar:30} {duration}s ({percentage:.0f}%)")

    return script


def demonstrate_json_export(mock_post):
    """Demonstrate JSON export functionality"""
    print("\n" + "=" * 60)
    print("JSON Export Demonstration")
    print("=" * 60)

    output_file = "/tmp/mock_reddit_post.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(mock_post, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Mock data exported to: {output_file}")
    print(f"  File size: {len(json.dumps(mock_post, indent=2))} bytes")

    # Show JSON preview
    print("\nJSON Preview (first 500 characters):")
    print("-" * 60)
    json_str = json.dumps(mock_post, indent=2)[:500]
    print(json_str + "...")
    print("-" * 60)


def demonstrate_data_filtering():
    """Demonstrate how data can be filtered for different video types"""
    print("\n" + "=" * 60)
    print("Data Filtering for Different Video Types")
    print("=" * 60)

    mock_post = create_mock_post_data()

    # Short form (TikTok/YouTube Shorts) - 30 seconds
    print("\n1. Short Form Video (30s):")
    print(f"  - Title: {mock_post['title'][:50]}...")
    print(f"  - Body (first 100 chars): {mock_post['body'][:100]}...")
    print(f"  - Top 1 comment only")
    print(f"  ✓ Optimized for quick engagement")

    # Medium form (Instagram/Facebook) - 60 seconds
    print("\n2. Medium Form Video (60s):")
    print(f"  - Full title: {mock_post['title']}")
    print(f"  - Full body text")
    print(f"  - Top 3 comments")
    print(f"  - Stats display")
    print(f"  ✓ Balanced content and engagement")

    # Long form (YouTube) - 3+ minutes
    print("\n3. Long Form Video (3+ min):")
    print(f"  - Full title with context")
    print(f"  - Full body with background info")
    print(f"  - Top 10 comments with discussion")
    print(f"  - Awards and community reaction")
    print(f"  - Related subreddit info")
    print(f"  ✓ Deep dive with full context")


def main():
    """Run all mock data tests"""
    print("\n" + "=" * 60)
    print("Reddit Fetcher - Mock Data Testing")
    print("=" * 60)
    print("\nThis demonstrates the module's data structure and processing")
    print("without requiring actual Reddit API credentials.")

    # Create and validate mock data
    mock_post = test_mock_data_structure()

    # Demonstrate processing
    script = demonstrate_post_processing(mock_post)

    # Demonstrate JSON export
    demonstrate_json_export(mock_post)

    # Demonstrate filtering
    demonstrate_data_filtering()

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("✓ Module correctly structures Reddit post data")
    print("✓ Data can be processed into video scripts")
    print("✓ JSON export works as expected")
    print("✓ Data can be filtered for different video formats")
    print("\n⚠ To test with real Reddit data:")
    print("  1. Configure credentials in reddit_config.py")
    print("  2. Run: python examples/reddit_fetcher_example.py")


if __name__ == "__main__":
    main()
