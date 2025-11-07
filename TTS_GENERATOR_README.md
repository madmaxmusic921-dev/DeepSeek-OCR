# Text-to-Speech Generator Module

A comprehensive TTS module that converts video scripts into audio narration files using multiple TTS providers.

## Features

- **Multiple TTS Providers** - gTTS (free), pyttsx3 (offline), Google Cloud, Amazon Polly, ElevenLabs
- **Audio Caching** - Cache generated audio to speed up regeneration
- **Script Integration** - Seamlessly process ScriptGenerator output
- **Voice Customization** - Multiple voices and accents
- **Audio Manifest** - JSON export of all generated audio files
- **Error Handling** - Robust error handling with retry logic
- **Batch Generation** - Process entire scripts at once

## Installation

### Basic (Free Providers)

```bash
pip install gtts pyttsx3 pydub
```

### Premium Providers (Optional)

```bash
# Google Cloud TTS
pip install google-cloud-texttospeech

# Amazon Polly
pip install boto3

# ElevenLabs
pip install elevenlabs
```

## Quick Start

### Basic Usage

```python
from tts_generator import TTSGenerator

# Initialize generator
generator = TTSGenerator(provider="gtts")

# Generate audio from text
audio_path = generator.generate_audio(
    "Hello from Reddit!",
    "output.mp3"
)
```

### Generate from Script

```python
from script_generator import ScriptGenerator
from tts_generator import TTSGenerator

# Generate script
script_gen = ScriptGenerator()
script = script_gen.generate_script(post_data)

# Generate audio
tts_gen = TTSGenerator(provider="gtts")
audio_files = tts_gen.generate_from_script(script, "./audio_output")

# Export manifest
tts_gen.export_audio_manifest(audio_files, "audio_manifest.json")
```

## TTS Providers

### gTTS (Free)
- **Cost**: Free
- **Quality**: Good
- **Setup**: No API key required
- **Languages**: 40+ languages
- **Best For**: Most use cases

```python
generator = TTSGenerator(provider="gtts", voice="default")
```

### pyttsx3 (Offline)
- **Cost**: Free
- **Quality**: Basic
- **Setup**: No internet required
- **Languages**: Limited
- **Best For**: Offline use, testing

```python
generator = TTSGenerator(provider="pyttsx3", voice="male")
```

### Google Cloud TTS (Premium)
- **Cost**: $4-16 per 1M characters
- **Quality**: Excellent
- **Setup**: Requires API key
- **Languages**: 40+ with neural voices
- **Best For**: Professional quality

```python
# Set environment variable: GOOGLE_CLOUD_TTS_API_KEY
generator = TTSGenerator(provider="google_cloud", voice="en-US-Neural2-A")
```

### Amazon Polly (Premium)
- **Cost**: $4-16 per 1M characters
- **Quality**: Excellent
- **Setup**: Requires AWS credentials
- **Languages**: 30+ languages
- **Best For**: AWS integration

```python
# Set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
generator = TTSGenerator(provider="amazon_polly", voice="Joanna")
```

### ElevenLabs (Premium)
- **Cost**: $5-99/month
- **Quality**: Exceptional (most realistic)
- **Setup**: Requires API key
- **Languages**: English + multilingual
- **Best For**: Maximum realism

```python
# Set environment variable: ELEVENLABS_API_KEY
generator = TTSGenerator(provider="elevenlabs", voice="default")
```

## Provider Comparison

| Provider | Cost | Quality | API Key | Offline | Best For |
|----------|------|---------|---------|---------|----------|
| **gTTS** | Free | Good | No | No | General use |
| **pyttsx3** | Free | Basic | No | Yes | Testing |
| **Google Cloud** | Paid | Excellent | Yes | No | Professional |
| **Amazon Polly** | Paid | Excellent | Yes | No | AWS users |
| **ElevenLabs** | Paid | Exceptional | Yes | No | Maximum quality |

## Configuration

### Voice Settings (tts_config.py)

