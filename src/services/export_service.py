"""Export helpers for story bible content."""

from typing import Any, Dict, List, Optional

from ..utils.formatting import render_json, render_markdown


class ExportService:
    def generate(
        self,
        story_bible: Dict[str, Any],
        *,
        export_format: str,
        sections: Optional[List[str]] = None,
    ) -> bytes:
        payload = self._filter_sections(story_bible, sections)
        fmt = export_format.lower()
        if fmt == "json":
            return render_json(payload).encode("utf-8")
        markdown = render_markdown(payload)
        if fmt == "markdown":
            return markdown.encode("utf-8")
        if fmt == "pdf":
            return markdown.encode("utf-8")
        if fmt == "docx":
            return markdown.encode("utf-8")
        raise ValueError(f"Unsupported export format: {export_format}")

    def _filter_sections(
        self,
        story_bible: Dict[str, Any],
        sections: Optional[List[str]],
    ) -> Dict[str, Any]:
        if not sections:
            return story_bible
        allowed = set(section.lower() for section in sections)
        filtered: Dict[str, Any] = {}
        for key, value in story_bible.items():
            if key.lower() in allowed:
                filtered[key] = value
        return filtered
