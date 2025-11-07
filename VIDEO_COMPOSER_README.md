# Video Composer Module

A comprehensive video composition module that combines scripts and audio files into final videos with visuals, text overlays, transitions, and effects.

## Features

- **Multiple Video Formats** - TikTok, Instagram, YouTube, Facebook
- **Automatic Visual Generation** - Text overlays, backgrounds, gradients
- **Audio Integration** - Sync audio with visuals
- **Background Music** - Add and mix background music
- **Thumbnail Generation** - Create video thumbnails
- **Multiple Resolutions** - From 1080p to 4K
- **Customizable Styles** - Minimal, modern, vibrant, professional
- **Rendering Optimization** - Multi-threaded rendering

## Installation

```bash
pip install moviepy imageio imageio-ffmpeg Pillow
```

**Note**: Requires FFmpeg installed on your system.

## Quick Start

### Basic Usage

```python
from video_composer import VideoComposer

# Initialize composer
composer = VideoComposer(format_type="youtube")

# Compose video
video_path = composer.compose_video(
    script=script,              # From ScriptGenerator
    audio_files=audio_files,    # From TTSGenerator
    output_path="final_video.mp4"
)
```

### Complete Pipeline

```python
from reddit_fetcher import RedditFetcher
from script_generator import ScriptGenerator
from tts_generator import TTSGenerator
from video_composer import VideoComposer

# 1. Fetch Reddit post
fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

# 2. Generate script
script_gen = ScriptGenerator()
script = script_gen.generate_script(post_data, format_type="medium")

# 3. Generate audio
tts_gen = TTSGenerator(provider="gtts")
audio_files = tts_gen.generate_from_script(script, "./audio")

# 4. Compose video
composer = VideoComposer(format_type="youtube")
video = composer.compose_video(script, audio_files, "final.mp4")

print(f"✓ Video ready: {video}")
```

## Video Formats

| Format | Resolution | Aspect | Duration | Platform |
|--------|-----------|---------|----------|----------|
| **tiktok** | 1080x1920 | 9:16 | 60s | TikTok/Shorts |
| **instagram** | 1080x1920 | 9:16 | 90s | Instagram Reels |
| **youtube** | 1920x1080 | 16:9 | 10min | YouTube |
| **youtube_4k** | 3840x2160 | 16:9 | 10min | YouTube 4K |
| **facebook** | 1080x1080 | 1:1 | 4min | Facebook |

## Configuration

### Video Settings (video_config.py)

```python
VIDEO_FORMATS = {
    "youtube": {
        "resolution": (1920, 1080),
        "fps": 30,
        "bitrate": "10000k",
        "codec": "libx264",
    }
}
```

### Background Settings

```python
BACKGROUND_SETTINGS = {
    "type": "gradient",  # solid, gradient, image
    "color": "#1a1a2e",
    "color_end": "#16213e",
}
```

### Text Settings

```python
TEXT_SETTINGS = {
    "font": "Arial-Bold",
    "title_size": 80,
    "body_size": 60,
    "color": "white",
    "stroke_width": 2,
}
```

## Features

### 1. Background Types

```python
# Solid color
BACKGROUND_SETTINGS = {"type": "solid", "color": "#1a1a2e"}

# Gradient
BACKGROUND_SETTINGS = {
    "type": "gradient",
    "color": "#1a1a2e",
    "color_end": "#16213e"
}

# Image
BACKGROUND_SETTINGS = {
    "type": "image",
    "image_path": "./background.jpg"
}
```

### 2. Text Overlays

Automatic text positioning and sizing based on segment type:
- **Intro/Title**: Large centered text (80px)
- **Body**: Medium scrolling text (60px)
- **Comments**: Smaller text with avatars (50px)
- **Outro**: Large call-to-action (70px)

### 3. Animations

```python
ANIMATION_SETTINGS = {
    "text_fade_in": 0.3,  # Fade in duration
    "text_fade_out": 0.3,  # Fade out duration
    "enable_animations": True,
}
```

