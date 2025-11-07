#!/usr/bin/env python3
"""
Complete Reddit-to-Video Pipeline Example

This example demonstrates the complete workflow from Reddit post to final video.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def example_1_basic_workflow():
    """Example 1: Basic workflow with mock data"""
    print("=" * 60)
    print("Example 1: Basic Workflow (Mock Data)")
    print("=" * 60)

    # Create mock post data (simulating RedditFetcher output)
    mock_post = {
        "id": "example123",
        "title": "TIL that honey never spoils and can last for thousands of years",
        "author": "science_fan",
        "subreddit": "todayilearned",
        "url": "https://reddit.com/r/todayilearned/comments/example123/",
        "score": 25000,
        "num_comments": 350,
        "body": "Archaeologists have found 3000-year-old honey in Egyptian tombs that was still perfectly edible. Honey's low moisture content and acidic pH create an environment where bacteria cannot survive, making it one of the few foods that never spoils.",
        "comments": [
            {
                "id": "c1",
                "author": "history_buff",
                "body": "The Egyptians also used honey for embalming because of its antibacterial properties!",
                "score": 5000,
            },
            {
                "id": "c2",
                "author": "bee_keeper",
                "body": "Fun fact: Bees add an enzyme that breaks down into hydrogen peroxide, which also helps preserve it.",
                "score": 3500,
            },
        ],
    }

    # Step 1: Generate script
    print("\n1. Generating script...")
    from script_generator import ScriptGenerator

    script_gen = ScriptGenerator()
    script = script_gen.generate_script(
        mock_post,
        format_type="medium",
        narration_style="casual"
    )

    print(f"   ✓ Script created")
    print(f"     - Duration: {script['total_duration']:.1f}s")
    print(f"     - Segments: {len(script['segments'])}")
    print(f"     - Words: {script['word_count']}")

    # Step 2: Generate audio (with note about environment)
    print("\n2. Generating audio...")
    print("   ⚠ Audio generation requires proper TTS setup")
    print("   ⚠ Skipping in this example environment")

    # Step 3: Compose video (with note about environment)
    print("\n3. Composing video...")
    print("   ⚠ Video composition requires MoviePy and FFmpeg")
    print("   ⚠ Skipping in this example environment")

    print("\n✓ Workflow structure demonstrated")
    print("  In a proper environment, this would create:")
    print("  - Audio files (7 segments)")
    print("  - Final video (1920x1080, ~67 seconds)")
    print("  - Thumbnail image (1280x720)")


def example_2_with_reddit_fetcher():
    """Example 2: Complete workflow with Reddit fetcher"""
    print("\n" + "=" * 60)
    print("Example 2: Complete Workflow (With Reddit)")
    print("=" * 60)

    print("\nThis example shows the complete pipeline:")
    print("""
from reddit_fetcher import RedditFetcher
from script_generator import ScriptGenerator
from tts_generator import TTSGenerator
from video_composer import VideoComposer

# Step 1: Fetch Reddit post
print("Fetching Reddit post...")
fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

# Step 2: Generate script
print("Generating script...")
script_gen = ScriptGenerator()
script = script_gen.generate_script(post_data, format_type="medium")

# Step 3: Generate audio
print("Generating audio...")
tts_gen = TTSGenerator(provider="gtts")
audio_files = tts_gen.generate_from_script(script, "./audio")

# Step 4: Compose video
print("Composing video...")
composer = VideoComposer(format_type="youtube")
video_path = composer.compose_video(
    script,
    audio_files,
    "final_video.mp4"
)

# Step 5: Generate thumbnail
thumbnail = composer.generate_thumbnail(script, "thumbnail.jpg")

print(f"✓ Complete! Video: {video_path}")
    """)

    print("⚠ Note: Requires Reddit API credentials and TTS/video dependencies")


def example_3_different_formats():
    """Example 3: Generate videos for different platforms"""
    print("\n" + "=" * 60)
    print("Example 3: Multiple Platform Formats")
    print("=" * 60)

    print("\nGenerate videos for different platforms:")
    print("""
from reddit_fetcher import RedditFetcher
from script_generator import ScriptGenerator
from tts_generator import TTSGenerator
from video_composer import VideoComposer

# Fetch post
fetcher = RedditFetcher()
post = fetcher.fetch_post_by_id("abc123")

# Generate scripts for different formats
script_gen = ScriptGenerator()
tts_gen = TTSGenerator(provider="gtts")

platforms = {
    "tiktok": "short",
    "instagram": "medium",
    "youtube": "long"
}

for platform, format_type in platforms.items():
    print(f"Creating {platform} video...")

    # Generate script
    script = script_gen.generate_script(post, format_type=format_type)

    # Generate audio
    audio = tts_gen.generate_from_script(script, f"./audio_{platform}")

    # Compose video
    composer = VideoComposer(format_type=platform)
    video = composer.compose_video(
        script,
        audio,
        f"{platform}_video.mp4"
    )

    print(f"✓ {platform}: {video}")

print("✓ Videos ready for TikTok, Instagram, and YouTube!")
    """)


def example_4_with_background_music():
    """Example 4: Add background music"""
    print("\n" + "=" * 60)
    print("Example 4: With Background Music")
    print("=" * 60)

    print("\nAdd background music to your video:")
    print("""
from video_composer import VideoComposer

composer = VideoComposer(format_type="youtube")

video = composer.compose_video(
    script=script,
    audio_files=audio_files,
    output_path="video_with_music.mp4",
    background_music="./music/background.mp3"  # Add music
)

