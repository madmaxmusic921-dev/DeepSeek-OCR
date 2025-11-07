"""
Video Composition Configuration

Configure video output settings, visual styles, and rendering options.
"""

import os

# Video Format Presets
VIDEO_FORMATS = {
    "tiktok": {
        "name": "TikTok / YouTube Shorts",
        "resolution": (1080, 1920),  # 9:16 vertical
        "fps": 30,
        "bitrate": "8000k",
        "codec": "libx264",
        "audio_codec": "aac",
        "max_duration": 60,
        "aspect_ratio": "9:16",
    },
    "instagram": {
        "name": "Instagram Reels",
        "resolution": (1080, 1920),  # 9:16 vertical
        "fps": 30,
        "bitrate": "8000k",
        "codec": "libx264",
        "audio_codec": "aac",
        "max_duration": 90,
        "aspect_ratio": "9:16",
    },
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "resolution": (1080, 1920),  # 9:16 vertical
        "fps": 30,
        "bitrate": "8000k",
        "codec": "libx264",
        "audio_codec": "aac",
        "max_duration": 60,
        "aspect_ratio": "9:16",
    },
    "youtube": {
        "name": "YouTube (1080p)",
        "resolution": (1920, 1080),  # 16:9 horizontal
        "fps": 30,
        "bitrate": "10000k",
        "codec": "libx264",
        "audio_codec": "aac",
        "max_duration": 600,
        "aspect_ratio": "16:9",
    },
    "youtube_4k": {
        "name": "YouTube (4K)",
        "resolution": (3840, 2160),  # 16:9 horizontal
        "fps": 60,
        "bitrate": "20000k",
        "codec": "libx264",
        "audio_codec": "aac",
        "max_duration": 600,
        "aspect_ratio": "16:9",
    },
    "facebook": {
        "name": "Facebook Video",
        "resolution": (1080, 1080),  # 1:1 square
        "fps": 30,
        "bitrate": "8000k",
        "codec": "libx264",
        "audio_codec": "aac",
        "max_duration": 240,
        "aspect_ratio": "1:1",
    },
}

# Default format
DEFAULT_FORMAT = "youtube"

# Background Settings
BACKGROUND_SETTINGS = {
    "type": "gradient",  # solid, gradient, image, video
    "color": "#1a1a2e",  # Solid color or gradient start
    "color_end": "#16213e",  # Gradient end color
    "image_path": None,  # Path to background image
    "video_path": None,  # Path to background video
    "blur": 0,  # Blur amount for images/videos
    "opacity": 1.0,  # Background opacity
}

# Text Settings
TEXT_SETTINGS = {
    "font": "Arial-Bold",  # Font name
    "title_size": 80,  # Title text size
    "body_size": 60,  # Body text size
    "comment_size": 50,  # Comment text size
    "color": "white",  # Text color
    "stroke_color": "black",  # Text outline color
    "stroke_width": 2,  # Outline width
    "align": "center",  # left, center, right
    "method": "caption",  # label or caption
    "position": "center",  # Position on screen
    "padding": 50,  # Padding from edges
    "shadow": True,  # Enable text shadow
    "shadow_offset": (3, 3),  # Shadow offset
}

# Animation Settings
ANIMATION_SETTINGS = {
    "text_fade_in": 0.3,  # seconds
    "text_fade_out": 0.3,  # seconds
    "slide_duration": 0.5,  # seconds for slide transitions
    "zoom_factor": 1.1,  # Zoom animation factor
    "enable_animations": True,  # Global animation toggle
}

# Overlay Settings (Reddit branding, etc.)
OVERLAY_SETTINGS = {
    "show_subreddit": True,
    "show_username": True,
    "show_score": True,
    "reddit_logo": None,  # Path to Reddit logo
    "watermark": None,  # Path to watermark image
    "watermark_position": "bottom-right",  # Position of watermark
    "watermark_opacity": 0.7,
}

# Audio Settings
AUDIO_SETTINGS = {
    "background_music": False,
    "music_path": None,  # Path to background music
    "music_volume": 0.15,  # 15% of narration volume
    "fade_in": 2.0,  # Music fade in duration
    "fade_out": 3.0,  # Music fade out duration
    "normalize_audio": True,  # Normalize audio levels
}

