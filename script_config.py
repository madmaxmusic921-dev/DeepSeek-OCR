"""
Video Script Generator Configuration

Configure video script generation settings for different platforms and formats.
"""

import os

# Video Format Presets
VIDEO_FORMATS = {
    "tiktok": {
        "name": "TikTok / YouTube Shorts",
        "max_duration": 60,  # seconds
        "optimal_duration": 30,
        "min_duration": 15,
        "aspect_ratio": "9:16",  # vertical
        "target_audience": "quick engagement",
        "pacing": "fast",
    },
    "instagram": {
        "name": "Instagram Reels",
        "max_duration": 90,
        "optimal_duration": 60,
        "min_duration": 30,
        "aspect_ratio": "9:16",
        "target_audience": "social media",
        "pacing": "medium",
    },
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "max_duration": 60,
        "optimal_duration": 45,
        "min_duration": 15,
        "aspect_ratio": "9:16",
        "target_audience": "quick content",
        "pacing": "fast",
    },
    "youtube": {
        "name": "YouTube (Standard)",
        "max_duration": 600,  # 10 minutes
        "optimal_duration": 180,  # 3 minutes
        "min_duration": 60,
        "aspect_ratio": "16:9",  # horizontal
        "target_audience": "in-depth",
        "pacing": "slow",
    },
    "facebook": {
        "name": "Facebook Video",
        "max_duration": 240,  # 4 minutes
        "optimal_duration": 90,
        "min_duration": 30,
        "aspect_ratio": "1:1",  # square
        "target_audience": "social sharing",
        "pacing": "medium",
    },
}

# Script Generation Options
SCRIPT_OPTIONS = {
    # Text-to-Speech settings
    "words_per_minute": 150,  # Average speaking pace
    "pause_duration": 0.5,  # Seconds between segments
    "emphasis_pause": 1.0,  # Seconds for dramatic pauses

    # Content settings
    "max_title_words": 15,
    "max_comment_length": 200,  # characters
    "show_usernames": True,
    "show_scores": True,
    "show_awards": True,
    "censor_profanity": False,

    # Visual settings
    "include_background_music": True,
    "include_sound_effects": True,
    "text_animation": True,
    "transition_effects": True,

    # Narration style
    "narration_style": "casual",  # casual, formal, dramatic, comedic
    "use_first_person": False,
    "add_commentary": False,
}

# Segment Timing (in seconds)
SEGMENT_TIMING = {
    "intro": {
        "short": 3,
        "medium": 5,
        "long": 8,
    },
    "title": {
        "short": 4,
        "medium": 6,
        "long": 8,
    },
    "context": {
        "short": 0,
        "medium": 3,
        "long": 10,
    },
    "body": {
        "short": 15,
        "medium": 30,
        "long": 90,
    },
    "comments": {
        "short": 8,
        "medium": 15,
        "long": 40,
    },
    "engagement": {
        "short": 0,
        "medium": 3,
        "long": 8,
    },
    "outro": {
        "short": 3,
        "medium": 5,
        "long": 10,
    },
}

# Comment Selection Criteria
COMMENT_SELECTION = {
    "short": {
        "max_comments": 1,
        "min_score": 100,
        "prefer_op_reply": True,
        "max_depth": 1,
    },
    "medium": {
        "max_comments": 3,
        "min_score": 50,
        "prefer_op_reply": True,
        "max_depth": 2,
    },
    "long": {
        "max_comments": 10,
        "min_score": 10,
        "prefer_op_reply": True,
        "max_depth": 3,
        "include_replies": True,
    },
}

# Narration Templates
NARRATION_TEMPLATES = {
    "intro": {
        "casual": [
            "Check out this post from Reddit",
            "Here's an interesting story from r/{subreddit}",
            "You won't believe what happened on Reddit",
            "This Reddit post is wild",
            "Let me tell you about this Reddit story",
        ],
        "formal": [
            "Today we're looking at a post from r/{subreddit}",
            "This is a story that was shared on Reddit",
            "A user on Reddit shared this interesting post",
        ],
        "dramatic": [
            "This is the story that shocked Reddit",
            "What you're about to hear will blow your mind",
            "The internet went crazy over this post",
        ],
        "comedic": [
            "Reddit never disappoints, and this post proves it",
            "Hold onto your hats for this one folks",
            "The internet is a weird place, and here's proof",
        ],
    },
    "transition": {
        "to_comments": [
            "Let's see what people had to say",
            "The comments section did not disappoint",
            "Here's what Redditors thought",
            "The best part is in the comments",
        ],
        "to_outro": [
            "And that's the story",
            "That wraps it up",
            "What do you think?",
            "That's all for this one",
        ],
    },
    "engagement": [
        "What do you think about this?",
        "Let me know in the comments",
        "Would you do the same thing?",
        "This is crazy, right?",
        "Drop your thoughts below",
    ],
    "outro": [
        "Thanks for watching! Hit that subscribe button for more Reddit content",
        "Don't forget to like and subscribe",
        "Follow for more stories from Reddit",
        "See you in the next one",
        "That's it for today, catch you later",
    ],
}

# Visual Cues
VISUAL_CUES = {
    "text_appear": "fade_in",
    "text_disappear": "fade_out",
    "transition": "swipe",
    "emphasis": "zoom",
    "comment_highlight": "highlight_box",
}

# Background Music Categories
BACKGROUND_MUSIC = {
    "casual": ["lofi", "chill", "ambient"],
    "dramatic": ["epic", "suspense", "orchestral"],
    "comedic": ["upbeat", "quirky", "playful"],
    "formal": ["corporate", "neutral", "minimal"],
}

# Export Formats
EXPORT_FORMATS = {
    "json": {
        "extension": ".json",
        "include_timing": True,
        "include_visuals": True,
        "human_readable": True,
    },
    "txt": {
        "extension": ".txt",
        "include_timing": True,
        "include_visuals": False,
        "human_readable": True,
    },
    "srt": {
        "extension": ".srt",
        "subtitle_format": True,
        "max_chars_per_line": 42,
        "max_lines": 2,
    },
    "vtt": {
        "extension": ".vtt",
        "subtitle_format": True,
        "supports_styling": True,
    },
}

# Profanity Filter (if enabled)
PROFANITY_REPLACEMENTS = {
    # Map of words to replace - add your own list
    "example": "****",
}

# Text-to-Speech Settings
TTS_SETTINGS = {
    "default_voice": "neutral",
    "speech_rate": 1.0,  # 1.0 is normal speed
    "pitch": 1.0,  # 1.0 is normal pitch
    "volume": 1.0,  # 1.0 is normal volume
}

# File Naming Convention
FILE_NAMING = {
    "pattern": "{subreddit}_{post_id}_{format}_{timestamp}",
    "use_timestamp": True,
    "lowercase": True,
    "remove_special_chars": True,
}