```python
VOICE_SETTINGS = {
    "gtts": {
        "default": {
            "language": "en",
            "tld": "com",  # US accent
            "slow": False,
        }
    },
    "pyttsx3": {
        "male": {
            "rate": 150,  # Words per minute
            "volume": 1.0,
        }
    }
}
```

### Audio Settings

```python
AUDIO_SETTINGS = {
    "format": "mp3",
    "sample_rate": 24000,  # Hz
    "bitrate": "128k",
    "channels": 1,  # Mono
}
```

## Features

### 1. Audio Caching

Cache generated audio for faster regeneration:

```python
generator = TTSGenerator(
    provider="gtts",
    options={
        "cache_audio": True,
        "cache_dir": "./tts_cache"
    }
)
```

### 2. Batch Generation

Process entire scripts at once:

```python
audio_files = generator.generate_from_script(script, "./audio")

# Returns list of audio file info:
# [
#   {
#     "segment_name": "intro",
#     "audio_path": "./audio/01_intro.mp3",
#     "duration": 3.0,
#     "text": "Check out this post..."
#   },
#   ...
# ]
```

### 3. Audio Manifest

Export JSON manifest of all audio files:

```python
generator.export_audio_manifest(audio_files, "manifest.json")

# Creates:
# {
#   "generated_at": "2025-11-07T...",
#   "provider": "gtts",
#   "total_files": 4,
#   "audio_files": [...]
# }
```

### 4. Generation Summary

Get human-readable summary:

```python
summary = generator.get_generation_summary(audio_files)
print(summary)

# Output:
# Audio Generation Summary
# ============================================================
# Provider: gtts
# Files Generated: 4
# Total Duration: 26.0 seconds
# ...
```

## API Reference

### TTSGenerator Class

#### `__init__(provider, voice, options)`
Initialize TTS generator.

**Args:**
- `provider`: "gtts", "pyttsx3", "google_cloud", "amazon_polly", "elevenlabs"
- `voice`: Voice name or configuration
- `options`: Custom options dict

#### `generate_audio(text, output_path, segment_name)`
Generate audio from text.

**Args:**
- `text`: Text to convert
- `output_path`: Output file path
- `segment_name`: Segment identifier (for caching)

**Returns:** Path to generated audio file

#### `generate_from_script(script, output_dir)`
Generate audio for all script segments.

**Args:**
- `script`: Script dictionary from ScriptGenerator
- `output_dir`: Directory for output files

**Returns:** List of audio file information dicts

#### `export_audio_manifest(audio_files, output_path)`
Export audio manifest as JSON.

### Convenience Functions

#### `generate_audio_from_script(script, provider, voice, output_dir)`
Quick function to generate audio without creating generator instance.

## Complete Workflow

```python
# 1. Fetch Reddit post
from reddit_fetcher import RedditFetcher
fetcher = RedditFetcher()
post_data = fetcher.fetch_post_by_id("abc123")

# 2. Generate script
from script_generator import ScriptGenerator
script_gen = ScriptGenerator()
script = script_gen.generate_script(post_data, format_type="medium")

# 3. Generate audio
from tts_generator import TTSGenerator
tts_gen = TTSGenerator(provider="gtts")
audio_files = tts_gen.generate_from_script(script, "./audio")

# 4. Export manifest
tts_gen.export_audio_manifest(audio_files, "audio_manifest.json")

print("✓ Complete! Audio files ready for video production")
```

## Voice Options

### gTTS Accents

```python
# US English
generator = TTSGenerator(provider="gtts", voice="default")

# British English
VOICE_SETTINGS["gtts"]["default"]["tld"] = "co.uk"

# Australian English
VOICE_SETTINGS["gtts"]["default"]["tld"] = "com.au"
```

### Multiple Languages

```python
# Spanish
VOICE_SETTINGS["gtts"]["default"]["language"] = "es"

# French
VOICE_SETTINGS["gtts"]["default"]["language"] = "fr"

# Japanese
VOICE_SETTINGS["gtts"]["default"]["language"] = "ja"
```

