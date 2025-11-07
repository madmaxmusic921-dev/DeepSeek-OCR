#!/usr/bin/env python3
"""
Complete Reddit-to-Video Pipeline Example

This script demonstrates the complete automation workflow:
1. Fetch a Reddit post
2. Generate a video script
3. Create audio narration
4. Compose the final video

Usage:
    python reddit_to_video.py <post_id> [options]
    python reddit_to_video.py abc123 --format youtube --style casual
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reddit_fetcher import RedditFetcher, RedditFetcherError
from script_generator import ScriptGenerator
from tts_generator import TTSGenerator
from video_composer import VideoComposer


class RedditToVideoError(Exception):
    """Base exception for Reddit to Video pipeline"""
    pass


class RedditToVideo:
    """
    Complete Reddit-to-Video automation pipeline.

    Converts a Reddit post into a finished video ready for upload.
    """

    def __init__(
        self,
        video_format: str = "youtube",
        narration_style: str = "casual",
        tts_provider: str = "gtts",
        output_dir: str = "./output"
    ):
        """
        Initialize the pipeline.

        Args:
            video_format: Video format (tiktok, instagram, youtube, etc.)
            narration_style: Script style (casual, formal, dramatic, comedic)
            tts_provider: TTS provider (gtts, pyttsx3, google_cloud, etc.)
            output_dir: Directory for output files
        """
        self.video_format = video_format
        self.narration_style = narration_style
        self.tts_provider = tts_provider
        self.output_dir = Path(output_dir)

        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir = self.output_dir / "audio"
        self.audio_dir.mkdir(exist_ok=True)

        # Initialize modules
        print("Initializing pipeline modules...")
        self.reddit_fetcher = None
        self.script_generator = ScriptGenerator()
        self.tts_generator = TTSGenerator(provider=tts_provider)
        self.video_composer = VideoComposer(format_type=video_format)
        print("✓ Pipeline initialized")

    def process_post(
        self,
        post_id: str = None,
        post_url: str = None,
        background_music: str = None
    ) -> dict:
        """
        Process a Reddit post into a complete video.

        Args:
            post_id: Reddit post ID (e.g., "abc123")
            post_url: Reddit post URL (alternative to post_id)
            background_music: Optional path to background music

        Returns:
            Dictionary with paths to all generated files

        Raises:
            RedditToVideoError: If processing fails
        """
        try:
            # Step 1: Fetch Reddit post
            print("\n" + "=" * 60)
            print("STEP 1: Fetching Reddit Post")
            print("=" * 60)

            post_data = self._fetch_post(post_id, post_url)
            print(f"✓ Fetched: {post_data['title'][:60]}...")
            print(f"  Subreddit: r/{post_data['subreddit']}")
            print(f"  Score: {post_data.get('score', 0):,}")
            print(f"  Comments: {post_data.get('num_comments', 0)}")

            # Step 2: Generate video script
            print("\n" + "=" * 60)
            print("STEP 2: Generating Video Script")
            print("=" * 60)

            script = self._generate_script(post_data)
            print(f"✓ Script generated")
            print(f"  Format: {self.video_format}")
            print(f"  Duration: {script['total_duration']:.1f} seconds")
            print(f"  Segments: {len(script['segments'])}")
            print(f"  Words: {script['word_count']}")

            # Save script
            script_path = self._save_script(script, post_data)
            print(f"  Saved: {script_path}")

            # Step 3: Generate audio narration
            print("\n" + "=" * 60)
            print("STEP 3: Generating Audio Narration")
            print("=" * 60)

            audio_files = self._generate_audio(script)
            print(f"✓ Audio generated: {len(audio_files)} files")

            # Save manifest
            manifest_path = self._save_audio_manifest(audio_files, post_data)
            print(f"  Manifest: {manifest_path}")

            # Step 4: Compose final video
            print("\n" + "=" * 60)
            print("STEP 4: Composing Final Video")
            print("=" * 60)

            video_path = self._compose_video(script, audio_files, post_data, background_music)
            print(f"✓ Video rendered: {video_path}")

            # Step 5: Generate thumbnail
            print("\n" + "=" * 60)
            print("STEP 5: Generating Thumbnail")
            print("=" * 60)

            thumbnail_path = self._generate_thumbnail(script, post_data)
            print(f"✓ Thumbnail created: {thumbnail_path}")

            # Return results
            results = {
                "post_data": post_data,
                "script_path": str(script_path),
                "audio_files": audio_files,
                "audio_manifest": str(manifest_path),
                "video_path": str(video_path),
                "thumbnail_path": str(thumbnail_path),
            }

            self._print_summary(results, script)

            return results

        except Exception as e:
            raise RedditToVideoError(f"Pipeline failed: {e}")

    def _fetch_post(self, post_id: str = None, post_url: str = None) -> dict:
        """Fetch Reddit post data"""
        if not self.reddit_fetcher:
            self.reddit_fetcher = RedditFetcher()

        if post_url:
            return self.reddit_fetcher.fetch_post_by_url(post_url)
        elif post_id:
            return self.reddit_fetcher.fetch_post_by_id(post_id)
        else:
            raise RedditToVideoError("Either post_id or post_url must be provided")

    def _generate_script(self, post_data: dict) -> dict:
        """Generate video script"""
        # Determine format type from video format
        if self.video_format in ["tiktok", "youtube_shorts"]:
            format_type = "short"
        elif self.video_format in ["instagram", "facebook"]:
            format_type = "medium"
        else:
            format_type = "long"

        return self.script_generator.generate_script(
            post_data,
            format_type=format_type,
            narration_style=self.narration_style
        )

    def _generate_audio(self, script: dict) -> list:
        """Generate audio narration"""
        return self.tts_generator.generate_from_script(
            script,
            str(self.audio_dir)
        )

    def _compose_video(
        self,
        script: dict,
        audio_files: list,
        post_data: dict,
        background_music: str = None
    ) -> Path:
        """Compose final video"""
        # Generate filename
        filename = self._generate_filename(post_data, "mp4")
        video_path = self.output_dir / filename

        # Compose video
        self.video_composer.compose_video(
            script,
            audio_files,
            str(video_path),
            background_music
        )

        return video_path

    def _generate_thumbnail(self, script: dict, post_data: dict) -> Path:
        """Generate video thumbnail"""
        filename = self._generate_filename(post_data, "jpg", suffix="_thumbnail")
        thumbnail_path = self.output_dir / filename

        self.video_composer.generate_thumbnail(script, str(thumbnail_path))

        return thumbnail_path

    def _save_script(self, script: dict, post_data: dict) -> Path:
        """Save script to JSON file"""
        import json

        filename = self._generate_filename(post_data, "json", suffix="_script")
        script_path = self.output_dir / filename

        with open(script_path, "w", encoding="utf-8") as f:
            json.dump(script, f, indent=2, ensure_ascii=False)

        return script_path

    def _save_audio_manifest(self, audio_files: list, post_data: dict) -> Path:
        """Save audio manifest"""
        filename = self._generate_filename(post_data, "json", suffix="_audio_manifest")
        manifest_path = self.output_dir / filename

        self.tts_generator.export_audio_manifest(audio_files, str(manifest_path))

        return manifest_path

    def _generate_filename(
        self,
        post_data: dict,
        extension: str,
        suffix: str = ""
    ) -> str:
        """Generate output filename"""
        subreddit = post_data.get("subreddit", "reddit")
        post_id = post_data.get("id", "post")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Clean subreddit name
        subreddit = subreddit.replace(" ", "_").lower()

        return f"{subreddit}_{post_id}{suffix}.{extension}"

    def _print_summary(self, results: dict, script: dict):
        """Print pipeline summary"""
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE!")
        print("=" * 60)

        print(f"\nTitle: {results['post_data']['title']}")
        print(f"Subreddit: r/{results['post_data']['subreddit']}")
        print(f"Format: {self.video_format}")
        print(f"Duration: {script['total_duration']:.1f} seconds")

        print("\nGenerated Files:")
        print(f"  📄 Script: {results['script_path']}")
        print(f"  🎤 Audio: {len(results['audio_files'])} files")
        print(f"  🎬 Video: {results['video_path']}")
        print(f"  🖼️  Thumbnail: {results['thumbnail_path']}")

        print("\nNext Steps:")
        print("  1. Review the video")
        print("  2. Edit if needed")
        print("  3. Upload to platform")
        print("  4. Add description and tags")
        print("\n✓ Ready for upload!")


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="Convert Reddit posts into videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with post ID
  python reddit_to_video.py abc123

  # Specify format and style
  python reddit_to_video.py abc123 --format tiktok --style dramatic

  # Use post URL instead
  python reddit_to_video.py --url "https://reddit.com/r/AskReddit/comments/abc123/"

  # Add background music
  python reddit_to_video.py abc123 --music ./background.mp3

  # Use different TTS provider
  python reddit_to_video.py abc123 --tts google_cloud
        """
    )

    # Required arguments
    parser.add_argument(
        "post_id",
        nargs="?",
        help="Reddit post ID (e.g., abc123)"
    )

    # Optional arguments
    parser.add_argument(
        "--url",
        help="Reddit post URL (alternative to post_id)"
    )

    parser.add_argument(
        "--format",
        choices=["tiktok", "instagram", "youtube_shorts", "youtube", "youtube_4k", "facebook"],
        default="youtube",
        help="Video format (default: youtube)"
    )

    parser.add_argument(
        "--style",
        choices=["casual", "formal", "dramatic", "comedic"],
        default="casual",
        help="Narration style (default: casual)"
    )

    parser.add_argument(
        "--tts",
        choices=["gtts", "pyttsx3", "google_cloud", "amazon_polly", "elevenlabs"],
        default="gtts",
        help="TTS provider (default: gtts)"
    )

    parser.add_argument(
        "--music",
        help="Path to background music file"
    )

    parser.add_argument(
        "--output",
        default="./output",
        help="Output directory (default: ./output)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.post_id and not args.url:
        parser.error("Either post_id or --url must be provided")

    try:
        # Initialize pipeline
        pipeline = RedditToVideo(
            video_format=args.format,
            narration_style=args.style,
            tts_provider=args.tts,
            output_dir=args.output
        )

        # Process post
        results = pipeline.process_post(
            post_id=args.post_id,
            post_url=args.url,
            background_music=args.music
        )

        print(f"\n✓ Success! Video saved to: {results['video_path']}")

    except RedditFetcherError as e:
        print(f"\n✗ Reddit Error: {e}")
        print("\nTips:")
        print("  - Check if the post ID is correct")
        print("  - Verify Reddit API credentials in reddit_config.py")
        print("  - Ensure the post is publicly accessible")
        sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Check if running as module or script
    if len(sys.argv) > 1:
        main()
    else:
        print("Reddit-to-Video Pipeline")
        print("=" * 60)
        print("\nUsage: python reddit_to_video.py <post_id> [options]")
        print("\nFor help: python reddit_to_video.py --help")
        print("\nQuick example:")
        print("  python reddit_to_video.py abc123 --format youtube")
