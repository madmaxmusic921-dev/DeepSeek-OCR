#!/usr/bin/env python3
"""
Debug script to identify issues in reddit_fetcher.py
"""

import ast
import re

def analyze_reddit_fetcher():
    """Analyze reddit_fetcher.py for potential bugs."""

    issues_found = []

    with open('reddit_fetcher.py', 'r') as f:
        content = f.read()
        lines = content.split('\n')

    # Issue 1: Comment depth attribute doesn't exist on flattened comment list
    if 'comment.depth if hasattr(comment, "depth")' in content:
        issue = {
            'line': 337,
            'severity': 'HIGH',
            'type': 'Logic Error',
            'description': 'comment.depth does not exist on comments from comments.list(). This will always return 0.',
            'code': lines[336].strip(),
            'fix': 'Remove depth tracking or use comment tree structure instead of list()'
        }
        issues_found.append(issue)

    # Issue 2: Comment filtering happens after limiting
    for i, line in enumerate(lines):
        if 'for comment in submission.comments.list()[: self.options["max_comments"]]' in line:
            # Check if filtering happens inside the loop
            if i + 5 < len(lines) and 'if comment.score <' in lines[i + 5]:
                issue = {
                    'line': i + 1,
                    'severity': 'MEDIUM',
                    'type': 'Logic Error',
                    'description': 'Comments are filtered by score AFTER limiting to max_comments. This means you might get fewer than max_comments if some are filtered out.',
                    'code': lines[i].strip(),
                    'fix': 'Fetch more comments than max_comments and filter, then limit the results'
                }
                issues_found.append(issue)

    # Issue 3: Gallery URL might be HTML encoded
    if 'media_info["urls"].append(item["s"]["u"])' in content:
        issue = {
            'line': 303,
            'severity': 'LOW',
            'type': 'Potential Bug',
            'description': 'Gallery URLs from Reddit API might be HTML-encoded (e.g., &amp; instead of &)',
            'code': 'media_info["urls"].append(item["s"]["u"])',
            'fix': 'Use html.unescape() to decode URLs'
        }
        issues_found.append(issue)

    # Issue 4: Authentication check will fail for read-only apps
    if 'self.reddit.user.me()' in content:
        issue = {
            'line': 92,
            'severity': 'MEDIUM',
            'type': 'Authentication Issue',
            'description': 'user.me() requires user authentication and will fail for read-only/script apps',
            'code': lines[91].strip(),
            'fix': 'Use self.reddit.read_only = True or test connection differently'
        }
        issues_found.append(issue)

    # Issue 5: Comment sort should be set before replace_more
    extract_comments_start = None
    for i, line in enumerate(lines):
        if 'def _extract_comments' in line:
            extract_comments_start = i
        if extract_comments_start and 'submission.comment_sort =' in line:
            comment_sort_line = i
        if extract_comments_start and 'replace_more' in line:
            replace_more_line = i
            # Check order - this is actually correct in the code
            break

    # Issue 6: No HTML entity decoding for text
    if 'def _clean_text' in content and 'html.unescape' not in content:
        issue = {
            'line': 358,
            'severity': 'LOW',
            'type': 'Missing Feature',
            'description': '_clean_text() does not decode HTML entities (e.g., &amp;, &lt;, &gt;)',
            'code': 'def _clean_text(self, text: str) -> str:',
            'fix': 'Add html.unescape() to handle HTML entities in text'
        }
        issues_found.append(issue)

    return issues_found


if __name__ == '__main__':
    print("=" * 80)
    print("REDDIT FETCHER DEBUG ANALYSIS")
    print("=" * 80)

    issues = analyze_reddit_fetcher()

    if not issues:
        print("\n✓ No issues found!")
    else:
        print(f"\n⚠ Found {len(issues)} potential issues:\n")

        for i, issue in enumerate(issues, 1):
            print(f"{i}. [{issue['severity']}] {issue['type']} at line {issue['line']}")
            print(f"   Description: {issue['description']}")
            print(f"   Code: {issue['code']}")
            print(f"   Fix: {issue['fix']}")
            print()

    print("=" * 80)
    print("DETAILED ANALYSIS")
    print("=" * 80)

    print("\n1. COMMENT DEPTH ISSUE (Line 337)")
    print("-" * 80)
    print("The code tries to get 'depth' from comments in a flattened list:")
    print("  comment.depth if hasattr(comment, 'depth') else 0")
    print("\nProblem:")
    print("  - comments.list() returns a flattened list of comments")
    print("  - The 'depth' attribute doesn't exist on these comment objects")
    print("  - This will always return 0")
    print("\nSolution:")
    print("  - Use comment tree structure: for comment in submission.comments:")
    print("  - Or calculate depth manually by parsing parent_id")

    print("\n2. COMMENT FILTERING LOGIC (Line 321-326)")
    print("-" * 80)
    print("The code limits comments BEFORE filtering by score:")
    print("  for comment in submission.comments.list()[:self.options['max_comments']]:")
    print("    if comment.score < self.options['min_comment_score']:")
    print("      continue")
    print("\nProblem:")
    print("  - If max_comments=10 but 5 have low scores, you only get 5 comments")
    print("  - The user expects 10 high-scoring comments, not '10 comments then filter'")
    print("\nSolution:")
    print("  - Fetch more comments (e.g., max_comments * 3)")
    print("  - Filter by score")
    print("  - Then limit to max_comments")

    print("\n3. HTML ENCODING (Line 303, 358)")
    print("-" * 80)
    print("URLs and text from Reddit API might contain HTML entities:")
    print("  - Gallery URLs: &amp; instead of &")
    print("  - Text content: &lt;, &gt;, &quot;, etc.")
    print("\nProblem:")
    print("  - These entities are not decoded")
    print("  - Can cause issues with URL requests or text display")
    print("\nSolution:")
    print("  - import html")
    print("  - Use html.unescape(url) for gallery URLs")
    print("  - Use html.unescape(text) in _clean_text()")

    print("\n4. READ-ONLY AUTHENTICATION (Line 92)")
    print("-" * 80)
    print("The code calls self.reddit.user.me() to test connection:")
    print("\nProblem:")
    print("  - This requires user authentication (OAuth2)")
    print("  - Read-only apps with just client_id/secret will fail")
    print("  - Most Reddit post fetching doesn't need user auth")
    print("\nSolution:")
    print("  - Use self.reddit.read_only = True")
    print("  - Or test with a simple subreddit fetch instead")
    print("  - Or catch the exception and continue for read-only mode")

    print("\n" + "=" * 80)
