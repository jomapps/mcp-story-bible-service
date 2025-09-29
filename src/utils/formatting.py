"""Data formatting helpers for exports."""

import json
from typing import Any, Dict, List


def render_markdown(story_bible: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"# {story_bible.get('title', 'Untitled Story')}")
    lines.append("")
    lines.append(f"**Genre:** {story_bible.get('genre', 'Unknown')}")
    if story_bible.get("premise"):
        lines.append(f"**Premise:** {story_bible.get('premise')}")
    if story_bible.get("logline"):
        lines.append(f"**Logline:** {story_bible.get('logline')}")

    themes = story_bible.get("themes") or []
    if themes:
        lines.append("## Themes")
        for theme in themes:
            lines.append(f"- {theme}")

    characters = story_bible.get("characters") or []
    if characters:
        lines.append("## Characters")
        for character in characters:
            lines.append(f"### {character.get('name', 'Unnamed Character')}")
            lines.append(f"Role: {character.get('role', 'unknown')}")
            if character.get("background"):
                lines.append(f"Background: {character['background']}")
            if character.get("motivation"):
                lines.append(f"Motivation: {character['motivation']}")
            lines.append("")

    scenes = story_bible.get("scenes") or []
    if scenes:
        lines.append("## Scenes")
        for scene in sorted(scenes, key=lambda s: s.get("sequence_number", 0)):
            lines.append(
                f"### {scene.get('sequence_number', '?')}. {scene.get('title', 'Untitled Scene')}"
            )
            lines.append(f"Location: {scene.get('location', 'Unknown')} - {scene.get('time_of_day', 'Unknown')}")
            if scene.get("scene_purpose"):
                lines.append(f"Purpose: {scene['scene_purpose']}")
            if scene.get("description"):
                lines.append(scene["description"])
            lines.append("")

    plot_threads = story_bible.get("plot_threads") or []
    if plot_threads:
        lines.append("## Plot Threads")
        for thread in plot_threads:
            lines.append(f"### {thread.get('thread_name', 'Unnamed Thread')}")
            lines.append(f"Type: {thread.get('thread_type', 'unknown')}")
            if thread.get("description"):
                lines.append(thread["description"])
            lines.append("")

    return "\n".join(lines)


def render_json(story_bible: Dict[str, Any]) -> str:
    return json.dumps(story_bible, indent=2, sort_keys=True, default=str)
