"""
Deterministic HTML Builder for Ebook Content Blocks.
Converts structured block data from LLM into consistent HTML.
"""

import html
from typing import Any


def escape(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(str(text)) if text else ""


def build_paragraph(block: dict) -> str:
    """Build a paragraph block."""
    return f'<p>{escape(block["text"])}</p>'


def build_heading(block: dict) -> str:
    """Build a heading block (h2, h3, h4)."""
    level = block.get("level", 2)
    level = max(2, min(4, level))  # Clamp to 2-4
    return f'<h{level}>{escape(block["text"])}</h{level}>'


def build_list(block: dict) -> str:
    """Build an ordered or unordered list."""
    ordered = block.get("ordered", False)
    tag = "ol" if ordered else "ul"
    items = block.get("items", [])

    items_html = "\n".join(f'        <li>{escape(item)}</li>' for item in items)
    return f'''<{tag} class="my-4 pl-6 space-y-2">
{items_html}
    </{tag}>'''


def build_table(block: dict) -> str:
    """Build a styled table."""
    headers = block.get("headers", [])
    rows = block.get("rows", [])

    header_cells = "\n".join(
        f'          <th class="border border-neutral-700 px-4 py-2 text-left">{escape(h)}</th>'
        for h in headers
    )

    body_rows = []
    for row in rows:
        cells = "\n".join(
            f'          <td class="border border-neutral-700 px-4 py-2">{escape(cell)}</td>'
            for cell in row
        )
        body_rows.append(f'        <tr>\n{cells}\n        </tr>')

    return f'''<div class="my-6 overflow-x-auto">
    <table class="w-full border-collapse border border-neutral-700 text-sm">
      <thead class="bg-neutral-800">
        <tr>
{header_cells}
        </tr>
      </thead>
      <tbody>
{chr(10).join(body_rows)}
      </tbody>
    </table>
  </div>'''


def build_callout(block: dict) -> str:
    """Build a callout box (info, warning, tip, note)."""
    style = block.get("style", "info")
    title = block.get("title", "")
    content = block.get("content", "")

    # Style configurations
    styles = {
        "info": {"border": "border-blue-500", "bg": "bg-blue-500/10", "icon": "&#8505;&#65039;"},
        "warning": {"border": "border-yellow-500", "bg": "bg-yellow-500/10", "icon": "&#9888;&#65039;"},
        "tip": {"border": "border-green-500", "bg": "bg-green-500/10", "icon": "&#128161;"},
        "note": {"border": "border-purple-500", "bg": "bg-purple-500/10", "icon": "&#128221;"},
    }

    cfg = styles.get(style, styles["info"])

    return f'''<div data-block="callout" data-callout-type="{style}" class="my-6 p-4 rounded-lg border-l-4 {cfg["border"]} {cfg["bg"]}">
    <div class="flex gap-3">
      <span class="text-xl">{cfg["icon"]}</span>
      <div>
        <strong class="block mb-1">{escape(title)}</strong>
        <p class="text-gray-300 m-0">{escape(content)}</p>
      </div>
    </div>
  </div>'''


def build_accordion(block: dict) -> str:
    """Build an accordion with expandable items."""
    items = block.get("items", [])

    items_html = []
    for i, item in enumerate(items):
        title = escape(item.get("title", ""))
        content = escape(item.get("content", ""))
        items_html.append(f'''    <div data-accordion-item="{i}" class="border border-neutral-700 rounded-lg mb-2 overflow-hidden">
      <div data-accordion-trigger class="px-4 py-3 bg-neutral-800 font-medium cursor-pointer hover:bg-neutral-700 flex justify-between items-center">
        <span>{title}</span>
        <span>&#9660;</span>
      </div>
      <div data-accordion-content class="px-4 py-3 border-t border-neutral-700">
        {content}
      </div>
    </div>''')

    return f'''<div data-block="accordion" class="my-6">
{chr(10).join(items_html)}
  </div>'''


def build_tabs(block: dict) -> str:
    """Build a tabbed interface."""
    tabs = block.get("tabs", [])

    # Tab buttons
    buttons = []
    for i, tab in enumerate(tabs):
        label = escape(tab.get("label", f"Tab {i+1}"))
        active_class = "border-orange-500 text-orange-500" if i == 0 else "border-transparent text-gray-400"
        buttons.append(f'      <button data-tab-button="{i}" class="px-4 py-2 border-b-2 {active_class}">{label}</button>')

    # Tab content
    contents = []
    for i, tab in enumerate(tabs):
        content = escape(tab.get("content", ""))
        hidden = "" if i == 0 else "hidden "
        contents.append(f'      <div data-tab-content="{i}" class="{hidden}p-4">{content}</div>')

    return f'''<div data-block="tabs" class="my-6 border border-neutral-700 rounded-lg overflow-hidden">
    <div class="flex border-b border-neutral-700 bg-neutral-800">
{chr(10).join(buttons)}
    </div>
    <div>
{chr(10).join(contents)}
    </div>
  </div>'''


def build_code(block: dict) -> str:
    """Build a code block with syntax highlighting placeholder."""
    language = block.get("language", "")
    filename = block.get("filename", "")
    code = escape(block.get("code", ""))

    header = ""
    if filename:
        header = f'''    <div class="px-4 py-2 bg-neutral-800 border-b border-neutral-700 text-xs text-gray-400 font-mono">{escape(filename)}</div>
'''

    return f'''<div data-block="code" data-language="{language}" data-filename="{escape(filename)}" class="my-6 rounded-lg overflow-hidden bg-neutral-900 border border-neutral-700">
{header}    <pre class="p-4 overflow-x-auto m-0"><code class="text-sm font-mono text-gray-200">{code}</code></pre>
  </div>'''


def build_quote(block: dict) -> str:
    """Build a styled blockquote."""
    text = escape(block.get("text", ""))
    author = escape(block.get("author", ""))

    author_html = f'\n    <footer class="mt-3 text-sm text-gray-400">— {author}</footer>' if author else ""

    return f'''<blockquote data-block="quote" data-author="{author}" class="my-8 pl-6 border-l-4 border-orange-500 bg-neutral-800/50 py-4 pr-4 rounded-r-lg">
    <p class="text-lg italic text-gray-200 m-0">"{text}"</p>{author_html}
  </blockquote>'''


def build_video(block: dict) -> str:
    """Build a video embed (YouTube/Vimeo)."""
    url = block.get("url", "")
    caption = escape(block.get("caption", ""))

    # Extract video ID and determine type
    video_type = "youtube"
    embed_url = url

    if "youtube.com" in url or "youtu.be" in url:
        video_type = "youtube"
        # Extract video ID
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
        elif "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
        else:
            video_id = url
        embed_url = f"https://www.youtube.com/embed/{video_id}"
    elif "vimeo.com" in url:
        video_type = "vimeo"
        video_id = url.split("/")[-1].split("?")[0]
        embed_url = f"https://player.vimeo.com/video/{video_id}"

    caption_html = f'\n    <p class="mt-2 text-center text-sm text-gray-400">{caption}</p>' if caption else ""

    return f'''<div data-block="video" data-video-type="{video_type}" class="my-8">
    <div class="relative aspect-video rounded-lg overflow-hidden bg-neutral-800">
      <iframe src="{embed_url}" title="Video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen class="absolute inset-0 w-full h-full"></iframe>
    </div>{caption_html}
  </div>'''


# Block type to builder function mapping
BLOCK_BUILDERS = {
    "paragraph": build_paragraph,
    "heading": build_heading,
    "list": build_list,
    "table": build_table,
    "callout": build_callout,
    "accordion": build_accordion,
    "tabs": build_tabs,
    "code": build_code,
    "quote": build_quote,
    "video": build_video,
}


def build_html(blocks: list[dict]) -> str:
    """
    Convert a list of content blocks to HTML string.

    Args:
        blocks: List of block dictionaries with 'type' and type-specific fields

    Returns:
        HTML string with all blocks rendered
    """
    html_parts = []

    for block in blocks:
        block_type = block.get("type", "paragraph")
        builder = BLOCK_BUILDERS.get(block_type)

        if builder:
            try:
                html_parts.append(builder(block))
            except Exception as e:
                # Fallback: render as paragraph if block fails
                text = block.get("text", block.get("content", str(block)))
                html_parts.append(f'<p>{escape(text)}</p>')
        else:
            # Unknown block type: render as paragraph
            text = block.get("text", block.get("content", str(block)))
            html_parts.append(f'<p>{escape(text)}</p>')

    return "\n\n".join(html_parts)
