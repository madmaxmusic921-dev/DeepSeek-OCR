"""
Video Script Generator Module

Converts Reddit post data into video-ready scripts with timing,
narration, visual cues, and subtitle support.

Example:
    generator = ScriptGenerator()
    script = generator.generate_script(post_data, format_type="medium")
    generator.export_script(script, "output.json")
"""

import json
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

try:
    from script_config import (
        VIDEO_FORMATS,
        SCRIPT_OPTIONS,
        SEGMENT_TIMING,
        COMMENT_SELECTION,
        NARRATION_TEMPLATES,
        EXPORT_FORMATS,
    )
    from script_templates import get_template, get_narration_style, list_templates
except ImportError:
    print("Warning: Configuration files not found. Using defaults.")
    VIDEO_FORMATS = {}
    SCRIPT_OPTIONS = {}
    SEGMENT_TIMING = {}
    COMMENT_SELECTION = {}
    NARRATION_TEMPLATES = {}
    EXPORT_FORMATS = {}


class ScriptGeneratorError(Exception):
    """Base exception for script generator errors"""
    pass


class InvalidFormatError(ScriptGeneratorError):
    """Raised when an invalid format is specified"""
    pass


class InvalidPostDataError(ScriptGeneratorError):
    """Raised when post data is invalid or missing required fields"""
    pass


