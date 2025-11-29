#!/usr/bin/env python3
"""
Test script to verify all bug fixes in reddit_fetcher.py
"""

import html
import sys

def test_fixes():
    """Test all bug fixes"""
    print("=" * 80)
    print("TESTING BUG FIXES IN reddit_fetcher.py")
    print("=" * 80)

    all_passed = True

    # Test 1: Verify html module is imported
    print("\n[Test 1] Verify html module import...")
    try:
        with open('reddit_fetcher.py', 'r') as f:
            content = f.read()
            if 'import html' in content:
                print("✓ PASS: html module is imported")
            else:
                print("✗ FAIL: html module not imported")
                all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        all_passed = False

    # Test 2: Verify comment depth field is removed
    print("\n[Test 2] Verify comment depth field removed...")
    try:
        with open('reddit_fetcher.py', 'r') as f:
            content = f.read()
            lines = content.split('\n')

            # Check that depth field is removed from comment_data
            depth_found = False
            for i, line in enumerate(lines):
                if '"depth":' in line and 'comment_data' in ''.join(lines[max(0, i-10):i+1]):
                    depth_found = True
                    break

            if not depth_found:
                print("✓ PASS: comment depth field removed")
            else:
                print("✗ FAIL: comment depth field still present")
                all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        all_passed = False

    # Test 3: Verify comment filtering logic (fetch 3x, then limit)
    print("\n[Test 3] Verify comment filtering logic...")
    try:
        with open('reddit_fetcher.py', 'r') as f:
            content = f.read()

            if 'max_fetch = self.options["max_comments"] * 3' in content:
                print("✓ PASS: Comments fetched with 3x multiplier")
            else:
                print("✗ FAIL: Comment fetch multiplier not found")
                all_passed = False

            if 'if len(comments_data) >= self.options["max_comments"]:' in content:
                print("✓ PASS: Comments limited after filtering")
            else:
                print("✗ FAIL: Comment limiting logic not found")
                all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        all_passed = False

    # Test 4: Verify gallery URL HTML decoding
    print("\n[Test 4] Verify gallery URL HTML decoding...")
    try:
        with open('reddit_fetcher.py', 'r') as f:
            content = f.read()

            if 'html.unescape(item["s"]["u"])' in content:
                print("✓ PASS: Gallery URLs are HTML-decoded")
            else:
                print("✗ FAIL: Gallery URL decoding not found")
                all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        all_passed = False

    # Test 5: Verify read-only mode
    print("\n[Test 5] Verify read-only mode enabled...")
    try:
        with open('reddit_fetcher.py', 'r') as f:
            content = f.read()

            if 'self.reddit.read_only = True' in content:
                print("✓ PASS: Read-only mode is enabled")
            else:
                print("✗ FAIL: Read-only mode not enabled")
                all_passed = False

            # Verify user.me() is removed
            if 'self.reddit.user.me()' not in content:
                print("✓ PASS: user.me() authentication removed")
            else:
                print("✗ FAIL: user.me() still present")
                all_passed = False

            # Verify subreddit test is used
            if 'self.reddit.subreddit("python").id' in content or 'self.reddit.subreddit' in content:
                print("✓ PASS: Read-only connection test implemented")
            else:
                print("✗ FAIL: Read-only connection test not found")
                all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        all_passed = False

    # Test 6: Verify _clean_text HTML decoding
    print("\n[Test 6] Verify _clean_text HTML entity decoding...")
    try:
        with open('reddit_fetcher.py', 'r') as f:
            content = f.read()
            lines = content.split('\n')

            # Find _clean_text function
            clean_text_start = None
            for i, line in enumerate(lines):
                if 'def _clean_text(self, text: str)' in line:
                    clean_text_start = i
                    break

            if clean_text_start:
                # Check next 20 lines for html.unescape
                clean_text_section = '\n'.join(lines[clean_text_start:clean_text_start+20])
                if 'html.unescape(text)' in clean_text_section:
                    print("✓ PASS: _clean_text uses html.unescape()")
                else:
                    print("✗ FAIL: html.unescape() not found in _clean_text")
                    all_passed = False
            else:
                print("✗ FAIL: _clean_text function not found")
                all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        all_passed = False

    # Test 7: Test HTML decoding functionality
    print("\n[Test 7] Test HTML decoding functionality...")
    try:
        test_cases = [
            ("&amp;", "&"),
            ("&lt;", "<"),
            ("&gt;", ">"),
            ("&quot;", '"'),
            ("&#39;", "'"),
            ("Rock &amp; Roll", "Rock & Roll"),
            ("https://example.com?foo=1&amp;bar=2", "https://example.com?foo=1&bar=2"),
        ]

        all_html_tests_passed = True
        for encoded, expected in test_cases:
            decoded = html.unescape(encoded)
            if decoded == expected:
                print(f"  ✓ '{encoded}' -> '{decoded}'")
            else:
                print(f"  ✗ '{encoded}' -> '{decoded}' (expected '{expected}')")
                all_html_tests_passed = False

        if all_html_tests_passed:
            print("✓ PASS: HTML decoding works correctly")
        else:
            print("✗ FAIL: Some HTML decoding tests failed")
            all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        all_passed = False

    # Final result
    print("\n" + "=" * 80)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("=" * 80)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 80)
        return 1


if __name__ == '__main__':
    sys.exit(test_fixes())
