"""
Text-to-Speech Configuration

Configure TTS providers, voices, and audio settings.
"""

import os

# TTS Provider Configuration
TTS_PROVIDERS = {
    "gtts": {
        "name": "Google Text-to-Speech (Free)",
        "requires_api_key": False,
        "languages": ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"],
        "voices": ["default"],
        "max_characters": 5000,
        "rate_limit": None,
        "quality": "good",
        "cost": "free",
    },
    "pyttsx3": {
        "name": "pyttsx3 (Offline)",
        "requires_api_key": False,
        "languages": ["en", "es", "fr"],
        "voices": ["male", "female"],
        "max_characters": None,
        "rate_limit": None,
        "quality": "basic",
        "cost": "free",
        "offline": True,
    },
    "google_cloud": {
        "name": "Google Cloud Text-to-Speech",
        "requires_api_key": True,
        "languages": ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT", "ja-JP", "ko-KR"],
        "voices": ["Neural2", "Wavenet", "Standard"],
        "max_characters": 5000,
        "rate_limit": "1M chars/month free",
        "quality": "excellent",
        "cost": "$4-16 per 1M chars",
    },
    "amazon_polly": {
        "name": "Amazon Polly",
        "requires_api_key": True,
        "languages": ["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT", "ja-JP", "pt-BR"],
        "voices": ["Neural", "Standard"],
        "max_characters": 3000,
        "rate_limit": "5M chars/month free",
        "quality": "excellent",
        "cost": "$4-16 per 1M chars",
    },
    "elevenlabs": {
        "name": "ElevenLabs (Premium)",
        "requires_api_key": True,
        "languages": ["en", "multilingual"],
        "voices": ["custom", "premade"],
        "max_characters": 10000,
        "rate_limit": "10K chars/month free",
        "quality": "exceptional",
        "cost": "$5-99/month",
        "realistic": True,
    },
}

# Default TTS Provider
DEFAULT_PROVIDER = "gtts"  # Free and works out of the box

# Voice Settings
VOICE_SETTINGS = {
    "gtts": {
        "default": {
            "language": "en",
            "tld": "com",  # com = US, co.uk = UK, com.au = AU, etc.
            "slow": False,
        }
    },
    "pyttsx3": {
        "male": {
            "rate": 150,  # Words per minute
            "volume": 1.0,  # 0.0 to 1.0
            "voice_id": 0,  # System-dependent
        },
        "female": {
            "rate": 150,
            "volume": 1.0,
            "voice_id": 1,
        }
    },
    "google_cloud": {
        "en-US-Neural2-A": {
            "language_code": "en-US",
            "name": "en-US-Neural2-A",
            "ssml_gender": "MALE",
            "speaking_rate": 1.0,
            "pitch": 0.0,
        },
        "en-US-Neural2-C": {
            "language_code": "en-US",
            "name": "en-US-Neural2-C",
            "ssml_gender": "FEMALE",
            "speaking_rate": 1.0,
            "pitch": 0.0,
        }
    },
    "amazon_polly": {
        "Matthew": {
            "voice_id": "Matthew",
            "engine": "neural",
            "language_code": "en-US",
        },
        "Joanna": {
            "voice_id": "Joanna",
            "engine": "neural",
            "language_code": "en-US",
        }
    },
    "elevenlabs": {
        "default": {
            "voice_id": None,  # Set your voice ID
            "model_id": "eleven_monolingual_v1",
            "stability": 0.5,
            "similarity_boost": 0.75,
        }
    }
}

# Audio Export Settings
AUDIO_SETTINGS = {
    "format": "mp3",  # mp3, wav, ogg, flac
    "sample_rate": 24000,  # Hz (24000 is good for speech)
    "bitrate": "128k",  # For MP3
    "channels": 1,  # Mono for voice-over
    "normalize": True,  # Normalize audio levels
    "remove_silence": True,  # Remove long silences
}

# Audio Processing
AUDIO_PROCESSING = {
    "silence_threshold": -40,  # dB
    "min_silence_duration": 0.5,  # seconds
    "fade_in": 0.1,  # seconds
    "fade_out": 0.2,  # seconds
    "padding": {
        "start": 0.5,  # seconds before first word
        "end": 0.5,  # seconds after last word
        "between_segments": 0.3,  # seconds between segments
    }
}

# Background Music Settings
BACKGROUND_MUSIC = {
    "enabled": False,
    "volume": 0.15,  # 15% of narration volume
    "fade_in": 2.0,  # seconds
    "fade_out": 3.0,  # seconds
    "loop": True,
}

# TTS Generation Options
TTS_OPTIONS = {
    "cache_audio": True,  # Cache generated audio files
    "cache_dir": "./tts_cache",
    "split_long_text": True,  # Split text longer than max_characters
    "retry_on_error": 3,  # Number of retries
    "timeout": 30,  # seconds
}

# API Keys (use environment variables)
API_KEYS = {
    "google_cloud": os.getenv("GOOGLE_CLOUD_TTS_API_KEY"),
    "amazon_polly": {
        "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region": os.getenv("AWS_REGION", "us-east-1"),
    },
    "elevenlabs": os.getenv("ELEVENLABS_API_KEY"),
}

# Voice Presets for Different Video Styles
VOICE_PRESETS = {
    "casual": {
        "provider": "gtts",
        "voice": "default",
        "speed": 1.0,
        "pitch": 0.0,
        "description": "Friendly, conversational voice",
    },
    "professional": {
        "provider": "google_cloud",
        "voice": "en-US-Neural2-A",
        "speed": 0.95,
        "pitch": -1.0,
        "description": "Clear, professional male voice",
    },
    "energetic": {
        "provider": "gtts",
        "voice": "default",
        "speed": 1.15,
        "pitch": 2.0,
        "description": "Fast-paced, exciting voice",
    },
    "calm": {
        "provider": "pyttsx3",
        "voice": "female",
        "speed": 0.85,
        "pitch": 0.0,
        "description": "Slow, calming voice",
    },
}

# File Naming
FILE_NAMING = {
    "pattern": "{script_id}_{segment_name}_{timestamp}",
    "use_timestamp": False,
    "include_provider": False,
}

# Supported Audio Formats
SUPPORTED_FORMATS = {
    "mp3": {
        "extension": ".mp3",
        "mime_type": "audio/mpeg",
        "compression": "lossy",
        "quality": "good",
        "file_size": "small",
    },
    "wav": {
        "extension": ".wav",
        "mime_type": "audio/wav",
        "compression": "none",
        "quality": "excellent",
        "file_size": "large",
    },
    "ogg": {
        "extension": ".ogg",
        "mime_type": "audio/ogg",
        "compression": "lossy",
        "quality": "good",
        "file_size": "small",
    },
    "flac": {
        "extension": ".flac",
        "mime_type": "audio/flac",
        "compression": "lossless",
        "quality": "excellent",
        "file_size": "medium",
    },
}

# Language Codes
LANGUAGE_CODES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
}

# Error Messages
ERROR_MESSAGES = {
    "api_key_missing": "API key not found for provider '{provider}'. Set environment variable.",
    "provider_not_found": "TTS provider '{provider}' not found. Available: {available}",
    "text_too_long": "Text exceeds maximum length of {max_chars} characters for provider '{provider}'",
    "generation_failed": "Failed to generate audio after {retries} attempts",
    "invalid_format": "Audio format '{format}' not supported. Use: {supported}",
}
