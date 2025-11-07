#!/usr/bin/env python3
"""
Script Generator Example Script

Demonstrates how to use the ScriptGenerator module to convert
Reddit posts into video-ready scripts with different formats and styles.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from script_generator import ScriptGenerator, generate_script
from script_templates import list_templates, get_template_info


def create_sample_post_data():
    """Create sample Reddit post data for demonstration"""
    return {
        "id": "abc123",
        "title": "TIL that octopuses have three hearts and blue blood",
        "author": "science_enthusiast",
        "subreddit": "todayilearned",
        "url": "https://reddit.com/r/todayilearned/comments/abc123/",
        "created_utc": 1699000000.0,
        "score": 15234,
        "upvote_ratio": 0.97,
        "num_comments": 456,
        "is_self": True,
        "is_video": False,
        "body": "I was reading about marine biology and discovered that octopuses have three hearts. Two pump blood to the gills, while the third pumps blood to the rest of the body. Their blood is blue because it contains copper-based hemocyanin instead of iron-based hemoglobin! This adaptation makes them perfectly suited for cold, low-oxygen environments.",
        "comments": [
            {
                "id": "comment1",
                "author": "ocean_expert",
                "body": "This is fascinating! Another cool fact: octopuses can taste with their tentacles. They have chemoreceptors on their suckers!",
                "score": 2543,
                "is_submitter": False,
            },
            {
                "id": "comment2",
                "author": "biology_student",
                "body": "I learned this in my marine biology class! The copper in their blood makes it more efficient in cold, low-oxygen environments.",
                "score": 1234,
                "is_submitter": False,
            },
            {
                "id": "comment3",
                "author": "science_enthusiast",
                "body": "Thanks everyone for the additional facts! I love learning from this community.",
                "score": 567,
                "is_submitter": True,
            },
        ],
        "awards": [
            {"name": "Gold", "count": 5},
            {"name": "Silver", "count": 23},
        ],
    }


def example_1_short_format():
    """Example 1: Generate short-form video script (TikTok/Shorts)"""
    print("\n" + "=" * 60)
    print("Example 1: Short-Form Video Script (30-60 seconds)")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_sample_post_data()

    # Generate short-form script
    script = generator.generate_script(
        post_data, format_type="short", narration_style="casual"
    )

    print(generator.get_script_summary(script))

    # Show first segment details
    if script["segments"]:
        first_segment = script["segments"][0]
        print("\nFirst Segment Details:")
        print(f"  Name: {first_segment['name']}")
        print(f"  Duration: {first_segment['duration']:.1f}s")
        print(f"  Narration: {first_segment['narration']}")


def example_2_medium_format():
    """Example 2: Generate medium-form video script (Instagram Reels)"""
    print("\n" + "=" * 60)
    print("Example 2: Medium-Form Video Script (60-90 seconds)")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_sample_post_data()

    # Generate medium-form script with formal style
    script = generator.generate_script(
        post_data, format_type="medium", narration_style="formal"
    )

    print(generator.get_script_summary(script))


def example_3_long_format():
    """Example 3: Generate long-form video script (YouTube)"""
    print("\n" + "=" * 60)
    print("Example 3: Long-Form Video Script (3+ minutes)")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_sample_post_data()

    # Generate long-form script with dramatic style
    script = generator.generate_script(
        post_data, format_type="long", narration_style="dramatic"
    )

    print(generator.get_script_summary(script))


def example_4_export_formats():
    """Example 4: Export scripts in different formats"""
    print("\n" + "=" * 60)
    print("Example 4: Exporting Scripts")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_sample_post_data()

    script = generator.generate_script(post_data, format_type="medium")

    # Export to different formats
    output_dir = "/tmp/reddit_scripts"
    os.makedirs(output_dir, exist_ok=True)

    print("\nExporting script to multiple formats...")

    # JSON export
    generator.export_script(script, f"{output_dir}/script.json", format="json")

    # Text export
    generator.export_script(script, f"{output_dir}/script.txt", format="txt")

    # SRT subtitles
    generator.export_script(script, f"{output_dir}/script.srt", format="srt")

    # WebVTT subtitles
    generator.export_script(script, f"{output_dir}/script.vtt", format="vtt")

    print(f"\n✓ All scripts exported to: {output_dir}")


def example_5_different_styles():
    """Example 5: Compare different narration styles"""
    print("\n" + "=" * 60)
    print("Example 5: Different Narration Styles")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_sample_post_data()

    styles = ["casual", "formal", "dramatic", "comedic"]

    for style in styles:
        print(f"\n{style.upper()} Style:")
        print("-" * 40)

        script = generator.generate_script(
            post_data, format_type="short", narration_style=style
        )

        # Show intro narration for comparison
        intro_segment = next(
            (s for s in script["segments"] if s["name"] == "intro"), None
        )
        if intro_segment:
            print(f"Intro: {intro_segment['narration']}")

        # Show title treatment
        title_segment = next(
            (s for s in script["segments"] if s["type"] == "title"), None
        )
        if title_segment:
            print(f"Title: {title_segment['narration']}")


def example_6_custom_options():
    """Example 6: Using custom generation options"""
    print("\n" + "=" * 60)
    print("Example 6: Custom Generation Options")
    print("=" * 60)

    # Custom options
    custom_options = {
        "words_per_minute": 180,  # Faster speech
        "show_usernames": False,  # Hide usernames
        "show_scores": False,  # Hide scores
    }

    generator = ScriptGenerator(options=custom_options)
    post_data = create_sample_post_data()

    script = generator.generate_script(post_data, format_type="medium")

    print("\nScript with custom options:")
    print(f"  Total Duration: {script['total_duration']:.1f} seconds")
    print(f"  Word Count: {script['word_count']}")

    # Show comments segment to see effect of hiding usernames
    comments_segment = next(
        (s for s in script["segments"] if s["type"] == "comments"), None
    )
    if comments_segment:
        print(f"\nComments narration (no usernames/scores):")
        print(f"  {comments_segment['narration'][:200]}...")


def example_7_subtitle_generation():
    """Example 7: Generate and preview subtitles"""
    print("\n" + "=" * 60)
    print("Example 7: Subtitle Generation")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_sample_post_data()

    script = generator.generate_script(post_data, format_type="short")

    # Generate subtitles
    subtitles = generator._generate_subtitles(script)

    print(f"\nGenerated {len(subtitles)} subtitle entries")
    print("\nFirst 3 subtitle entries:\n")

    for i, subtitle in enumerate(subtitles[:3], 1):
        start_time = generator._format_srt_time(subtitle["start"])
        end_time = generator._format_srt_time(subtitle["end"])
        print(f"{i}")
        print(f"{start_time} --> {end_time}")
        print(f"{subtitle['text']}")
        print()


def example_8_template_comparison():
    """Example 8: Compare available templates"""
    print("\n" + "=" * 60)
    print("Example 8: Available Templates")
    print("=" * 60)

    print("\nTemplate Comparison:\n")

    for template_name in list_templates():
        info = get_template_info(template_name)
        print(f"{template_name.upper()}:")
        print(f"  Segments: {info['total_segments']}")
        print(f"  Duration: ~{info['estimated_duration']} seconds")
        print(f"  Structure: {' → '.join(info['segment_names'][:3])}...")
        print()


def example_9_full_workflow():
    """Example 9: Complete workflow from post to script files"""
    print("\n" + "=" * 60)
    print("Example 9: Complete Workflow")
    print("=" * 60)

    # Step 1: Create post data (normally from RedditFetcher)
    print("\n1. Fetching Reddit post data...")
    post_data = create_sample_post_data()
    print(f"   ✓ Post ID: {post_data['id']}")
    print(f"   ✓ Title: {post_data['title'][:50]}...")

    # Step 2: Generate script
    print("\n2. Generating video script...")
    generator = ScriptGenerator()
    script = generator.generate_script(
        post_data, format_type="medium", narration_style="casual"
    )
    print(f"   ✓ Duration: {script['total_duration']:.1f}s")
    print(f"   ✓ Segments: {len(script['segments'])}")
    print(f"   ✓ Words: {script['word_count']}")

    # Step 3: Export files
    print("\n3. Exporting script files...")
    output_dir = "/tmp/reddit_video_script"
    os.makedirs(output_dir, exist_ok=True)

    generator.export_script(script, f"{output_dir}/script.json", format="json")
    generator.export_script(script, f"{output_dir}/script.txt", format="txt")
    generator.export_script(script, f"{output_dir}/subtitles.srt", format="srt")

    # Step 4: Display summary
    print("\n4. Script Summary:")
    print(generator.get_script_summary(script))

    print(f"\n✓ Workflow complete! Files saved to: {output_dir}")


def example_10_integration_with_reddit_fetcher():
    """Example 10: Integration with RedditFetcher (if available)"""
    print("\n" + "=" * 60)
    print("Example 10: Integration with RedditFetcher")
    print("=" * 60)

    print("\nThis example shows how to integrate with RedditFetcher:")
    print("""