# Rendering Settings
RENDERING_SETTINGS = {
    "threads": 4,  # Number of threads for rendering
    "preset": "medium",  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    "audio_bitrate": "192k",
    "remove_temp": True,  # Remove temporary files after rendering
    "verbose": False,  # Show detailed rendering output
}

# Visual Styles
VISUAL_STYLES = {
    "minimal": {
        "background": {"type": "solid", "color": "#000000"},
        "text_color": "white",
        "animations": False,
        "overlays": False,
    },
    "modern": {
        "background": {"type": "gradient", "color": "#1a1a2e", "color_end": "#16213e"},
        "text_color": "white",
        "animations": True,
        "overlays": True,
    },
    "vibrant": {
        "background": {"type": "gradient", "color": "#FF6B6B", "color_end": "#4ECDC4"},
        "text_color": "white",
        "animations": True,
        "overlays": True,
    },
    "professional": {
        "background": {"type": "solid", "color": "#f5f5f5"},
        "text_color": "#333333",
        "animations": False,
        "overlays": True,
    },
}

# Segment Visual Templates
SEGMENT_TEMPLATES = {
    "intro": {
        "background": "gradient",
        "text_size": 80,
        "text_position": "center",
        "animation": "fade",
        "duration_min": 3,
        "duration_max": 8,
    },
    "title": {
        "background": "gradient",
        "text_size": 70,
        "text_position": "center",
        "animation": "slide_up",
        "duration_min": 4,
        "duration_max": 8,
    },
    "body": {
        "background": "solid",
        "text_size": 60,
        "text_position": "center",
        "animation": "fade",
        "scroll": True,
        "duration_min": 15,
        "duration_max": 90,
    },
    "comments": {
        "background": "solid",
        "text_size": 50,
        "text_position": "top",
        "animation": "slide_up",
        "show_avatars": False,
        "duration_min": 8,
        "duration_max": 40,
    },
    "outro": {
        "background": "gradient",
        "text_size": 70,
        "text_position": "center",
        "animation": "fade",
        "duration_min": 3,
        "duration_max": 10,
    },
}

# Export Settings
EXPORT_SETTINGS = {
    "output_dir": "./video_output",
    "filename_pattern": "{subreddit}_{post_id}_{timestamp}",
    "format": "mp4",
    "include_metadata": True,  # Include metadata in video file
}

# Color Schemes
COLOR_SCHEMES = {
    "dark": {
        "background": "#1a1a2e",
        "text": "#ffffff",
        "accent": "#FF6B6B",
    },
    "light": {
        "background": "#f5f5f5",
        "text": "#333333",
        "accent": "#4ECDC4",
    },
    "reddit": {
        "background": "#0d1117",
        "text": "#ffffff",
        "accent": "#FF4500",  # Reddit orange
    },
    "youtube": {
        "background": "#282828",
        "text": "#ffffff",
        "accent": "#FF0000",  # YouTube red
    },
}

# Thumbnail Settings
THUMBNAIL_SETTINGS = {
    "generate": True,
    "resolution": (1280, 720),  # Standard YouTube thumbnail
    "text_size": 100,
    "add_face": False,  # Add reaction face/emoji
    "style": "bold",  # bold, minimal, colorful
}

# Progress Indicators
PROGRESS_SETTINGS = {
    "show_progress": True,
    "progress_bar_height": 5,
    "progress_bar_color": "#FF4500",
    "progress_bar_position": "bottom",
}

# Captions/Subtitles
CAPTION_SETTINGS = {
    "enabled": True,
    "style": "word_highlight",  # word_highlight, sentence, or none
    "highlight_color": "#FFFF00",  # Yellow highlight
    "font_size": 70,
    "position": "center",
    "max_words_per_line": 6,
    "background": True,  # Background box for captions
    "background_color": "rgba(0, 0, 0, 0.7)",
}

# Transition Effects
TRANSITION_EFFECTS = {
    "enabled": True,
    "default": "fade",  # fade, slide, zoom, wipe
    "duration": 0.5,  # seconds
}

# Error Messages
ERROR_MESSAGES = {
    "audio_not_found": "Audio file not found: {path}",
    "invalid_format": "Invalid video format: {format}",
    "rendering_failed": "Video rendering failed: {error}",
    "missing_script": "Script data is missing required fields",
}

# Temporary Files
TEMP_SETTINGS = {
    "temp_dir": "./video_temp",
    "keep_temp_files": False,  # Keep temporary files for debugging
    "cleanup_on_error": True,  # Clean up even if error occurs
}
