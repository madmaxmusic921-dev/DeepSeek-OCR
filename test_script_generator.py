#!/usr/bin/env python3
"""
Test Script Generator Module

Validates the script generator functionality with mock data.
"""

import json
import os
from script_generator import ScriptGenerator, generate_script, ScriptGeneratorError
from script_templates import list_templates


def create_mock_post():
    """Create mock post data for testing"""
    return {
        "id": "test123",
        "title": "TIL that octopuses have three hearts and blue blood",
        "author": "test_user",
        "subreddit": "todayilearned",
        "url": "https://reddit.com/r/todayilearned/comments/test123/",
        "score": 15234,
        "num_comments": 456,
        "body": "Octopuses have three hearts. Two pump blood to the gills, while the third pumps blood to the rest of the body. Their blood is blue because it contains copper-based hemocyanin.",
        "comments": [
            {
                "id": "c1",
                "author": "commenter1",
                "body": "This is fascinating!",
                "score": 2543,
                "is_submitter": False,
            },
            {
                "id": "c2",
                "author": "commenter2",
                "body": "I learned this in biology class!",
                "score": 1234,
                "is_submitter": False,
            },
        ],
        "awards": [{"name": "Gold", "count": 5}],
    }


def test_basic_functionality():
    """Test basic script generation"""
    print("=" * 60)
    print("Test 1: Basic Functionality")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_mock_post()

    try:
        script = generator.generate_script(post_data, format_type="medium")
        print(f"✓ Script generated successfully")
        print(f"  Duration: {script['total_duration']:.1f}s")
        print(f"  Segments: {len(script['segments'])}")
        print(f"  Word count: {script['word_count']}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_all_formats():
    """Test all video formats"""
    print("\n" + "=" * 60)
    print("Test 2: All Video Formats")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_mock_post()
    formats = ["short", "medium", "long"]

    all_passed = True
    for fmt in formats:
        try:
            script = generator.generate_script(post_data, format_type=fmt)
            print(f"✓ {fmt.upper():7} format: {script['total_duration']:.1f}s, {len(script['segments'])} segments")
        except Exception as e:
            print(f"✗ {fmt.upper():7} format failed: {e}")
            all_passed = False

    return all_passed


def test_narration_styles():
    """Test all narration styles"""
    print("\n" + "=" * 60)
    print("Test 3: Narration Styles")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_mock_post()
    styles = ["casual", "formal", "dramatic", "comedic"]

    all_passed = True
    for style in styles:
        try:
            script = generator.generate_script(
                post_data, format_type="short", narration_style=style
            )
            intro = script["segments"][0]["narration"] if script["segments"] else ""
            print(f"✓ {style.capitalize():10} style: {intro[:50]}...")
        except Exception as e:
            print(f"✗ {style.capitalize():10} style failed: {e}")
            all_passed = False

    return all_passed


def test_export_formats():
    """Test all export formats"""
    print("\n" + "=" * 60)
    print("Test 4: Export Formats")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_mock_post()
    script = generator.generate_script(post_data, format_type="medium")

    output_dir = "/tmp/test_script_export"
    os.makedirs(output_dir, exist_ok=True)

    formats = ["json", "txt", "srt", "vtt"]
    all_passed = True

    for fmt in formats:
        try:
            output_file = f"{output_dir}/test_script.{fmt}"
            generator.export_script(script, output_file, format=fmt)

            # Check file exists and has content
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                size = os.path.getsize(output_file)
                print(f"✓ {fmt.upper():4} export: {output_file} ({size} bytes)")
            else:
                print(f"✗ {fmt.upper():4} export: File not created or empty")
                all_passed = False
        except Exception as e:
            print(f"✗ {fmt.upper():4} export failed: {e}")
            all_passed = False

    return all_passed


def test_subtitle_generation():
    """Test subtitle generation"""
    print("\n" + "=" * 60)
    print("Test 5: Subtitle Generation")
    print("=" * 60)

    generator = ScriptGenerator()
    post_data = create_mock_post()
    script = generator.generate_script(post_data, format_type="short")

    try:
        subtitles = generator._generate_subtitles(script)
        print(f"✓ Generated {len(subtitles)} subtitle entries")

        if subtitles:
            # Test SRT time formatting
            srt_time = generator._format_srt_time(subtitles[0]["start"])
            print(f"✓ SRT time format: {srt_time}")

            # Test VTT time formatting
            vtt_time = generator._format_vtt_time(subtitles[0]["start"])
            print(f"✓ VTT time format: {vtt_time}")

        return True
    except Exception as e:
        print(f"✗ Subtitle generation failed: {e}")
        return False


def test_custom_options():
    """Test custom options"""
    print("\n" + "=" * 60)
    print("Test 6: Custom Options")
    print("=" * 60)

    custom_options = {
        "words_per_minute": 180,
        "show_usernames": False,
        "show_scores": False,
    }

    try:
        generator = ScriptGenerator(options=custom_options)
        post_data = create_mock_post()
        script = generator.generate_script(post_data, format_type="medium")

        print(f"✓ Custom options applied")
        print(f"  words_per_minute: {generator.words_per_minute}")
        print(f"  show_usernames: {generator.options['show_usernames']}")
        print(f"  show_scores: {generator.options['show_scores']}")
        return True
    except Exception as e:
        print(f"✗ Custom options failed: {e}")
        return False


def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("Test 7: Error Handling")
    print("=" * 60)

    generator = ScriptGenerator()

    # Test missing required fields
    invalid_post = {"id": "123"}  # Missing title, body, etc.

    try:
        script = generator.generate_script(invalid_post, format_type="medium")
        print("✗ Should have raised InvalidPostDataError")
        return False
    except ScriptGeneratorError as e:
        print(f"✓ Correctly raised error for invalid data: {type(e).__name__}")
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_templates():
    """Test template system"""
    print("\n" + "=" * 60)
    print("Test 8: Template System")
    print("=" * 60)

    try:
        templates = list_templates()
        print(f"✓ Available templates: {', '.join(templates)}")

        # Test each template
        generator = ScriptGenerator()
        post_data = create_mock_post()

        for template in templates:
            try:
                script = generator.generate_script(
                    post_data, template_name=template
                )
                print(f"✓ Template '{template}': {len(script['segments'])} segments")
            except Exception as e:
                print(f"✗ Template '{template}' failed: {e}")
                return False

        return True
    except Exception as e:
        print(f"✗ Template system failed: {e}")
        return False


def test_script_summary():
    """Test script summary generation"""
    print("\n" + "=" * 60)
    print("Test 9: Script Summary")
    print("=" * 60)

    try:
        generator = ScriptGenerator()
        post_data = create_mock_post()
        script = generator.generate_script(post_data, format_type="medium")

        summary = generator.get_script_summary(script)

        if "Video Script Summary" in summary and "Duration:" in summary:
            print("✓ Summary generated successfully")
            print("\nSummary preview:")
            print(summary[:300] + "...")
            return True
        else:
            print("✗ Summary missing expected content")
            return False
    except Exception as e:
        print(f"✗ Summary generation failed: {e}")
        return False


def test_convenience_function():
    """Test convenience function"""
    print("\n" + "=" * 60)
    print("Test 10: Convenience Function")
    print("=" * 60)

    try:
        post_data = create_mock_post()
        script = generate_script(post_data, format_type="short")

        if script and "segments" in script:
            print("✓ Convenience function works")
            print(f"  Generated {len(script['segments'])} segments")
            return True
        else:
            print("✗ Convenience function returned invalid data")
            return False
    except Exception as e:
        print(f"✗ Convenience function failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("SCRIPT GENERATOR MODULE TESTS")
    print("=" * 60)

    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("All Video Formats", test_all_formats),
        ("Narration Styles", test_narration_styles),
        ("Export Formats", test_export_formats),
        ("Subtitle Generation", test_subtitle_generation),
        ("Custom Options", test_custom_options),
        ("Error Handling", test_error_handling),
        ("Template System", test_templates),
        ("Script Summary", test_script_summary),
        ("Convenience Function", test_convenience_function),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ {name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({100 * passed / total:.0f}%)")

    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