## Audio Formats

Supported formats:
- **MP3**: Good quality, small size (default)
- **WAV**: Excellent quality, large size
- **OGG**: Good quality, small size
- **FLAC**: Lossless, medium size

## Error Handling

```python
from tts_generator import TTSError, ProviderNotFoundError, APIKeyMissingError

try:
    generator = TTSGenerator(provider="gtts")
    audio = generator.generate_audio("Hello!", "output.mp3")
except ProviderNotFoundError as e:
    print(f"Provider not found: {e}")
except APIKeyMissingError as e:
    print(f"API key missing: {e}")
except TTSError as e:
    print(f"TTS error: {e}")
```

## Best Practices

### 1. Provider Selection
- **Development/Testing**: Use `pyttsx3` (offline, free)
- **Production (Free)**: Use `gtts` (good quality, free)
- **Production (Paid)**: Use `google_cloud` or `elevenlabs` (best quality)

### 2. Caching
Always enable caching for repeated script generation:
```python
options = {"cache_audio": True, "cache_dir": "./tts_cache"}
```

### 3. Batch Processing
Generate all segments at once rather than one by one:
```python
# Good
audio_files = generator.generate_from_script(script)

# Less efficient
for segment in script["segments"]:
    generator.generate_audio(segment["narration"], ...)
```

### 4. Error Handling
Always wrap TTS calls in try-except blocks

### 5. API Keys
Use environment variables for API keys:
```bash
export GOOGLE_CLOUD_TTS_API_KEY="your-key"
export AWS_ACCESS_KEY_ID="your-key"
export ELEVENLABS_API_KEY="your-key"
```

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Single audio (gTTS) | 0.5-2s | Depends on text length |
| Full script (4 segments) | 2-5s | With caching |
| Cached audio retrieval | <0.1s | Instant |

## Troubleshooting

### "Provider not available"
**Solution**: Install required library
```bash
pip install gtts  # For gTTS
pip install pyttsx3  # For pyttsx3
```

### "API key missing"
**Solution**: Set environment variable
```bash
export GOOGLE_CLOUD_TTS_API_KEY="your-key"
```

### "Audio generation failed"
**Solution**: Check internet connection (for online providers)

### "No audio output"
**Solution**: Check if pyttsx3 voices are installed on system

## Examples

See `examples/tts_generator_example.py` for:
1. Basic TTS generation
2. Generate from script
3. Different providers
4. Voice variations
5. Audio caching
6. Full workflow
7. Script Generator integration
8. Provider comparison
9. Error handling
10. Convenience functions

Run examples:
```bash
python examples/tts_generator_example.py
```

## Integration with Video Editing

### After Effects / Premiere Pro
1. Generate audio files from script
2. Import audio files matching script timing
3. Sync with visual elements
4. Export final video

### Python (moviepy)
```python
from moviepy.editor import *

# Load audio files
clips = []
for audio_info in audio_files:
    audio = AudioFileClip(audio_info["audio_path"])
    clips.append(audio)

# Concatenate
final_audio = concatenate_audioclips(clips)
final_audio.write_audiofile("narration.mp3")
```

## Roadmap

Planned features:
- [ ] SSML support for advanced control
- [ ] Real-time streaming TTS
- [ ] Voice cloning integration
- [ ] Background music mixing
- [ ] Audio effects (reverb, EQ)
- [ ] Multi-language script support
- [ ] Pronunciation dictionary
- [ ] Emotion/tone control

## License

Part of the DeepSeek-OCR project. See LICENSE file.

## Next Steps

After generating audio:
1. **Combine with video** - Use audio files in video editor
2. **Add background music** - Mix narration with music
3. **Add sound effects** - Enhance engagement
4. **Sync subtitles** - Use script timing for perfect sync
5. **Export final video** - Render and publish

---

**Created**: 2025-11-07
**Version**: 1.0.0
**Status**: Production Ready