class ScriptGenerator:
    """
    Generate video scripts from Reddit post data.

    Attributes:
        options: Dictionary of script generation options
        templates: Available script templates
    """

    def __init__(self, options: Optional[Dict] = None):
        """
        Initialize the Script Generator.

        Args:
            options: Custom script generation options
        """
        self.options = {**SCRIPT_OPTIONS, **(options or {})}
        self.words_per_minute = self.options.get("words_per_minute", 150)

    def generate_script(
        self,
        post_data: Dict[str, Any],
        format_type: str = "medium",
        template_name: Optional[str] = None,
        narration_style: str = "casual",
    ) -> Dict[str, Any]:
        """
        Generate a video script from Reddit post data.

        Args:
            post_data: Reddit post data from RedditFetcher
            format_type: Video format (short/medium/long)
            template_name: Optional custom template name
            narration_style: Narration style (casual/formal/dramatic/comedic)

        Returns:
            Dictionary containing complete script with timing and narration

        Raises:
            InvalidPostDataError: If post data is invalid
            InvalidFormatError: If format type is invalid
        """
        # Validate post data
        self._validate_post_data(post_data)

        # Get template
        if template_name is None:
            template_name = format_type
        template = get_template(template_name)

        # Initialize script structure
        script = {
            "metadata": self._generate_metadata(post_data, format_type, template_name),
            "segments": [],
            "total_duration": 0,
            "word_count": 0,
            "narration_style": narration_style,
        }

        # Generate segments
        cumulative_time = 0
        for segment_template in template.segments:
            segment = self._generate_segment(
                segment_template,
                post_data,
                cumulative_time,
                format_type,
                narration_style,
            )
            if segment:  # Only add if segment has content
                script["segments"].append(segment)
                cumulative_time = segment["end_time"]

        # Update totals
        script["total_duration"] = cumulative_time
        script["word_count"] = sum(
            self._count_words(seg["narration"]) for seg in script["segments"]
        )

        return script

    def _validate_post_data(self, post_data: Dict[str, Any]) -> None:
        """Validate that post data has required fields"""
        required_fields = ["title", "body", "subreddit", "author"]
        missing = [field for field in required_fields if field not in post_data]
        if missing:
            raise InvalidPostDataError(
                f"Post data missing required fields: {', '.join(missing)}"
            )

    def _generate_metadata(
        self, post_data: Dict[str, Any], format_type: str, template_name: str
    ) -> Dict[str, Any]:
        """Generate script metadata"""
        return {
            "post_id": post_data.get("id", "unknown"),
            "title": post_data["title"],
            "subreddit": post_data["subreddit"],
            "author": post_data["author"],
            "post_url": post_data.get("url", ""),
            "format_type": format_type,
            "template": template_name,
            "generated_at": datetime.now().isoformat(),
            "post_score": post_data.get("score", 0),
            "num_comments": post_data.get("num_comments", 0),
        }

    def _generate_segment(
        self,
        segment_template: Dict[str, Any],
        post_data: Dict[str, Any],
        start_time: float,
        format_type: str,
        narration_style: str,
    ) -> Optional[Dict[str, Any]]:
        """Generate a single script segment"""
        segment_name = segment_template["name"]
        content_type = segment_template["content_type"]

        # Generate narration based on content type
        narration = self._generate_narration(
            content_type, post_data, format_type, narration_style, segment_name
        )

        if not narration and not segment_template.get("required"):
            return None  # Skip optional empty segments

        # Calculate duration
        duration = self._calculate_duration(narration, segment_template["duration"])

        # Generate visual cues
        visual_cues = self._generate_visual_cues(
            segment_template["visual"], content_type, post_data
        )

        segment = {
            "name": segment_name,
            "type": content_type,
            "start_time": start_time,
            "end_time": start_time + duration,
            "duration": duration,
            "narration": narration,
            "visual": visual_cues,
            "required": segment_template.get("required", True),
        }

        return segment

    def _generate_narration(
        self,
        content_type: str,
        post_data: Dict[str, Any],
        format_type: str,
        narration_style: str,
        segment_name: str,
    ) -> str:
        """Generate narration text for a segment"""
        if content_type == "intro":
            return self._generate_intro_narration(post_data, narration_style)
        elif content_type == "title":
            return self._generate_title_narration(post_data, narration_style)
        elif content_type == "metadata" or content_type == "context":
            return self._generate_context_narration(post_data, format_type)
        elif content_type == "post_body":
            return self._generate_body_narration(post_data, format_type)
        elif content_type == "comments":
            return self._generate_comments_narration(post_data, format_type)
        elif content_type == "engagement":
            return self._generate_engagement_narration(narration_style)
        elif content_type in ["call_to_action", "outro"]:
            return self._generate_outro_narration(narration_style)
        elif content_type == "teaser":
            return self._generate_teaser_narration(post_data, narration_style)
        else:
            return ""

    def _generate_intro_narration(
        self, post_data: Dict[str, Any], style: str
    ) -> str:
        """Generate intro narration"""
        templates = NARRATION_TEMPLATES.get("intro", {}).get(style, [])
        if not templates:
            templates = ["Here's an interesting post from r/{subreddit}"]

        template = random.choice(templates)
        return template.format(subreddit=post_data["subreddit"])

    def _generate_title_narration(
        self, post_data: Dict[str, Any], style: str
    ) -> str:
        """Generate title narration"""
        title = post_data["title"]
        # Add style-specific prefix if needed
        if style == "dramatic":
            return f"Listen to this: {title}"
        elif style == "comedic":
            return f"Get this: {title}"
        else:
            return title

    def _generate_context_narration(
        self, post_data: Dict[str, Any], format_type: str
    ) -> str:
        """Generate context/metadata narration"""
        context_parts = []

        if self.options.get("show_usernames", True):
            context_parts.append(f"Posted by u/{post_data['author']}")

        if self.options.get("show_scores", True) and post_data.get("score"):
            score = post_data["score"]
            context_parts.append(f"with {score:,} upvotes")

        if format_type == "long" and post_data.get("awards"):
            award_count = len(post_data["awards"])
            if award_count > 0:
                context_parts.append(f"and {award_count} awards")

        return ". ".join(context_parts) + "." if context_parts else ""

    def _generate_body_narration(
        self, post_data: Dict[str, Any], format_type: str
    ) -> str:
        """Generate body content narration"""
        body = post_data.get("body", "")
        if not body:
            return ""

        # Truncate based on format
        if format_type == "short":
            max_words = 50
        elif format_type == "medium":
            max_words = 150
        else:
            max_words = 500

        words = body.split()
        if len(words) > max_words:
            body = " ".join(words[:max_words]) + "..."

        return body

    def _generate_comments_narration(
        self, post_data: Dict[str, Any], format_type: str
    ) -> str:
        """Generate comments narration"""
        comments = post_data.get("comments", [])
        if not comments:
            return ""

        # Get comment selection criteria
        criteria = COMMENT_SELECTION.get(
            format_type, {"max_comments": 3, "min_score": 10}
        )

        # Filter and select comments
        selected = []
        for comment in comments:
            if len(selected) >= criteria["max_comments"]:
                break
            if comment.get("score", 0) >= criteria.get("min_score", 0):
                selected.append(comment)

        # Generate narration
        if not selected:
            return ""

        narration_parts = []

        # Add transition
        transitions = NARRATION_TEMPLATES.get("transition", {}).get("to_comments", [])
        if transitions:
            narration_parts.append(random.choice(transitions))

        # Add comments
        for i, comment in enumerate(selected, 1):
            author = comment.get("author", "someone")
            body = comment.get("body", "")
            score = comment.get("score", 0)

            # Truncate long comments
            max_length = 200 if format_type == "long" else 100
            if len(body) > max_length:
                body = body[:max_length] + "..."

            if self.options.get("show_usernames", True):
                comment_text = f"u/{author} said: {body}"
            else:
                comment_text = f"One person said: {body}"

            if self.options.get("show_scores", True) and score > 50:
                comment_text += f". This got {score} upvotes"

            narration_parts.append(comment_text)

        return ". ".join(narration_parts) + "."

    def _generate_engagement_narration(self, style: str) -> str:
        """Generate engagement prompt narration"""
        prompts = NARRATION_TEMPLATES.get("engagement", [])
        if not prompts:
            prompts = ["What do you think?", "Let me know in the comments"]
        return random.choice(prompts)

    def _generate_outro_narration(self, style: str) -> str:
        """Generate outro narration"""
        outros = NARRATION_TEMPLATES.get("outro", [])
        if not outros:
            outros = ["Thanks for watching!"]
        return random.choice(outros)

    def _generate_teaser_narration(
        self, post_data: Dict[str, Any], style: str
    ) -> str:
        """Generate teaser/hook narration"""
        title = post_data["title"]
        # Extract the most interesting part of the title
        if ":" in title:
            teaser = title.split(":")[0]
        else:
            words = title.split()
            teaser = " ".join(words[: min(10, len(words))])

        if style == "dramatic":
            return f"You need to hear this story about {teaser}"
        else:
            return teaser

    def _calculate_duration(self, text: str, base_duration: float) -> float:
        """Calculate segment duration based on narration length"""
        if not text:
            return base_duration

        word_count = self._count_words(text)
        calculated_duration = (word_count / self.words_per_minute) * 60

        # Add pause time
        pause_time = self.options.get("pause_duration", 0.5)
        calculated_duration += pause_time

        # Use the longer of base_duration or calculated_duration
        return max(base_duration, calculated_duration)

    def _count_words(self, text: str) -> int:
        """Count words in text"""
        return len(text.split()) if text else 0

    def _generate_visual_cues(
        self, visual_type: str, content_type: str, post_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate visual cue specifications"""
        visual = {
            "type": visual_type,
            "elements": [],
        }

        if visual_type == "title_screen":
            visual["elements"] = [
                {"type": "text", "content": post_data["title"], "position": "center"},
                {
                    "type": "label",
                    "content": f"r/{post_data['subreddit']}",
                    "position": "top",
                },
            ]
        elif visual_type == "text_overlay":
            visual["elements"] = [
                {"type": "text", "content": post_data.get("body", ""), "scroll": True}
            ]
        elif visual_type == "comment_section":
            comments = post_data.get("comments", [])[:3]
            for comment in comments:
                visual["elements"].append(
                    {
                        "type": "comment",
                        "author": comment.get("author", ""),
                        "content": comment.get("body", ""),
                        "score": comment.get("score", 0),
                    }
                )
        elif visual_type == "stats_display":
            visual["elements"] = [
                {"type": "stat", "label": "Upvotes", "value": post_data.get("score", 0)},
                {
                    "type": "stat",
                    "label": "Comments",
                    "value": post_data.get("num_comments", 0),
                },
            ]

        return visual

    def export_script(
        self, script: Dict[str, Any], output_path: str, format: str = "json"
    ) -> None:
        """
        Export script to file.

        Args:
            script: Generated script dictionary
            output_path: Path to save file
            format: Export format (json, txt, srt, vtt)
        """
        output_path = Path(output_path)

        if format == "json":
            self._export_json(script, output_path)
        elif format == "txt":
            self._export_txt(script, output_path)
        elif format == "srt":
            self._export_srt(script, output_path)
        elif format == "vtt":
            self._export_vtt(script, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def _export_json(self, script: Dict[str, Any], output_path: Path) -> None:
        """Export script as JSON"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        print(f"Script exported to: {output_path}")

    def _export_txt(self, script: Dict[str, Any], output_path: Path) -> None:
        """Export script as plain text"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("VIDEO SCRIPT\n")
            f.write("=" * 60 + "\n\n")

            # Metadata
            f.write("METADATA:\n")
            for key, value in script["metadata"].items():
                f.write(f"  {key}: {value}\n")

            f.write(f"\nTotal Duration: {script['total_duration']:.1f} seconds\n")
            f.write(f"Word Count: {script['word_count']}\n")
            f.write("\n" + "=" * 60 + "\n\n")

            # Segments
            for i, segment in enumerate(script["segments"], 1):
                f.write(f"SEGMENT {i}: {segment['name'].upper()}\n")
                f.write("-" * 60 + "\n")
                f.write(
                    f"Time: {segment['start_time']:.1f}s - {segment['end_time']:.1f}s "
                    f"({segment['duration']:.1f}s)\n"
                )
                f.write(f"Type: {segment['type']}\n")
                f.write(f"\nNarration:\n{segment['narration']}\n")
                f.write(f"\nVisual: {segment['visual']['type']}\n")
                f.write("\n" + "=" * 60 + "\n\n")

        print(f"Script exported to: {output_path}")

    def _export_srt(self, script: Dict[str, Any], output_path: Path) -> None:
        """Export script as SRT subtitle file"""
        subtitles = self._generate_subtitles(script)

        with open(output_path, "w", encoding="utf-8") as f:
            for i, subtitle in enumerate(subtitles, 1):
                f.write(f"{i}\n")
                f.write(
                    f"{self._format_srt_time(subtitle['start'])} --> "
                    f"{self._format_srt_time(subtitle['end'])}\n"
                )
                f.write(f"{subtitle['text']}\n\n")

        print(f"Subtitles exported to: {output_path}")

    def _export_vtt(self, script: Dict[str, Any], output_path: Path) -> None:
        """Export script as WebVTT subtitle file"""
        subtitles = self._generate_subtitles(script)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for subtitle in subtitles:
                f.write(
                    f"{self._format_vtt_time(subtitle['start'])} --> "
                    f"{self._format_vtt_time(subtitle['end'])}\n"
                )
                f.write(f"{subtitle['text']}\n\n")

        print(f"Subtitles exported to: {output_path}")

    def _generate_subtitles(
        self, script: Dict[str, Any], max_chars_per_line: int = 42
    ) -> List[Dict[str, Any]]:
        """Generate subtitle entries from script"""
        subtitles = []

        for segment in script["segments"]:
            narration = segment["narration"]
            if not narration:
                continue

            # Split narration into sentences
            sentences = re.split(r"[.!?]+", narration)
            sentences = [s.strip() for s in sentences if s.strip()]

            # Calculate time per sentence
            segment_duration = segment["duration"]
            time_per_sentence = segment_duration / len(sentences) if sentences else 0

            current_time = segment["start_time"]

            for sentence in sentences:
                # Split long sentences into multiple lines
                if len(sentence) > max_chars_per_line:
                    words = sentence.split()
                    lines = []
                    current_line = []
                    current_length = 0

                    for word in words:
                        if current_length + len(word) + 1 > max_chars_per_line:
                            lines.append(" ".join(current_line))
                            current_line = [word]
                            current_length = len(word)
                        else:
                            current_line.append(word)
                            current_length += len(word) + 1

                    if current_line:
                        lines.append(" ".join(current_line))

                    sentence = "\n".join(lines)

                subtitles.append(
                    {
                        "start": current_time,
                        "end": current_time + time_per_sentence,
                        "text": sentence,
                    }
                )

                current_time += time_per_sentence

        return subtitles

    def _format_srt_time(self, seconds: float) -> str:
        """Format time for SRT format (HH:MM:SS,mmm)"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _format_vtt_time(self, seconds: float) -> str:
        """Format time for WebVTT format (HH:MM:SS.mmm)"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    def get_script_summary(self, script: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the script"""
        summary = f"""
Video Script Summary
{'=' * 60}
Title: {script['metadata']['title']}
Subreddit: r/{script['metadata']['subreddit']}
Format: {script['metadata']['format_type']}

Duration: {script['total_duration']:.1f} seconds ({script['total_duration'] / 60:.1f} minutes)
Word Count: {script['word_count']} words
Segments: {len(script['segments'])}

Segment Breakdown:
"""

        for segment in script["segments"]:
            summary += (
                f"  {segment['name']:15} | "
                f"{segment['start_time']:6.1f}s - {segment['end_time']:6.1f}s | "
                f"{segment['duration']:5.1f}s\n"
            )

        return summary


# Convenience function
def generate_script(
    post_data: Dict[str, Any], format_type: str = "medium", **kwargs
) -> Dict[str, Any]:
    """
    Quick function to generate a script.

    Args:
        post_data: Reddit post data
        format_type: Video format type
        **kwargs: Additional options for ScriptGenerator

    Returns:
        Generated script dictionary
    """
    generator = ScriptGenerator()
    return generator.generate_script(post_data, format_type, **kwargs)


if __name__ == "__main__":
    print("Video Script Generator Module")
    print("=" * 60)
    print("\nAvailable formats:", ", ".join(list_templates()))
    print("\nThis module converts Reddit post data into video scripts.")
    print("See examples/script_generator_example.py for usage examples.")