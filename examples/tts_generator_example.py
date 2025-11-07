#!/usr/bin/env python3
"""
TTS Generator Example Script

Demonstrates how to use the TTSGenerator module to convert
video scripts into audio narration files.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tts_generator import TTSGenerator, generate_audio_from_script, TTSError
from tts_config import TTS_PROVIDERS


def create_sample_script():
    """Create sample video script for demonstration"""
    return {
        "metadata": {
            "post_id": "test123",
            "title": "TIL that octopuses have three hearts",
            "subreddit": "todayilearned",
            "format_type": "short",
        },
        "segments": [
            {
                "name": "intro",
                "type": "intro",
                "start_time": 0.0,
                "end_time": 3.0,
                "duration": 3.0,
                "narration": "Check out this amazing fact from Reddit!",
            },
            {
                "name": "title",
                "type": "title",
                "start_time": 3.0,
                "end_time": 8.0,
                "duration": 5.0,
                "narration": "Today I learned that octopuses have three hearts and blue blood.",
            },
            {
                "name": "body",
                "type": "post_body",
                "start_time": 8.0,
                "end_time": 23.0,
                "duration": 15.0,
                "narration": "Two hearts pump blood to the gills, while the third pumps blood to the rest of the body. Their blood is blue because it contains copper-based hemocyanin instead of iron-based hemoglobin!",
            },
            {
                "name": "outro",
                "type": "outro",
                "start_time": 23.0,
                "end_time": 26.0,
                "duration": 3.0,
                "narration": "Thanks for watching! Like and subscribe for more!",
            },
        ],
        "total_duration": 26.0,
        "word_count": 65,
    }


def example_1_basic_tts():
    """Example 1: Basic TTS generation with gTTS"""
    print("\n" + "=" * 60)
    print("Example 1: Basic TTS with gTTS (Free)")
    print("=" * 60)

    try:
        # Create generator
        generator = TTSGenerator(provider="gtts", voice="default")

        # Generate single audio file
        text = "Hello from Reddit! This is a test of text to speech."
        output_file = "/tmp/tts_test_basic.mp3"

        audio_path = generator.generate_audio(text, output_file)
        print(f"\n✓ Audio generated: {audio_path}")

        # Check file size
        file_size = os.path.getsize(audio_path)
        print(f"  File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

    except TTSError as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def example_2_generate_from_script():
    """Example 2: Generate audio from complete script"""
    print("\n" + "=" * 60)
    print("Example 2: Generate Audio from Complete Script")
    print("=" * 60)

    try:
        generator = TTSGenerator(provider="gtts")
        script = create_sample_script()

        # Generate audio for all segments
        output_dir = "/tmp/tts_script_audio"
        audio_files = generator.generate_from_script(script, output_dir)

        # Print summary
        print(generator.get_generation_summary(audio_files))

        # Export manifest
        manifest_path = f"{output_dir}/audio_manifest.json"
        generator.export_audio_manifest(audio_files, manifest_path)

    except Exception as e:
        print(f"✗ Error: {e}")


def example_3_different_providers():
    """Example 3: Try different TTS providers"""
    print("\n" + "=" * 60)
    print("Example 3: Different TTS Providers")
    print("=" * 60)

    text = "This is a test of different text to speech providers."
    providers_to_try = ["gtts", "pyttsx3"]

    for provider in providers_to_try:
        print(f"\n{provider.upper()}:")
        print("-" * 40)

        try:
            generator = TTSGenerator(provider=provider)
            output_file = f"/tmp/tts_test_{provider}.mp3"

            audio_path = generator.generate_audio(text, output_file)

            file_size = os.path.getsize(audio_path)
            print(f"✓ Generated: {audio_path}")
            print(f"  Size: {file_size:,} bytes")

        except TTSError as e:
            print(f"⚠ {provider}: {e}")
        except Exception as e:
            print(f"✗ {provider} failed: {e}")


def example_4_voice_variations():
    """Example 4: Test different voice settings"""
    print("\n" + "=" * 60)
    print("Example 4: Voice Variations (gTTS)")
    print("=" * 60)

    text = "The quick brown fox jumps over the lazy dog."

    # Try different accents with gTTS
    accents = [
        ("com", "US English"),
        ("co.uk", "British English"),
        ("com.au", "Australian English"),
        ("ca", "Canadian English"),
    ]

    for tld, description in accents:
        print(f"\n{description}:")
        try:
            from gtts import gTTS

            tts = gTTS(text=text, lang="en", tld=tld)
            output_file = f"/tmp/tts_accent_{tld.replace('.', '_')}.mp3"
            tts.save(output_file)

            print(f"✓ Generated: {output_file}")

        except Exception as e:
            print(f"✗ Failed: {e}")


def example_5_caching():
    """Example 5: Demonstrate audio caching"""
    print("\n" + "=" * 60)
    print("Example 5: Audio Caching")
    print("=" * 60)

    text = "This audio will be cached for faster regeneration."
    output_file = "/tmp/tts_cache_test.mp3"

    try:
        # Enable caching
        generator = TTSGenerator(
            provider="gtts",
            options={"cache_audio": True, "cache_dir": "/tmp/tts_cache_demo"}
        )

        # First generation
        print("\nFirst generation (no cache):")
        import time

        start = time.time()
        audio_path = generator.generate_audio(text, output_file, "test_segment")
        duration1 = time.time() - start
        print(f"  Time: {duration1:.2f} seconds")

        # Second generation (cached)
        print("\nSecond generation (cached):")
        start = time.time()
        audio_path = generator.generate_audio(text, output_file, "test_segment")
        duration2 = time.time() - start
        print(f"  Time: {duration2:.2f} seconds")

        speedup = duration1 / duration2 if duration2 > 0 else 0
        print(f"\n✓ Speedup: {speedup:.1f}x faster")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_6_full_workflow():
    """Example 6: Complete workflow from script to audio"""
    print("\n" + "=" * 60)
    print("Example 6: Complete Workflow")
    print("=" * 60)

    try:
        # Step 1: Load or create script
        print("\n1. Creating video script...")
        script = create_sample_script()
        print(f"   ✓ Script loaded: {len(script['segments'])} segments")

        # Step 2: Initialize TTS generator
        print("\n2. Initializing TTS generator...")
        generator = TTSGenerator(provider="gtts", voice="default")
        print(f"   ✓ Using provider: {generator.provider}")

        # Step 3: Generate audio files
        print("\n3. Generating audio files...")
        output_dir = "/tmp/tts_workflow"
        audio_files = generator.generate_from_script(script, output_dir)
        print(f"   ✓ Generated {len(audio_files)} audio files")

        # Step 4: Export manifest
        print("\n4. Exporting audio manifest...")
        manifest_path = f"{output_dir}/manifest.json"
        generator.export_audio_manifest(audio_files, manifest_path)

        # Step 5: Display summary
        print("\n5. Generation Summary:")
        print(generator.get_generation_summary(audio_files))

        print(f"\n✓ Complete! Audio files saved to: {output_dir}")
        print(f"  - Audio files: {len(audio_files)}")
        print(f"  - Manifest: {manifest_path}")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()


def example_7_integration_with_script_generator():
    """Example 7: Integration with Script Generator"""
    print("\n" + "=" * 60)
    print("Example 7: Integration with Script Generator")
    print("=" * 60)

    print("\nThis example shows integration with ScriptGenerator:")
    print("""