# Fetch Reddit post
from reddit_fetcher import RedditFetcher
from script_generator import ScriptGenerator

fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

# Generate script
generator = ScriptGenerator()
script = generator.generate_script(post_data, format_type="medium")

# Export
generator.export_script(script, "video_script.json")
generator.export_script(script, "subtitles.srt", format="srt")

print("✓ Video script ready for production!")
""")

    # Try to actually run it if modules are available
    try:
        from reddit_fetcher import RedditFetcher

        print("\n✓ RedditFetcher is available!")
        print("  You can now fetch real Reddit posts and generate scripts.")
    except ImportError:
        print("\n⚠ RedditFetcher not configured with credentials yet.")
        print("  Using mock data for demonstration.")


def interactive_mode():
    """Interactive mode for script generation"""
    print("\n" + "=" * 60)
    print("Interactive Script Generator")
    print("=" * 60)

    generator = ScriptGenerator()

    while True:
        print("\nOptions:")
        print("1. Generate short-form script")
        print("2. Generate medium-form script")
        print("3. Generate long-form script")
        print("4. Compare narration styles")
        print("5. Export all formats")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            post_data = create_sample_post_data()
            script = generator.generate_script(post_data, format_type="short")
            print(generator.get_script_summary(script))

        elif choice == "2":
            post_data = create_sample_post_data()
            script = generator.generate_script(post_data, format_type="medium")
            print(generator.get_script_summary(script))

        elif choice == "3":
            post_data = create_sample_post_data()
            script = generator.generate_script(post_data, format_type="long")
            print(generator.get_script_summary(script))

        elif choice == "4":
            example_5_different_styles()

        elif choice == "5":
            post_data = create_sample_post_data()
            script = generator.generate_script(post_data, format_type="medium")

            output_dir = "/tmp/interactive_script"
            os.makedirs(output_dir, exist_ok=True)

            for fmt in ["json", "txt", "srt", "vtt"]:
                output_file = f"{output_dir}/script.{fmt}"
                generator.export_script(script, output_file, format=fmt)

            print(f"\n✓ All formats exported to: {output_dir}")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


def main():
    """Run all examples or specific ones"""
    print("=" * 60)
    print("Video Script Generator Examples")
    print("=" * 60)

    print("\nAvailable examples:")
    print("1. Short-form video script")
    print("2. Medium-form video script")
    print("3. Long-form video script")
    print("4. Export formats")
    print("5. Different narration styles")
    print("6. Custom options")
    print("7. Subtitle generation")
    print("8. Template comparison")
    print("9. Full workflow")
    print("10. RedditFetcher integration")
    print("11. Interactive mode")
    print("0. Run all examples (1-9)")

    choice = input("\nSelect example to run (0-11): ").strip()

    if choice == "1":
        example_1_short_format()
    elif choice == "2":
        example_2_medium_format()
    elif choice == "3":
        example_3_long_format()
    elif choice == "4":
        example_4_export_formats()
    elif choice == "5":
        example_5_different_styles()
    elif choice == "6":
        example_6_custom_options()
    elif choice == "7":
        example_7_subtitle_generation()
    elif choice == "8":
        example_8_template_comparison()
    elif choice == "9":
        example_9_full_workflow()
    elif choice == "10":
        example_10_integration_with_reddit_fetcher()
    elif choice == "11":
        interactive_mode()
    elif choice == "0":
        example_1_short_format()
        example_2_medium_format()
        example_3_long_format()
        example_4_export_formats()
        example_5_different_styles()
        example_6_custom_options()
        example_7_subtitle_generation()
        example_8_template_comparison()
        example_9_full_workflow()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