# Music will be:
# - Looped to match video duration
# - Mixed at 15% volume (configurable)
# - Faded in/out smoothly
    """)


def example_5_customization():
    """Example 5: Customization options"""
    print("\n" + "=" * 60)
    print("Example 5: Customization Options")
    print("=" * 60)

    print("\nCustomize every aspect of the pipeline:")
    print("""
# Custom script options
script_gen = ScriptGenerator(options={
    "words_per_minute": 180,  # Faster speech
    "show_usernames": False,  # Hide usernames
    "max_comments": 5,  # More comments
})

# Custom TTS options
tts_gen = TTSGenerator(
    provider="google_cloud",  # Premium TTS
    voice="en-US-Neural2-C",  # Specific voice
    options={
        "cache_audio": True,  # Cache for speed
        "cache_dir": "./tts_cache"
    }
)

# Custom video options
composer = VideoComposer(
    format_type="youtube_4k",  # 4K resolution
    fps=60,  # 60 FPS
    options={
        "preset": "slow",  # Higher quality
        "threads": 8,  # More CPU cores
    }
)
    """)


def example_6_batch_processing():
    """Example 6: Batch process multiple posts"""
    print("\n" + "=" * 60)
    print("Example 6: Batch Processing")
    print("=" * 60)

    print("\nProcess multiple Reddit posts:")
    print("""
from reddit_fetcher import RedditFetcher
from script_generator import ScriptGenerator
from tts_generator import TTSGenerator
from video_composer import VideoComposer

# Initialize once
fetcher = RedditFetcher()
script_gen = ScriptGenerator()
tts_gen = TTSGenerator(provider="gtts")
composer = VideoComposer(format_type="youtube")

# Fetch top posts from subreddit
posts = fetcher.fetch_posts_from_subreddit(
    "todayilearned",
    sort_method="top",
    limit=10
)

# Process each post
for i, post in enumerate(posts, 1):
    print(f"Processing {i}/10: {post['title'][:50]}...")

    # Generate and compose
    script = script_gen.generate_script(post, format_type="medium")
    audio = tts_gen.generate_from_script(script, f"./audio/post_{i}")
    video = composer.compose_video(
        script,
        audio,
        f"./videos/video_{i}.mp4"
    )

    print(f"✓ Completed: {video}")

print("✓ Batch complete! 10 videos ready to upload!")
    """)


def example_7_error_handling():
    """Example 7: Proper error handling"""
    print("\n" + "=" * 60)
    print("Example 7: Error Handling")
    print("=" * 60)

    print("\nHandle errors gracefully:")
    print("""
from reddit_fetcher import RedditFetcher, RedditFetcherError
from script_generator import ScriptGenerator, ScriptGeneratorError
from tts_generator import TTSGenerator, TTSError
from video_composer import VideoComposer, VideoComposerError

try:
    # Fetch post
    fetcher = RedditFetcher()
    post = fetcher.fetch_post_by_id("abc123")

except RedditFetcherError as e:
    print(f"Reddit error: {e}")
    # Fallback: use mock data or skip

try:
    # Generate script
    script_gen = ScriptGenerator()
    script = script_gen.generate_script(post, format_type="medium")

except ScriptGeneratorError as e:
    print(f"Script error: {e}")
    # Fallback: use template or skip

try:
    # Generate audio
    tts_gen = TTSGenerator(provider="gtts")
    audio = tts_gen.generate_from_script(script, "./audio")

except TTSError as e:
    print(f"TTS error: {e}")
    # Fallback: try different provider or skip

try:
    # Compose video
    composer = VideoComposer(format_type="youtube")
    video = composer.compose_video(script, audio, "video.mp4")

except VideoComposerError as e:
    print(f"Video error: {e}")
    # Fallback: save data for manual editing
    """)


def example_8_using_cli():
    """Example 8: Using the CLI tool"""
    print("\n" + "=" * 60)
    print("Example 8: Using the CLI Tool")
    print("=" * 60)

    print("\nUse the command-line interface:")
    print("""
# Basic usage
python reddit_to_video.py abc123

# Specify format and style
python reddit_to_video.py abc123 --format tiktok --style dramatic

# Use URL instead of ID
python reddit_to_video.py --url "https://reddit.com/r/AskReddit/comments/abc123/"

# Add background music
python reddit_to_video.py abc123 --music ./background.mp3

# Use premium TTS
python reddit_to_video.py abc123 --tts google_cloud

# Custom output directory
python reddit_to_video.py abc123 --output ./my_videos

# All options combined
python reddit_to_video.py abc123 \\
    --format youtube_4k \\
    --style formal \\
    --tts elevenlabs \\
    --music ./music.mp3 \\
    --output ./output
    """)


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("COMPLETE PIPELINE EXAMPLES")
    print("=" * 60)

    examples = [
        ("Basic Workflow", example_1_basic_workflow),
        ("With Reddit Fetcher", example_2_with_reddit_fetcher),
        ("Multiple Formats", example_3_different_formats),
        ("Background Music", example_4_with_background_music),
        ("Customization", example_5_customization),
        ("Batch Processing", example_6_batch_processing),
        ("Error Handling", example_7_error_handling),
        ("CLI Tool", example_8_using_cli),
    ]

    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n  0. Run all examples")

    choice = input("\nSelect example (0-8): ").strip()

    if choice == "0":
        for name, func in examples:
            func()
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        examples[int(choice) - 1][1]()
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
