"""
Video Script Templates

Provides templates for different video formats and styles.
Each template defines the structure and flow of the video.
"""

from typing import Dict, List, Any


class ScriptTemplate:
    """Base class for script templates"""

    def __init__(self, format_type: str):
        self.format_type = format_type
        self.segments = []

    def get_structure(self) -> List[Dict[str, Any]]:
        """Return the script structure"""
        return self.segments


class ShortFormTemplate(ScriptTemplate):
    """Template for short-form content (15-60 seconds)"""

    def __init__(self):
        super().__init__("short")
        self.segments = [
            {
                "name": "hook",
                "duration": 3,
                "required": True,
                "content_type": "title",
                "narration": "attention_grabbing",
                "visual": "title_screen",
            },
            {
                "name": "body",
                "duration": 15,
                "required": True,
                "content_type": "post_body",
                "narration": "main_content",
                "visual": "text_overlay",
            },
            {
                "name": "top_comment",
                "duration": 8,
                "required": False,
                "content_type": "comments",
                "narration": "comment_reaction",
                "visual": "comment_highlight",
            },
            {
                "name": "outro",
                "duration": 3,
                "required": True,
                "content_type": "call_to_action",
                "narration": "engagement",
                "visual": "cta_screen",
            },
        ]


class MediumFormTemplate(ScriptTemplate):
    """Template for medium-form content (60-120 seconds)"""

    def __init__(self):
        super().__init__("medium")
        self.segments = [
            {
                "name": "intro",
                "duration": 5,
                "required": True,
                "content_type": "intro",
                "narration": "greeting",
                "visual": "animated_intro",
            },
            {
                "name": "title",
                "duration": 6,
                "required": True,
                "content_type": "title",
                "narration": "title_read",
                "visual": "title_screen",
            },
            {
                "name": "context",
                "duration": 3,
                "required": False,
                "content_type": "metadata",
                "narration": "background",
                "visual": "stats_display",
            },
            {
                "name": "body",
                "duration": 30,
                "required": True,
                "content_type": "post_body",
                "narration": "main_content",
                "visual": "text_overlay",
            },
            {
                "name": "comments",
                "duration": 15,
                "required": True,
                "content_type": "comments",
                "narration": "comment_reactions",
                "visual": "comment_section",
            },
            {
                "name": "engagement",
                "duration": 3,
                "required": False,
                "content_type": "engagement",
                "narration": "question",
                "visual": "engagement_prompt",
            },
            {
                "name": "outro",
                "duration": 5,
                "required": True,
                "content_type": "call_to_action",
                "narration": "subscribe_reminder",
                "visual": "outro_screen",
            },
        ]


class LongFormTemplate(ScriptTemplate):
    """Template for long-form content (3+ minutes)"""

    def __init__(self):
        super().__init__("long")
        self.segments = [
            {
                "name": "cold_open",
                "duration": 8,
                "required": False,
                "content_type": "teaser",
                "narration": "hook",
                "visual": "dramatic_opener",
            },
            {
                "name": "intro",
                "duration": 8,
                "required": True,
                "content_type": "intro",
                "narration": "channel_intro",
                "visual": "branded_intro",
            },
            {
                "name": "title",
                "duration": 8,
                "required": True,
                "content_type": "title",
                "narration": "title_with_context",
                "visual": "title_animation",
            },
            {
                "name": "context",
                "duration": 10,
                "required": True,
                "content_type": "metadata",
                "narration": "detailed_background",
                "visual": "context_graphics",
            },
            {
                "name": "body_part_1",
                "duration": 45,
                "required": True,
                "content_type": "post_body",
                "narration": "main_content",
                "visual": "scrolling_text",
            },
            {
                "name": "mid_engagement",
                "duration": 8,
                "required": True,
                "content_type": "engagement",
                "narration": "like_reminder",
                "visual": "like_button_animation",
            },
            {
                "name": "body_part_2",
                "duration": 45,
                "required": False,
                "content_type": "post_continuation",
                "narration": "continued_content",
                "visual": "scrolling_text",
            },
            {
                "name": "comments",
                "duration": 40,
                "required": True,
                "content_type": "comments",
                "narration": "comment_analysis",
                "visual": "comment_thread",
            },
            {
                "name": "engagement",
                "duration": 8,
                "required": True,
                "content_type": "engagement",
                "narration": "discussion_prompt",
                "visual": "poll_or_question",
            },
            {
                "name": "outro",
                "duration": 10,
                "required": True,
                "content_type": "outro",
                "narration": "thanks_and_subscribe",
                "visual": "end_screen",
            },
        ]