### 4. Background Music

```python
composer.compose_video(
    script=script,
    audio_files=audio_files,
    output_path="video.mp4",
    background_music="./music.mp3"  # Optional
)
```

### 5. Thumbnail Generation

```python
# Generate thumbnail
thumbnail_path = composer.generate_thumbnail(
    script=script,
    output_path="thumbnail.jpg"
)
```

## API Reference

### VideoComposer Class

#### `__init__(format_type, resolution, fps, options)`
Initialize video composer.

**Args:**
- `format_type`: Video format preset
- `resolution`: Custom resolution tuple
- `fps`: Frames per second
- `options`: Custom rendering options

#### `compose_video(script, audio_files, output_path, background_music)`
Compose complete video.

**Args:**
- `script`: Video script dictionary
- `audio_files`: List of audio file info
- `output_path`: Output video path
- `background_music`: Optional music path

**Returns:** Path to rendered video

#### `generate_thumbnail(script, output_path)`
Generate thumbnail image.

**Returns:** Path to thumbnail image

### Convenience Function

#### `compose_video_from_script(script, audio_files, output_path, format_type, background_music)`
Quick video composition without creating composer instance.

## Rendering Options

```python
RENDERING_SETTINGS = {
    "threads": 4,  # Number of rendering threads
    "preset": "medium",  # Speed/quality tradeoff
    "verbose": False,  # Show detailed output
}
```

### Preset Options

- **ultrafast**: Fastest, lowest quality
- **fast**: Fast, good quality
- **medium**: Balanced (default)
- **slow**: Slow, high quality
- **veryslow**: Slowest, highest quality

## Performance

| Resolution | Preset | Duration | Render Time (approx) |
|-----------|---------|----------|---------------------|
| 1080p | fast | 60s | 1-2 min |
| 1080p | medium | 60s | 2-4 min |
| 1080p | slow | 60s | 5-10 min |
| 4K | medium | 60s | 10-20 min |

## Complete Workflow

```
1. Reddit Post (RedditFetcher)
          ↓
2. Video Script (ScriptGenerator)
          ↓
3. Audio Narration (TTSGenerator)
          ↓
4. Final Video (VideoComposer) ← YOU ARE HERE
          ↓
5. Published Video!
```

## Best Practices

### 1. Format Selection
- **TikTok/Shorts**: Use "tiktok" format (9:16, 60s max)
- **Instagram**: Use "instagram" format (9:16, 90s max)
- **YouTube**: Use "youtube" format (16:9, HD)

### 2. Resolution
- **Mobile-first**: 1080x1920 (vertical)
- **Desktop**: 1920x1080 (horizontal)
- **Professional**: 3840x2160 (4K)

### 3. Rendering
- Use "fast" preset for testing
- Use "medium" for production
- Use "slow" only for final uploads

### 4. File Sizes
- 1080p, 60s, medium: ~50-100 MB
- 4K, 60s, medium: ~200-400 MB

## Troubleshooting

### "FFmpeg not found"
**Solution**: Install FFmpeg
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from ffmpeg.org
```

### "MoviePy import error"
**Solution**: Install moviepy
```bash
pip install moviepy imageio-ffmpeg
```

### "Rendering is slow"
**Solutions**:
- Use faster preset ("fast" or "ultrafast")
- Reduce resolution
- Increase threads in RENDERING_SETTINGS
- Use SSD for temp files

### "Out of memory"
**Solutions**:
- Reduce resolution
- Process shorter segments
- Close other applications

## Examples

See `examples/video_composer_example.py` for detailed examples.

## Status

**Module Status: ✅ PRODUCTION READY**

- Video composition working
- Multiple format support
- Background and text rendering
- Audio integration
- Thumbnail generation

---

**Created**: 2025-11-07
**Version**: 1.0.0
**Status**: Production Ready
