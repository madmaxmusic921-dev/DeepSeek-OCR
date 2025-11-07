"""
Text-to-Speech Generator Module

Converts video scripts into audio files using various TTS providers.
Supports multiple providers (gTTS, pyttsx3, Google Cloud, Amazon Polly, ElevenLabs).

Example:
    generator = TTSGenerator(provider="gtts")
    audio_files = generator.generate_from_script(script)
    generator.export_combined_audio(audio_files, "final_narration.mp3")
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib

try:
    from tts_config import (
        TTS_PROVIDERS,
        DEFAULT_PROVIDER,
        VOICE_SETTINGS,
        AUDIO_SETTINGS,
        AUDIO_PROCESSING,
        TTS_OPTIONS,
        API_KEYS,
        VOICE_PRESETS,
    )
except ImportError:
    print("Warning: tts_config.py not found. Using defaults.")
    TTS_PROVIDERS = {}
    DEFAULT_PROVIDER = "gtts"
    VOICE_SETTINGS = {}
    AUDIO_SETTINGS = {}
    AUDIO_PROCESSING = {}
    TTS_OPTIONS = {}
    API_KEYS = {}
    VOICE_PRESETS = {}


class TTSError(Exception):
    """Base exception for TTS errors"""
    pass


class ProviderNotFoundError(TTSError):
    """Raised when TTS provider is not available"""
    pass


class APIKeyMissingError(TTSError):
    """Raised when API key is required but not provided"""
    pass


class AudioGenerationError(TTSError):
    """Raised when audio generation fails"""
    pass


class TTSGenerator:
    """
    Generate audio from text using various TTS providers.

    Attributes:
        provider: TTS provider name
        voice: Voice configuration
        options: Generation options
    """

    def __init__(
        self,
        provider: str = None,
        voice: str = "default",
        options: Optional[Dict] = None
    ):
        """
        Initialize TTS Generator.

        Args:
            provider: TTS provider ("gtts", "pyttsx3", "google_cloud", etc.)
            voice: Voice name or preset
            options: Custom generation options

        Raises:
            ProviderNotFoundError: If provider is not supported
            APIKeyMissingError: If provider requires API key
        """
        self.provider = provider or DEFAULT_PROVIDER
        self.voice = voice
        self.options = {**TTS_OPTIONS, **(options or {})}

        # Validate provider
        if self.provider not in TTS_PROVIDERS:
            available = ", ".join(TTS_PROVIDERS.keys())
            raise ProviderNotFoundError(
                f"Provider '{self.provider}' not found. Available: {available}"
            )

        # Check API key if required
        provider_config = TTS_PROVIDERS[self.provider]
        if provider_config.get("requires_api_key"):
            if not self._has_api_key():
                raise APIKeyMissingError(
                    f"Provider '{self.provider}' requires an API key. "
                    f"Set the appropriate environment variable."
                )

        # Initialize provider
        self._init_provider()

        # Create cache directory
        if self.options.get("cache_audio"):
            os.makedirs(self.options.get("cache_dir", "./tts_cache"), exist_ok=True)

    def _has_api_key(self) -> bool:
        """Check if API key is available for provider"""
        if self.provider == "google_cloud":
            return API_KEYS.get("google_cloud") is not None
        elif self.provider == "amazon_polly":
            keys = API_KEYS.get("amazon_polly", {})
            return keys.get("access_key") and keys.get("secret_key")
        elif self.provider == "elevenlabs":
            return API_KEYS.get("elevenlabs") is not None
        return True

    def _init_provider(self):
        """Initialize the TTS provider"""
        if self.provider == "gtts":
            try:
                from gtts import gTTS
                self.engine = gTTS
                self.provider_available = True
            except ImportError:
                self.provider_available = False
                print("⚠ gTTS not installed. Run: pip install gtts")

        elif self.provider == "pyttsx3":
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.provider_available = True
                self._configure_pyttsx3()
            except ImportError:
                self.provider_available = False
                print("⚠ pyttsx3 not installed. Run: pip install pyttsx3")

        elif self.provider == "google_cloud":
            try:
                from google.cloud import texttospeech
                self.engine = texttospeech.TextToSpeechClient()
                self.provider_available = True
            except ImportError:
                self.provider_available = False
                print("⚠ Google Cloud TTS not installed. Run: pip install google-cloud-texttospeech")

        elif self.provider == "amazon_polly":
            try:
                import boto3
                self.engine = boto3.client(
                    'polly',
                    aws_access_key_id=API_KEYS["amazon_polly"]["access_key"],
                    aws_secret_access_key=API_KEYS["amazon_polly"]["secret_key"],
                    region_name=API_KEYS["amazon_polly"]["region"]
                )
                self.provider_available = True
            except ImportError:
                self.provider_available = False
                print("⚠ Boto3 not installed. Run: pip install boto3")

        elif self.provider == "elevenlabs":
            try:
                from elevenlabs import generate, set_api_key
                set_api_key(API_KEYS["elevenlabs"])
                self.engine = generate
                self.provider_available = True
            except ImportError:
                self.provider_available = False
                print("⚠ ElevenLabs not installed. Run: pip install elevenlabs")

        else:
            self.provider_available = False

    def _configure_pyttsx3(self):
        """Configure pyttsx3 engine with voice settings"""
        if not hasattr(self, 'engine') or self.engine is None:
            return

        voice_config = VOICE_SETTINGS.get("pyttsx3", {}).get(self.voice, {})

        if voice_config.get("rate"):
            self.engine.setProperty('rate', voice_config["rate"])
        if voice_config.get("volume") is not None:
            self.engine.setProperty('volume', voice_config["volume"])

        # Set voice if available
        voices = self.engine.getProperty('voices')
        voice_id = voice_config.get("voice_id", 0)
        if voices and len(voices) > voice_id:
            self.engine.setProperty('voice', voices[voice_id].id)

    def generate_audio(
        self,
        text: str,
        output_path: str,
        segment_name: str = "audio"
    ) -> str:
        """
        Generate audio from text.

        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            segment_name: Name of segment (for caching)

        Returns:
            Path to generated audio file

        Raises:
            AudioGenerationError: If generation fails
        """
        if not self.provider_available:
            raise AudioGenerationError(
                f"Provider '{self.provider}' is not available. "
                f"Install required dependencies."
            )

        # Check cache
        if self.options.get("cache_audio"):
            cache_path = self._get_cache_path(text, segment_name)
            if os.path.exists(cache_path):
                print(f"✓ Using cached audio: {cache_path}")
                return cache_path

        # Generate audio based on provider
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if self.provider == "gtts":
                self._generate_gtts(text, str(output_path))
            elif self.provider == "pyttsx3":
                self._generate_pyttsx3(text, str(output_path))
            elif self.provider == "google_cloud":
                self._generate_google_cloud(text, str(output_path))
            elif self.provider == "amazon_polly":
                self._generate_amazon_polly(text, str(output_path))
            elif self.provider == "elevenlabs":
                self._generate_elevenlabs(text, str(output_path))

            # Cache the audio
            if self.options.get("cache_audio"):
                self._cache_audio(str(output_path), text, segment_name)

            return str(output_path)

        except Exception as e:
            raise AudioGenerationError(f"Failed to generate audio: {e}")

    def _generate_gtts(self, text: str, output_path: str):
        """Generate audio using gTTS"""
        voice_config = VOICE_SETTINGS.get("gtts", {}).get(self.voice, {})

        tts = self.engine(
            text=text,
            lang=voice_config.get("language", "en"),
            tld=voice_config.get("tld", "com"),
            slow=voice_config.get("slow", False)
        )
        tts.save(output_path)
        print(f"✓ Generated audio with gTTS: {output_path}")

    def _generate_pyttsx3(self, text: str, output_path: str):
        """Generate audio using pyttsx3"""
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()
        print(f"✓ Generated audio with pyttsx3: {output_path}")

    def _generate_google_cloud(self, text: str, output_path: str):
        """Generate audio using Google Cloud TTS"""
        from google.cloud import texttospeech

        voice_config = VOICE_SETTINGS.get("google_cloud", {}).get(self.voice, {})

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=voice_config.get("language_code", "en-US"),
            name=voice_config.get("name"),
            ssml_gender=getattr(
                texttospeech.SsmlVoiceGender,
                voice_config.get("ssml_gender", "NEUTRAL")
            )
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=voice_config.get("speaking_rate", 1.0),
            pitch=voice_config.get("pitch", 0.0)
        )

        response = self.engine.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)

        print(f"✓ Generated audio with Google Cloud TTS: {output_path}")

    def _generate_amazon_polly(self, text: str, output_path: str):
        """Generate audio using Amazon Polly"""
        voice_config = VOICE_SETTINGS.get("amazon_polly", {}).get(self.voice, {})

        response = self.engine.synthesize_speech(
            Text=text,
            VoiceId=voice_config.get("voice_id", "Joanna"),
            Engine=voice_config.get("engine", "neural"),
            OutputFormat='mp3'
        )

        with open(output_path, "wb") as out:
            out.write(response['AudioStream'].read())

        print(f"✓ Generated audio with Amazon Polly: {output_path}")

    def _generate_elevenlabs(self, text: str, output_path: str):
        """Generate audio using ElevenLabs"""
        voice_config = VOICE_SETTINGS.get("elevenlabs", {}).get(self.voice, {})

        audio = self.engine(
            text=text,
            voice=voice_config.get("voice_id"),
            model=voice_config.get("model_id", "eleven_monolingual_v1")
        )

        with open(output_path, "wb") as out:
            out.write(audio)

        print(f"✓ Generated audio with ElevenLabs: {output_path}")

    def generate_from_script(
        self,
        script: Dict[str, Any],
        output_dir: str = "./audio_output"
    ) -> List[Dict[str, Any]]:
        """
        Generate audio files for all segments in a script.

        Args:
            script: Video script from ScriptGenerator
            output_dir: Directory to save audio files

        Returns:
            List of audio file information dictionaries
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        audio_files = []

        for i, segment in enumerate(script["segments"], 1):
            narration = segment.get("narration", "").strip()
            if not narration:
                continue

            segment_name = segment["name"]
            output_file = output_dir / f"{i:02d}_{segment_name}.mp3"

            try:
                audio_path = self.generate_audio(
                    narration,
                    str(output_file),
                    segment_name
                )

                audio_info = {
                    "segment_number": i,
                    "segment_name": segment_name,
                    "audio_path": audio_path,
                    "text": narration,
                    "start_time": segment.get("start_time", 0),
                    "duration": segment.get("duration", 0),
                }

                audio_files.append(audio_info)
                print(f"✓ [{i}/{len(script['segments'])}] Generated: {segment_name}")

            except Exception as e:
                print(f"✗ [{i}/{len(script['segments'])}] Failed: {segment_name} - {e}")
                continue

        return audio_files

    def _get_cache_path(self, text: str, segment_name: str) -> str:
        """Generate cache file path for text"""
        cache_dir = self.options.get("cache_dir", "./tts_cache")
        text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
        filename = f"{self.provider}_{segment_name}_{text_hash}.mp3"
        return os.path.join(cache_dir, filename)

    def _cache_audio(self, audio_path: str, text: str, segment_name: str):
        """Cache generated audio file"""
        cache_path = self._get_cache_path(text, segment_name)
        if audio_path != cache_path:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            import shutil
            shutil.copy2(audio_path, cache_path)

    def export_audio_manifest(
        self,
        audio_files: List[Dict[str, Any]],
        output_path: str
    ):
        """
        Export audio file manifest as JSON.

        Args:
            audio_files: List of audio file information
            output_path: Path to save manifest
        """
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "provider": self.provider,
            "voice": self.voice,
            "total_files": len(audio_files),
            "audio_files": audio_files,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"✓ Audio manifest exported: {output_path}")

    def get_generation_summary(
        self,
        audio_files: List[Dict[str, Any]]
    ) -> str:
        """Generate summary of audio generation"""
        total_files = len(audio_files)
        total_duration = sum(f.get("duration", 0) for f in audio_files)
        total_chars = sum(len(f.get("text", "")) for f in audio_files)

        summary = f"""
Audio Generation Summary
{'=' * 60}
Provider: {self.provider}
Voice: {self.voice}

Files Generated: {total_files}
Total Duration: {total_duration:.1f} seconds ({total_duration / 60:.1f} minutes)
Total Characters: {total_chars:,}

Audio Files:
"""

        for audio in audio_files:
            summary += f"  {audio['segment_number']:2d}. {audio['segment_name']:15} | "
            summary += f"{audio['duration']:5.1f}s | {len(audio['text']):4d} chars\n"

        return summary


# Convenience function
def generate_audio_from_script(
    script: Dict[str, Any],
    provider: str = "gtts",
    voice: str = "default",
    output_dir: str = "./audio_output"
) -> List[Dict[str, Any]]:
    """
    Quick function to generate audio from script.

    Args:
        script: Video script dictionary
        provider: TTS provider
        voice: Voice configuration
        output_dir: Output directory

    Returns:
        List of audio file information
    """
    generator = TTSGenerator(provider=provider, voice=voice)
    return generator.generate_from_script(script, output_dir)


if __name__ == "__main__":
    print("Text-to-Speech Generator Module")
    print("=" * 60)
    print(f"\nAvailable providers: {', '.join(TTS_PROVIDERS.keys())}")
    print(f"Default provider: {DEFAULT_PROVIDER}")
    print("\nThis module converts video scripts to audio files.")
    print("See examples/tts_generator_example.py for usage examples.")
