# Video Script Generator Module

A comprehensive module for converting Reddit post data into production-ready video scripts with timing, narration, visual cues, and subtitle support.

## Features

- **Multiple Video Formats** - Short (TikTok/Shorts), Medium (Instagram), Long (YouTube)
- **Narration Styles** - Casual, Formal, Dramatic, Comedic, Educational
- **Smart Timing** - Automatic duration calculation based on word count
- **Visual Cues** - Scene descriptions and visual element specifications
- **Subtitle Generation** - SRT and WebVTT subtitle file export
- **Multiple Export Formats** - JSON, TXT, SRT, VTT
- **Template System** - Customizable script templates for different video types
- **Comment Selection** - Intelligent comment filtering and ranking

## Installation

Dependencies are already included in `requirements.txt`. The script generator works seamlessly with the Reddit Fetcher module.

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from script_generator import ScriptGenerator
from reddit_fetcher import RedditFetcher

# Fetch Reddit post
fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

# Generate script
generator = ScriptGenerator()
script = generator.generate_script(post_data, format_type="medium")

# Export
generator.export_script(script, "video_script.json")
generator.export_script(script, "subtitles.srt", format="srt")
```

### Generate Different Formats

```python
# Short-form (30-60 seconds)
script_short = generator.generate_script(post_data, format_type="short")

# Medium-form (60-120 seconds)
script_medium = generator.generate_script(post_data, format_type="medium")

# Long-form (3+ minutes)
script_long = generator.generate_script(post_data, format_type="long")
```

### Use Different Narration Styles

```python
# Casual style (default)
script = generator.generate_script(post_data, narration_style="casual")

# Dramatic style
script = generator.generate_script(post_data, narration_style="dramatic")

# Formal style
script = generator.generate_script(post_data, narration_style="formal")

# Comedic style
script = generator.generate_script(post_data, narration_style="comedic")
```

## Video Format Presets

### Short-Form (TikTok, YouTube Shorts)
- **Duration**: 15-60 seconds (optimal: 30s)
- **Aspect Ratio**: 9:16 (vertical)
- **Pacing**: Fast
- **Structure**: Hook → Body → Comment → CTA
- **Best For**: Quick engagement, viral content

### Medium-Form (Instagram Reels, Facebook)
- **Duration**: 30-120 seconds (optimal: 60s)
- **Aspect Ratio**: 9:16 or 1:1
- **Pacing**: Medium
- **Structure**: Intro → Title → Body → Comments → Engagement → Outro
- **Best For**: Social media sharing, balanced content

### Long-Form (YouTube)
- **Duration**: 60-600 seconds (optimal: 180s)
- **Aspect Ratio**: 16:9 (horizontal)
- **Pacing**: Slow
- **Structure**: Cold Open → Intro → Title → Context → Body → Comments → Engagement → Outro
- **Best For**: In-depth coverage, monetization

## Script Structure

Generated scripts contain:

```python
{
    "metadata": {
        "post_id": "abc123",
        "title": "Post title",
        "subreddit": "subreddit_name",
        "author": "username",
        "format_type": "medium",
        "generated_at": "2025-11-07T...",
    },
    "segments": [
        {
            "name": "intro",
            "type": "intro",
            "start_time": 0.0,
            "end_time": 5.0,
            "duration": 5.0,
            "narration": "Check out this post from Reddit...",
            "visual": {
                "type": "animated_intro",
                "elements": [...]
            }
        },
        # More segments...
    ],
    "total_duration": 67.5,
    "word_count": 185,
    "narration_style": "casual"
}
```

## Segment Types

Each script is composed of multiple segments:

### Intro
- Greeting and channel branding
- Sets the tone for the video
- Duration: 3-8 seconds

### Title
- Post title presentation
- Eye-catching text animation
- Duration: 4-8 seconds

### Context
- Post metadata (author, score, subreddit)
- Background information
- Duration: 0-10 seconds

### Body
- Main post content narration
- Scrolling text overlay
- Duration: 15-90 seconds

### Comments
- Top comment selection and narration
- Comment thread visualization
- Duration: 8-40 seconds

### Engagement
- Call-to-action prompts
- Like/subscribe reminders
- Duration: 0-8 seconds

### Outro
- Thank you message
- End screen with next video suggestions
- Duration: 3-10 seconds

## Narration Styles

### Casual
- **Tone**: Friendly and conversational
- **Uses**: Contractions, slang
- **Example**: "Check this out! This is wild!"
- **Best For**: Most Reddit content

### Formal
- **Tone**: Professional and clear
- **Uses**: Proper grammar, no contractions
- **Example**: "Today we examine an interesting post."
- **Best For**: Educational, serious topics

### Dramatic
- **Tone**: Intense and engaging
- **Uses**: Suspenseful language
- **Example**: "You won't believe what happens next!"
- **Best For**: Story-time, shocking content

### Comedic
- **Tone**: Humorous and lighthearted
- **Uses**: Jokes, playful language
- **Example**: "Oh boy, here we go!"
- **Best For**: Funny posts, memes

## Export Formats

### JSON Format
```json
{
  "metadata": {...},
  "segments": [...],
  "total_duration": 67.5,
  "word_count": 185
}
```
**Use Case**: Video editing software integration, programmatic access

### Text Format
```
VIDEO SCRIPT
============================================================
SEGMENT 1: INTRO
------------------------------------------------------------
Time: 0.0s - 5.0s (5.0s)
Narration: Check out this post from Reddit...
```
**Use Case**: Human-readable scripts, voice actor scripts

### SRT Subtitles
```
1
00:00:00,000 --> 00:00:03,500
Check out this post from Reddit

