"""
Video Composer Module

Combines script data and audio files to create final videos with visuals,
text overlays, transitions, and effects.

Example:
    composer = VideoComposer(format_type="youtube")
    video_path = composer.compose_video(script, audio_files, "output.mp4")
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

try:
    from moviepy.editor import (
        VideoClip, AudioFileClip, CompositeVideoClip, TextClip,
        ColorClip, ImageClip, concatenate_videoclips
    )
    from moviepy.video.fx import fadein, fadeout, resize
    from moviepy.video.tools.subtitles import SubtitlesClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠ MoviePy not installed. Run: pip install moviepy")

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠ Pillow not installed. Run: pip install Pillow")

try:
    from video_config import (
        VIDEO_FORMATS,
        DEFAULT_FORMAT,
        BACKGROUND_SETTINGS,
        TEXT_SETTINGS,
        ANIMATION_SETTINGS,
        RENDERING_SETTINGS,
        EXPORT_SETTINGS,
        CAPTION_SETTINGS,
    )
except ImportError:
    print("Warning: video_config.py not found. Using defaults.")
    VIDEO_FORMATS = {}
    DEFAULT_FORMAT = "youtube"
    BACKGROUND_SETTINGS = {}
    TEXT_SETTINGS = {}
    ANIMATION_SETTINGS = {}
    RENDERING_SETTINGS = {}
    EXPORT_SETTINGS = {}
    CAPTION_SETTINGS = {}


class VideoComposerError(Exception):
    """Base exception for video composer errors"""
    pass


class InvalidFormatError(VideoComposerError):
    """Raised when video format is invalid"""
    pass


class RenderingError(VideoComposerError):
    """Raised when video rendering fails"""
    pass


class VideoComposer:
    """
    Compose videos from scripts and audio files.

    Attributes:
        format_type: Video format (youtube, tiktok, etc.)
        resolution: Video resolution tuple
        fps: Frames per second
    """

    def __init__(
        self,
        format_type: str = None,
        resolution: Tuple[int, int] = None,
        fps: int = 30,
        options: Optional[Dict] = None
    ):
        """
        Initialize Video Composer.

        Args:
            format_type: Video format preset
            resolution: Custom resolution (overrides format)
            fps: Frames per second
            options: Custom composition options

        Raises:
            InvalidFormatError: If format is invalid
        """
        if not MOVIEPY_AVAILABLE:
            raise VideoComposerError(
                "MoviePy is required for video composition. "
                "Install with: pip install moviepy"
            )

        self.format_type = format_type or DEFAULT_FORMAT
        self.options = {**RENDERING_SETTINGS, **(options or {})}

        # Get format configuration
        if self.format_type not in VIDEO_FORMATS:
            raise InvalidFormatError(
                f"Invalid format: {self.format_type}. "
                f"Available: {', '.join(VIDEO_FORMATS.keys())}"
            )

        format_config = VIDEO_FORMATS[self.format_type]
        self.resolution = resolution or format_config["resolution"]
        self.fps = fps or format_config.get("fps", 30)
        self.codec = format_config.get("codec", "libx264")
        self.audio_codec = format_config.get("audio_codec", "aac")
        self.bitrate = format_config.get("bitrate", "8000k")

        # Create output directory
        os.makedirs(EXPORT_SETTINGS.get("output_dir", "./video_output"), exist_ok=True)

    def compose_video(
        self,
        script: Dict[str, Any],
        audio_files: List[Dict[str, Any]],
        output_path: str,
        background_music: Optional[str] = None
    ) -> str:
        """
        Compose complete video from script and audio files.

        Args:
            script: Video script from ScriptGenerator
            audio_files: List of audio file info from TTSGenerator
            output_path: Path for output video
            background_music: Optional path to background music

        Returns:
            Path to rendered video file

        Raises:
            RenderingError: If video rendering fails
        """
        print(f"Composing video: {output_path}")
        print(f"  Format: {self.format_type}")
        print(f"  Resolution: {self.resolution[0]}x{self.resolution[1]}")
        print(f"  FPS: {self.fps}")

        try:
            # Create video clips for each segment
            video_clips = []
            for i, segment in enumerate(script["segments"], 1):
                print(f"  Creating segment {i}/{len(script['segments'])}: {segment['name']}")

                # Find corresponding audio file
                audio_info = next(
                    (a for a in audio_files if a["segment_name"] == segment["name"]),
                    None
                )

                # Create video clip for segment
                clip = self._create_segment_clip(segment, audio_info, script)
                if clip:
                    video_clips.append(clip)

            if not video_clips:
                raise RenderingError("No video clips were created")

            # Concatenate all clips
            print("  Combining segments...")
            final_clip = concatenate_videoclips(video_clips, method="compose")

            # Add background music if provided
            if background_music and os.path.exists(background_music):
                print("  Adding background music...")
                final_clip = self._add_background_music(final_clip, background_music)

            # Render final video
            print(f"  Rendering video...")
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            final_clip.write_videofile(
                str(output_path),
                fps=self.fps,
                codec=self.codec,
                audio_codec=self.audio_codec,
                bitrate=self.bitrate,
                preset=self.options.get("preset", "medium"),
                threads=self.options.get("threads", 4),
                verbose=self.options.get("verbose", False),
                logger=None if not self.options.get("verbose") else "bar"
            )

            # Clean up
            final_clip.close()
            for clip in video_clips:
                clip.close()

            print(f"✓ Video rendered successfully: {output_path}")
            return str(output_path)

        except Exception as e:
            raise RenderingError(f"Failed to compose video: {e}")

    def _create_segment_clip(
        self,
        segment: Dict[str, Any],
        audio_info: Optional[Dict[str, Any]],
        script: Dict[str, Any]
    ) -> Optional[Any]:
        """Create video clip for a single segment"""
        # Get segment duration from audio or script
        if audio_info and os.path.exists(audio_info.get("audio_path", "")):
            audio_clip = AudioFileClip(audio_info["audio_path"])
            duration = audio_clip.duration
        else:
            duration = segment.get("duration", 5.0)
            audio_clip = None

        # Create background
        background = self._create_background(duration)

        # Create text overlay
        text_clip = self._create_text_overlay(
            segment.get("narration", ""),
            duration,
            segment.get("type", "body")
        )

        # Combine background and text
        if text_clip:
            video_clip = CompositeVideoClip(
                [background, text_clip],
                size=self.resolution
            )
        else:
            video_clip = background

        # Add audio
        if audio_clip:
            video_clip = video_clip.set_audio(audio_clip)

        # Apply animations
        if ANIMATION_SETTINGS.get("enable_animations", True):
            fade_in = ANIMATION_SETTINGS.get("text_fade_in", 0.3)
            fade_out = ANIMATION_SETTINGS.get("text_fade_out", 0.3)

            if duration > fade_in + fade_out:
                video_clip = video_clip.fx(fadein, fade_in)
                video_clip = video_clip.fx(fadeout, fade_out)

        return video_clip

    def _create_background(self, duration: float) -> Any:
        """Create background clip"""
        bg_settings = BACKGROUND_SETTINGS

        bg_type = bg_settings.get("type", "solid")

        if bg_type == "solid":
            color = self._hex_to_rgb(bg_settings.get("color", "#1a1a2e"))
            background = ColorClip(
                size=self.resolution,
                color=color,
                duration=duration
            )

        elif bg_type == "gradient":
            # Create gradient using PIL
            background = self._create_gradient_background(duration)

        elif bg_type == "image" and bg_settings.get("image_path"):
            # Load image background
            background = ImageClip(bg_settings["image_path"], duration=duration)
            background = background.resize(self.resolution)

        else:
            # Default to solid color
            background = ColorClip(
                size=self.resolution,
                color=(26, 26, 46),  # Default dark blue
                duration=duration
            )

        return background

    def _create_gradient_background(self, duration: float) -> Any:
        """Create gradient background using PIL"""
        if not PIL_AVAILABLE:
            # Fallback to solid color
            return ColorClip(size=self.resolution, color=(26, 26, 46), duration=duration)

        width, height = self.resolution
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Get colors
        color1 = self._hex_to_rgb(BACKGROUND_SETTINGS.get("color", "#1a1a2e"))
        color2 = self._hex_to_rgb(BACKGROUND_SETTINGS.get("color_end", "#16213e"))

        # Create vertical gradient
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Convert to video clip
        img_path = "/tmp/gradient_bg.png"
        img.save(img_path)
        background = ImageClip(img_path, duration=duration)

        return background

    def _create_text_overlay(
        self,
        text: str,
        duration: float,
        segment_type: str = "body"
    ) -> Optional[Any]:
        """Create text overlay for segment"""
        if not text:
            return None

        text_settings = TEXT_SETTINGS

        # Determine text size based on segment type
        if segment_type in ["intro", "title", "outro"]:
            fontsize = text_settings.get("title_size", 80)
        elif segment_type == "comments":
            fontsize = text_settings.get("comment_size", 50)
        else:
            fontsize = text_settings.get("body_size", 60)

        # Create text clip
        try:
            txt_clip = TextClip(
                text,
                fontsize=fontsize,
                color=text_settings.get("color", "white"),
                font=text_settings.get("font", "Arial-Bold"),
                method='caption',
                size=(self.resolution[0] - 100, None),  # Leave padding
                align='center'
            )

            # Position text
            txt_clip = txt_clip.set_position("center").set_duration(duration)

            # Add stroke/outline
            if text_settings.get("stroke_width", 0) > 0:
                txt_clip = txt_clip.on_color(
                    size=(txt_clip.w + 20, txt_clip.h + 20),
                    color=(0, 0, 0),
                    pos=('center', 'center'),
                    col_opacity=0
                )

            return txt_clip

        except Exception as e:
            print(f"⚠ Failed to create text clip: {e}")
            return None

    def _add_background_music(
        self,
        video_clip: Any,
        music_path: str
    ) -> Any:
        """Add background music to video"""
        try:
            music = AudioFileClip(music_path)

            # Loop music if needed
            if music.duration < video_clip.duration:
                n_loops = int(video_clip.duration / music.duration) + 1
                music = music.loop(n=n_loops)

            # Trim to video length
            music = music.subclip(0, video_clip.duration)

            # Reduce volume
            music_volume = 0.15  # 15% of original
            music = music.volumex(music_volume)

            # Mix with narration
            if video_clip.audio:
                final_audio = CompositeAudioClip([video_clip.audio, music])
                video_clip = video_clip.set_audio(final_audio)
            else:
                video_clip = video_clip.set_audio(music)

            return video_clip

        except Exception as e:
            print(f"⚠ Failed to add background music: {e}")
            return video_clip

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def generate_thumbnail(
        self,
        script: Dict[str, Any],
        output_path: str
    ) -> str:
        """
        Generate thumbnail image for video.

        Args:
            script: Video script
            output_path: Path for thumbnail image

        Returns:
            Path to thumbnail image
        """
        if not PIL_AVAILABLE:
            raise VideoComposerError("Pillow is required for thumbnail generation")

        width, height = (1280, 720)  # Standard YouTube thumbnail
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Create gradient background
        color1 = self._hex_to_rgb("#1a1a2e")
        color2 = self._hex_to_rgb("#FF6B6B")

        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Add title text
        title = script["metadata"]["title"]
        if len(title) > 60:
            title = title[:57] + "..."

        # Try to load a font, fall back to default
        try:
            font = ImageFont.truetype("Arial.ttf", 80)
        except:
            font = ImageFont.load_default()

        # Calculate text size and position
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw text with outline
        outline_range = 3
        for adj_x in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj_x, y + adj_y), title, font=font, fill=(0, 0, 0))

        # Draw main text
        draw.text((x, y), title, font=font, fill=(255, 255, 255))

        # Save thumbnail
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path))

        print(f"✓ Thumbnail generated: {output_path}")
        return str(output_path)

    def get_composition_summary(
        self,
        script: Dict[str, Any],
        video_path: str
    ) -> str:
        """Generate summary of video composition"""
        summary = f"""