class StoryTimeTemplate(ScriptTemplate):
    """Template for story-style narrative videos"""

    def __init__(self):
        super().__init__("story")
        self.segments = [
            {
                "name": "hook",
                "duration": 5,
                "required": True,
                "content_type": "title",
                "narration": "story_hook",
                "visual": "dramatic_text",
            },
            {
                "name": "setup",
                "duration": 15,
                "required": True,
                "content_type": "context",
                "narration": "story_setup",
                "visual": "background_visuals",
            },
            {
                "name": "story",
                "duration": 60,
                "required": True,
                "content_type": "post_body",
                "narration": "story_telling",
                "visual": "story_visuals",
            },
            {
                "name": "reactions",
                "duration": 30,
                "required": True,
                "content_type": "comments",
                "narration": "reaction_summary",
                "visual": "comment_reactions",
            },
            {
                "name": "conclusion",
                "duration": 10,
                "required": True,
                "content_type": "outro",
                "narration": "story_wrap",
                "visual": "conclusion_screen",
            },
        ]


class CompilationTemplate(ScriptTemplate):
    """Template for compilation videos with multiple posts"""

    def __init__(self):
        super().__init__("compilation")
        self.segments = [
            {
                "name": "intro",
                "duration": 10,
                "required": True,
                "content_type": "intro",
                "narration": "compilation_intro",
                "visual": "montage",
            },
            {
                "name": "post_segment",
                "duration": 30,
                "required": True,
                "content_type": "post_block",
                "narration": "post_summary",
                "visual": "post_display",
                "repeatable": True,
            },
            {
                "name": "outro",
                "duration": 10,
                "required": True,
                "content_type": "outro",
                "narration": "compilation_outro",
                "visual": "end_montage",
            },
        ]


# Template Factory
TEMPLATES = {
    "short": ShortFormTemplate,
    "medium": MediumFormTemplate,
    "long": LongFormTemplate,
    "story": StoryTimeTemplate,
    "compilation": CompilationTemplate,
}


def get_template(template_name: str) -> ScriptTemplate:
    """
    Get a script template by name.

    Args:
        template_name: Name of template (short, medium, long, story, compilation)

    Returns:
        ScriptTemplate instance

    Raises:
        ValueError: If template name is invalid
    """
    if template_name not in TEMPLATES:
        raise ValueError(
            f"Invalid template: {template_name}. "
            f"Available templates: {', '.join(TEMPLATES.keys())}"
        )
    return TEMPLATES[template_name]()


def list_templates() -> List[str]:
    """Return list of available template names"""
    return list(TEMPLATES.keys())


def get_template_info(template_name: str) -> Dict[str, Any]:
    """
    Get information about a template.

    Args:
        template_name: Name of template

    Returns:
        Dictionary with template information
    """
    template = get_template(template_name)
    total_duration = sum(seg["duration"] for seg in template.segments)
    required_segments = [seg["name"] for seg in template.segments if seg["required"]]

    return {
        "name": template_name,
        "format_type": template.format_type,
        "total_segments": len(template.segments),
        "required_segments": len(required_segments),
        "estimated_duration": total_duration,
        "segment_names": [seg["name"] for seg in template.segments],
    }


# Narration Style Modifiers
NARRATION_STYLES = {
    "casual": {
        "tone": "friendly and conversational",
        "formality": "low",
        "contractions": True,
        "slang": True,
        "examples": ["Check this out!", "This is wild!", "No way!"],
    },
    "formal": {
        "tone": "professional and clear",
        "formality": "high",
        "contractions": False,
        "slang": False,
        "examples": [
            "Today we examine",
            "It is important to note",
            "In conclusion",
        ],
    },
    "dramatic": {
        "tone": "intense and engaging",
        "formality": "medium",
        "contractions": True,
        "slang": False,
        "examples": [
            "You won't believe what happens next",
            "This is shocking",
            "The truth revealed",
        ],
    },
    "comedic": {
        "tone": "humorous and lighthearted",
        "formality": "low",
        "contractions": True,
        "slang": True,
        "examples": [
            "Oh boy, here we go",
            "This is hilarious",
            "Wait until you hear this",
        ],
    },
    "educational": {
        "tone": "informative and clear",
        "formality": "medium",
        "contractions": False,
        "slang": False,
        "examples": [
            "Let's break this down",
            "Here's what you need to know",
            "This demonstrates",
        ],
    },
}


def get_narration_style(style_name: str) -> Dict[str, Any]:
    """Get narration style configuration"""
    return NARRATION_STYLES.get(
        style_name, NARRATION_STYLES["casual"]
    )  # Default to casual


if __name__ == "__main__":
    # Demo: Show available templates
    print("Available Script Templates:")
    print("=" * 60)

    for template_name in list_templates():
        info = get_template_info(template_name)
        print(f"\n{template_name.upper()}")
        print(f"  Segments: {info['total_segments']}")
        print(f"  Duration: ~{info['estimated_duration']} seconds")
        print(f"  Structure: {', '.join(info['segment_names'])}")