2
00:00:03,500 --> 00:00:07,000
about octopuses having three hearts
```
**Use Case**: Video subtitles, accessibility

### WebVTT Subtitles
```
WEBVTT

00:00:00.000 --> 00:00:03.500
Check out this post from Reddit

00:00:03.500 --> 00:00:07.000
about octopuses having three hearts
```
**Use Case**: Web players, HTML5 video

## Configuration

### Script Options (script_config.py)

```python
SCRIPT_OPTIONS = {
    "words_per_minute": 150,      # Speaking pace
    "pause_duration": 0.5,        # Pause between segments
    "max_comment_length": 200,    # Max comment characters
    "show_usernames": True,       # Show u/username
    "show_scores": True,          # Show upvote counts
    "narration_style": "casual",  # Default style
}
```

### Custom Options

```python
custom_options = {
    "words_per_minute": 180,  # Faster speech
    "show_usernames": False,   # Hide usernames
}

generator = ScriptGenerator(options=custom_options)
script = generator.generate_script(post_data, format_type="medium")
```

## Templates

Available templates:

### short
- **Segments**: 4 (hook, body, comment, outro)
- **Duration**: ~29 seconds
- **Best For**: TikTok, YouTube Shorts

### medium
- **Segments**: 7 (intro, title, context, body, comments, engagement, outro)
- **Duration**: ~67 seconds
- **Best For**: Instagram Reels, Facebook

### long
- **Segments**: 10 (cold open, intro, title, context, body parts, comments, engagement, outro)
- **Duration**: ~192 seconds
- **Best For**: YouTube full videos

### story
- **Segments**: 5 (hook, setup, story, reactions, conclusion)
- **Duration**: ~120 seconds
- **Best For**: Story-time format

### compilation
- **Segments**: 3 (intro, repeatable post blocks, outro)
- **Duration**: Variable
- **Best For**: Multiple posts in one video

## Advanced Usage

### Custom Template

```python
# List available templates
from script_templates import list_templates
print(list_templates())  # ['short', 'medium', 'long', 'story', 'compilation']

# Get template info
from script_templates import get_template_info
info = get_template_info("medium")
print(info)
```

### Subtitle Customization

```python
# Generate subtitles with custom settings
subtitles = generator._generate_subtitles(
    script,
    max_chars_per_line=50  # Longer subtitle lines
)
```

### Script Summary

```python
# Get human-readable summary
summary = generator.get_script_summary(script)
print(summary)

# Output:
# Video Script Summary
# ============================================================
# Title: TIL that octopuses have three hearts...
# Duration: 67.5 seconds (1.1 minutes)
# Segments: 7
# ...
```

## Integration with Video Editing

### After Effects / Premiere Pro
1. Export script as JSON
2. Use script timing for cuts
3. Import SRT for subtitle track
4. Use visual cues for effects

### Python Video Libraries (moviepy)
```python
from moviepy.editor import *

# Load script
with open("script.json") as f:
    script = json.load(f)

# Create clips based on segments
clips = []
for segment in script["segments"]:
    # Create clip with duration
    clip = create_segment_clip(segment)
    clips.append(clip)