Video Composition Summary
{'=' * 60}
Title: {script['metadata']['title']}
Format: {self.format_type}
Resolution: {self.resolution[0]}x{self.resolution[1]}
FPS: {self.fps}

Output: {video_path}
Segments: {len(script['segments'])}
Total Duration: {script['total_duration']:.1f} seconds

Segment Breakdown:
"""

        for segment in script["segments"]:
            summary += f"  {segment['name']:15} | {segment['duration']:5.1f}s\n"

        return summary


# Convenience function
def compose_video_from_script(
    script: Dict[str, Any],
    audio_files: List[Dict[str, Any]],
    output_path: str,
    format_type: str = "youtube",
    background_music: Optional[str] = None
) -> str:
    """
    Quick function to compose video.

    Args:
        script: Video script
        audio_files: Audio file information
        output_path: Output video path
        format_type: Video format
        background_music: Optional background music path

    Returns:
        Path to rendered video
    """
    composer = VideoComposer(format_type=format_type)
    return composer.compose_video(script, audio_files, output_path, background_music)


if __name__ == "__main__":
    print("Video Composer Module")
    print("=" * 60)
    print(f"\nAvailable formats: {', '.join(VIDEO_FORMATS.keys())}")
    print(f"Default format: {DEFAULT_FORMAT}")
    print("\nThis module composes final videos from scripts and audio.")
    print("See examples/video_composer_example.py for usage examples.")