# Generate script from Reddit post
from reddit_fetcher import RedditFetcher
from script_generator import ScriptGenerator
from tts_generator import TTSGenerator

# Fetch post
fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

# Generate script
script_gen = ScriptGenerator()
script = script_gen.generate_script(post_data, format_type="medium")

# Generate audio
tts_gen = TTSGenerator(provider="gtts")
audio_files = tts_gen.generate_from_script(script, "./audio_output")

# Export
tts_gen.export_audio_manifest(audio_files, "audio_manifest.json")

print("✓ Complete pipeline: Reddit → Script → Audio!")
""")

    # Try to actually run it
    try:
        from script_generator import ScriptGenerator

        print("\n✓ ScriptGenerator is available!")

        # Create a simple script
        script_gen = ScriptGenerator()

        # Create mock post data
        mock_post = {
            "id": "test",
            "title": "Test Title",
            "author": "test_user",
            "subreddit": "test",
            "body": "This is a test post.",
            "comments": [],
        }

        script = script_gen.generate_script(mock_post, format_type="short")

        # Generate audio
        tts_gen = TTSGenerator(provider="gtts")
        audio_files = tts_gen.generate_from_script(script, "/tmp/tts_integration")

        print(f"\n✓ Generated {len(audio_files)} audio files from script!")

    except ImportError:
        print("\n⚠ ScriptGenerator not available")
    except Exception as e:
        print(f"\n⚠ Integration test error: {e}")


def example_8_provider_comparison():
    """Example 8: Compare TTS providers"""
    print("\n" + "=" * 60)
    print("Example 8: TTS Provider Comparison")
    print("=" * 60)

    print("\nAvailable TTS Providers:\n")

    for provider, config in TTS_PROVIDERS.items():
        print(f"{provider.upper()}:")
        print(f"  Name: {config['name']}")
        print(f"  Quality: {config['quality']}")
        print(f"  Cost: {config['cost']}")
        print(f"  Requires API Key: {config['requires_api_key']}")
        print(f"  Languages: {len(config['languages'])} supported")
        print()


def example_9_error_handling():
    """Example 9: Error handling"""
    print("\n" + "=" * 60)
    print("Example 9: Error Handling")
    print("=" * 60)

    # Test 1: Invalid provider
    print("\nTest 1: Invalid provider")
    try:
        generator = TTSGenerator(provider="invalid_provider")
        print("✗ Should have raised ProviderNotFoundError")
    except TTSError as e:
        print(f"✓ Correctly raised error: {type(e).__name__}")

    # Test 2: Missing API key (if applicable)
    print("\nTest 2: Provider requiring API key")
    try:
        generator = TTSGenerator(provider="google_cloud")
        print("⚠ API key available or check skipped")
    except TTSError as e:
        print(f"✓ Correctly raised error: {type(e).__name__}")


def example_10_convenience_function():
    """Example 10: Use convenience function"""
    print("\n" + "=" * 60)
    print("Example 10: Convenience Function")
    print("=" * 60)

    try:
        script = create_sample_script()

        # Use convenience function
        audio_files = generate_audio_from_script(
            script, provider="gtts", output_dir="/tmp/tts_convenience"
        )

        print(f"\n✓ Generated {len(audio_files)} audio files")
        print("  Files:")
        for audio in audio_files:
            print(f"    - {audio['segment_name']}: {audio['audio_path']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def interactive_mode():
    """Interactive TTS generation"""
    print("\n" + "=" * 60)
    print("Interactive TTS Generator")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("1. Generate audio from text")
        print("2. Generate audio from script")
        print("3. List available providers")
        print("4. Compare providers")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            text = input("Enter text to convert: ").strip()
            if text:
                try:
                    generator = TTSGenerator(provider="gtts")
                    output_file = "/tmp/tts_interactive.mp3"
                    audio_path = generator.generate_audio(text, output_file)
                    print(f"✓ Audio generated: {audio_path}")
                except Exception as e:
                    print(f"✗ Error: {e}")

        elif choice == "2":
            script = create_sample_script()
            try:
                generator = TTSGenerator(provider="gtts")
                audio_files = generator.generate_from_script(
                    script, "/tmp/tts_interactive_script"
                )
                print(generator.get_generation_summary(audio_files))
            except Exception as e:
                print(f"✗ Error: {e}")

        elif choice == "3":
            print("\nAvailable providers:")
            for provider in TTS_PROVIDERS.keys():
                print(f"  - {provider}")

        elif choice == "4":
            example_8_provider_comparison()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


def main():
    """Run all examples or specific ones"""
    print("=" * 60)
    print("TTS Generator Examples")
    print("=" * 60)

    print("\nAvailable examples:")
    print("1. Basic TTS generation")
    print("2. Generate from script")
    print("3. Different providers")
    print("4. Voice variations")
    print("5. Audio caching")
    print("6. Full workflow")
    print("7. Script Generator integration")
    print("8. Provider comparison")
    print("9. Error handling")
    print("10. Convenience function")
    print("11. Interactive mode")
    print("0. Run all examples (1-10)")

    choice = input("\nSelect example to run (0-11): ").strip()

    if choice == "1":
        example_1_basic_tts()
    elif choice == "2":
        example_2_generate_from_script()
    elif choice == "3":
        example_3_different_providers()
    elif choice == "4":
        example_4_voice_variations()
    elif choice == "5":
        example_5_caching()
    elif choice == "6":
        example_6_full_workflow()
    elif choice == "7":
        example_7_integration_with_script_generator()
    elif choice == "8":
        example_8_provider_comparison()
    elif choice == "9":
        example_9_error_handling()
    elif choice == "10":
        example_10_convenience_function()
    elif choice == "11":
        interactive_mode()
    elif choice == "0":
        example_1_basic_tts()
        example_2_generate_from_script()
        example_3_different_providers()
        example_4_voice_variations()
        example_5_caching()
        example_6_full_workflow()
        example_7_integration_with_script_generator()
        example_8_provider_comparison()
        example_9_error_handling()
        example_10_convenience_function()
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