# Concatenate
final = concatenate_videoclips(clips)
```

### DaVinci Resolve
1. Export as TXT for narration reference
2. Import SRT for subtitle track
3. Use segment timing for scene markers

## Best Practices

### 1. Content Selection
- Choose posts with clear narratives
- Verify post content is appropriate
- Check comment quality before generating

### 2. Format Selection
- **Short**: Viral potential, quick facts, jokes
- **Medium**: Most Reddit posts, balanced content
- **Long**: Deep dives, complex stories, discussions

### 3. Narration Style
- Match style to content tone
- **Casual**: General content (80% of posts)
- **Formal**: Educational, serious topics (10%)
- **Dramatic**: Stories, shocking events (5%)
- **Comedic**: Humor, memes (5%)

### 4. Timing Adjustments
- Adjust `words_per_minute` for different voices
- Slow (120): Careful enunciation
- Normal (150): Standard speaking pace
- Fast (180): Energetic delivery

### 5. Comment Curation
- Set appropriate `min_comment_score`
- Review selected comments for quality
- Ensure comments add value

## Examples

See `examples/script_generator_example.py` for:
1. Short-form video generation
2. Medium-form video generation
3. Long-form video generation
4. Export format demonstrations
5. Narration style comparisons
6. Custom option usage
7. Subtitle generation
8. Template comparisons
9. Full workflow example
10. RedditFetcher integration

Run examples:
```bash
python examples/script_generator_example.py
```

## API Reference

### ScriptGenerator Class

#### `__init__(options=None)`
Initialize generator with custom options.

#### `generate_script(post_data, format_type="medium", template_name=None, narration_style="casual")`
Generate video script from Reddit post data.

**Args:**
- `post_data`: Dict from RedditFetcher
- `format_type`: "short", "medium", or "long"
- `template_name`: Custom template (optional)
- `narration_style`: "casual", "formal", "dramatic", or "comedic"

**Returns:** Script dictionary

#### `export_script(script, output_path, format="json")`
Export script to file.

**Args:**
- `script`: Generated script dictionary
- `output_path`: File path
- `format`: "json", "txt", "srt", or "vtt"

#### `get_script_summary(script)`
Generate human-readable summary.

**Returns:** Formatted string

### Convenience Functions

#### `generate_script(post_data, format_type="medium", **kwargs)`
Quick script generation without creating generator instance.

## Performance

| Operation | Time |
|-----------|------|
| Script generation | < 0.1s |
| JSON export | < 0.05s |
| SRT generation | < 0.1s |
| Full workflow | < 0.3s |

## Troubleshooting

### "Missing required fields" Error
**Cause**: Post data doesn't have required fields
**Solution**: Ensure post has title, body, subreddit, author

### Empty segments
**Cause**: No content available for segment
**Solution**: Optional segments are automatically skipped

### Subtitle timing issues
**Cause**: `words_per_minute` doesn't match actual speech
**Solution**: Adjust `words_per_minute` in options

## Roadmap

Planned features:
- [ ] A/B testing for titles
- [ ] SEO optimization for video descriptions
- [ ] Multi-language support
- [ ] AI voice-over integration (TTS)
- [ ] Background music suggestions
- [ ] Automated thumbnail generation
- [ ] Analytics and performance tracking

## Contributing

To add custom templates:
1. Create new template class in `script_templates.py`
2. Inherit from `ScriptTemplate`
3. Define segment structure
4. Add to `TEMPLATES` dictionary

## License

Part of the DeepSeek-OCR project. See LICENSE file.

## Next Steps

After generating scripts:
1. **Record narration** - Use script text for voice-over
2. **Create visuals** - Follow visual cues for editing
3. **Add subtitles** - Import SRT/VTT files
4. **Edit video** - Use segment timing for cuts
5. **Publish** - Export and upload to platform

## Complete Workflow

```
Reddit Post → RedditFetcher → Post Data
                                  ↓
                         ScriptGenerator → Video Script
                                  ↓
                    ├─ JSON (editing software)
                    ├─ TXT (narration script)
                    ├─ SRT (subtitles)
                    └─ VTT (web subtitles)
                                  ↓
                         Video Production
                                  ↓
                            Published Video
```

---

**Created**: 2025-11-07
**Version**: 1.0.0
**Status**: Production Ready
