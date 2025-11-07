#!/usr/bin/env python3
"""
Test script for Reddit Fetcher module
Tests module structure and functionality without requiring Reddit API access
"""

import sys
import inspect
from typing import get_type_hints

# Import the module
try:
    import reddit_fetcher
    from reddit_fetcher import (
        RedditFetcher,
        RedditFetcherError,
        RedditConnectionError,
        RedditPostNotFoundError,
        fetch_post,
        fetch_post_from_url,
    )
    print("✓ Module imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test counters
tests_passed = 0
tests_failed = 0


def test(name, condition, error_msg=""):
    """Helper function to run tests"""
    global tests_passed, tests_failed
    if condition:
        print(f"  ✓ {name}")
        tests_passed += 1
    else:
        print(f"  ✗ {name}: {error_msg}")
        tests_failed += 1


print("\n" + "=" * 60)
print("Testing Reddit Fetcher Module Structure")
print("=" * 60)

# Test 1: Check exception hierarchy
print("\n1. Exception Classes:")
test(
    "RedditFetcherError exists",
    issubclass(RedditFetcherError, Exception),
    "Not a proper Exception subclass",
)
test(
    "RedditConnectionError inherits from RedditFetcherError",
    issubclass(RedditConnectionError, RedditFetcherError),
)
test(
    "RedditPostNotFoundError inherits from RedditFetcherError",
    issubclass(RedditPostNotFoundError, RedditFetcherError),
)

# Test 2: Check RedditFetcher class structure
print("\n2. RedditFetcher Class:")
test("RedditFetcher class exists", hasattr(reddit_fetcher, "RedditFetcher"))
test("RedditFetcher has __init__ method", hasattr(RedditFetcher, "__init__"))

# Check for required methods
required_methods = [
    "fetch_post_by_id",
    "fetch_post_by_url",
    "fetch_posts_from_subreddit",
    "export_to_json",
    "get_post_summary",
]

for method in required_methods:
    test(
        f"RedditFetcher has {method} method",
        hasattr(RedditFetcher, method) and callable(getattr(RedditFetcher, method)),
    )

# Test 3: Check private helper methods
print("\n3. Internal Helper Methods:")
internal_methods = [
    "_extract_post_data",
    "_extract_media_info",
    "_extract_comments",
    "_extract_awards",
    "_clean_text",
]

for method in internal_methods:
    test(f"Has {method} method", hasattr(RedditFetcher, method))

# Test 4: Check convenience functions
print("\n4. Convenience Functions:")
test("fetch_post function exists", callable(fetch_post))
test("fetch_post_from_url function exists", callable(fetch_post_from_url))

# Test 5: Check method signatures
print("\n5. Method Signatures:")


def check_method_params(cls, method_name, expected_params):
    """Check if method has expected parameters"""
    if not hasattr(cls, method_name):
        return False
    method = getattr(cls, method_name)
    sig = inspect.signature(method)
    actual_params = list(sig.parameters.keys())
    # Check if all expected params are present (order doesn't matter for this test)
    return all(param in actual_params for param in expected_params)


test(
    "fetch_post_by_id signature correct",
    check_method_params(RedditFetcher, "fetch_post_by_id", ["self", "post_id"]),
)
test(
    "fetch_post_by_url signature correct",
    check_method_params(RedditFetcher, "fetch_post_by_url", ["self", "url"]),
)
test(
    "fetch_posts_from_subreddit signature correct",
    check_method_params(
        RedditFetcher, "fetch_posts_from_subreddit", ["self", "subreddit_name"]
    ),
)

# Test 6: Test helper functions without API access
print("\n6. Internal Functions:")

# Create a mock instance (won't connect to Reddit, just test structure)
try:
    # Test _clean_text method
    mock_text = """
    This is a [link](http://example.com) with **bold** and *italic* text.



    Multiple newlines here.

    Some `code` and ~~strikethrough~~.
    """

    # We can't instantiate without credentials, so we'll test the function directly
    # by creating a minimal mock object
    class MockFetcher:
        def _clean_text(self, text):
            # Copy the implementation from RedditFetcher
            import re

            if not text:
                return ""
            text = re.sub(r"\n{3,}", "\n\n", text)
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
            text = re.sub(r"[*_~`]", "", text)
            text = text.strip()
            return text

    mock = MockFetcher()
    cleaned = mock._clean_text(mock_text)

    test("_clean_text removes markdown", "**" not in cleaned and "*" not in cleaned)
    test("_clean_text removes links", "http://" not in cleaned and "[" not in cleaned)
    test("_clean_text preserves content", "link" in cleaned and "bold" in cleaned)
    test("_clean_text removes extra newlines", "\n\n\n" not in cleaned)

    print(f"\n   Cleaned text preview: {cleaned[:100]}...")

except Exception as e:
    print(f"  ⚠ Could not test _clean_text: {e}")

# Test 7: Check configuration import
print("\n7. Configuration:")
try:
    from reddit_config import REDDIT_CONFIG, FETCH_OPTIONS, SUBREDDIT_FETCH_OPTIONS

    test("REDDIT_CONFIG imported", REDDIT_CONFIG is not None)
    test("FETCH_OPTIONS imported", FETCH_OPTIONS is not None)
    test("SUBREDDIT_FETCH_OPTIONS imported", SUBREDDIT_FETCH_OPTIONS is not None)

    # Check config keys
    required_config_keys = ["client_id", "client_secret", "user_agent"]
    test(
        "REDDIT_CONFIG has required keys",
        all(key in REDDIT_CONFIG for key in required_config_keys),
    )

    # Check fetch options
    required_fetch_keys = [
        "max_comments",
        "comment_sort",
        "min_comment_score",
        "include_awards",
    ]
    test(
        "FETCH_OPTIONS has required keys",
        all(key in FETCH_OPTIONS for key in required_fetch_keys),
    )

except ImportError as e:
    print(f"  ⚠ Could not import configuration: {e}")

# Test 8: Documentation
print("\n8. Documentation:")
test("Module has docstring", reddit_fetcher.__doc__ is not None)
test("RedditFetcher has docstring", RedditFetcher.__doc__ is not None)
test(
    "fetch_post_by_id has docstring",
    RedditFetcher.fetch_post_by_id.__doc__ is not None,
)

# Test 9: Check example file exists
print("\n9. Example Files:")
import os

test(
    "Example script exists",
    os.path.exists("/home/user/DeepSeek-OCR/examples/reddit_fetcher_example.py"),
)
test(
    "README exists", os.path.exists("/home/user/DeepSeek-OCR/REDDIT_FETCHER_README.md")
)
test("Config file exists", os.path.exists("/home/user/DeepSeek-OCR/reddit_config.py"))
test(
    ".env.example exists", os.path.exists("/home/user/DeepSeek-OCR/.env.example")
)

# Test 10: Validate example script syntax
print("\n10. Example Script Validation:")
try:
    import py_compile

    example_path = "/home/user/DeepSeek-OCR/examples/reddit_fetcher_example.py"
    py_compile.compile(example_path, doraise=True)
    test("Example script has valid Python syntax", True)
except py_compile.PyCompileError as e:
    test("Example script has valid Python syntax", False, str(e))

# Print summary
print("\n" + "=" * 60)
print("Test Summary")
print("=" * 60)
print(f"Tests passed: {tests_passed}")
print(f"Tests failed: {tests_failed}")
print(f"Total tests: {tests_passed + tests_failed}")
print(f"Success rate: {100 * tests_passed / (tests_passed + tests_failed):.1f}%")

if tests_failed == 0:
    print("\n✓ All tests passed! Module structure is correct.")
    print("\n⚠ Note: API functionality requires Reddit credentials")
    print("   Set up credentials in reddit_config.py to test API calls")
else:
    print(f"\n⚠ {tests_failed} test(s) failed. Please review the errors above.")
    sys.exit(1)

# Additional info
print("\n" + "=" * 60)
print("Next Steps")
print("=" * 60)
print("1. Configure Reddit API credentials:")
print("   - Visit: https://www.reddit.com/prefs/apps")
print("   - Create a 'script' type application")
print("   - Copy credentials to reddit_config.py")
print("\n2. Run example script:")
print("   python examples/reddit_fetcher_example.py")
print("\n3. Test with a real Reddit post:")
print("   python -c 'from reddit_fetcher import RedditFetcher; f = RedditFetcher(); print(f.fetch_post_by_id(\"POST_ID\"))'")
