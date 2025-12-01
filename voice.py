"""
Wagner Nascimento Voice - Prompts and Persona
The Unconnected Society / Predator Protocol Voice
"""

# Archive citation counter (increments per chapter)
_archive_counter = 100

def get_archive_citation(topic: str) -> str:
    """Generate Wagner-style archive citation."""
    global _archive_counter
    _archive_counter += 1
    return f"— Archive: UNCONNECTED SOCIETY / Blueprint {_archive_counter:03d}"

# Core Wagner Persona
WAGNER_SYSTEM_PROMPT = """You are Wagner Nascimento, founder of The Unconnected Society.

YOUR VOICE:
- Anti-Matrix philosophy: Modern society is a prison designed to keep humans weak, dependent, and asleep
- You speak with authority, like a mentor who has seen through the lies
- Use Matrix metaphors: "red pill", "unplugging", "seeing through the code"
- Reference "The Predator Protocol" - your nutrition/lifestyle system
- Zero tolerance for excuses, victimhood, or weakness
- Discipline over motivation - motivation is for amateurs
- Dark, aggressive, but ultimately empowering tone

KEY CONCEPTS YOU REFERENCE:
- The Unconnected Society: Your community of awakened individuals
- Predator Protocol: Zero essential carbohydrates, animal-based nutrition
- War Mode: State of peak mental and physical performance
- The Matrix: Modern society's systems of control (processed food, social media, comfort)
- Blueprint Archives: Your knowledge base, cited as "— Archive: UNCONNECTED SOCIETY / Blueprint XXX"

WRITING STYLE:
- Short, punchy paragraphs
- Rhetorical questions that challenge the reader
- Bold statements that provoke thought
- Scientific backing when discussing nutrition/health
- Personal anecdotes of transformation
- End sections with archive citations

FORBIDDEN:
- Never be soft or apologetic
- Never suggest "balance" or "moderation" (these are Matrix concepts)
- Never use corporate wellness language
- Never validate weakness or excuses"""

RESEARCH_PROMPT = """Research the following topic thoroughly. Gather:
1. Scientific studies and data
2. Historical context
3. Common misconceptions (Matrix lies)
4. Counter-narrative truths
5. Practical applications

Topic: {topic}

Return structured research findings that can be transformed into Wagner Nascimento's anti-Matrix content."""

OUTLINE_PROMPT = """Create a {num_chapters}-chapter ebook outline for: "{topic}"

Each chapter must:
1. Have a provocative, Matrix-breaking title
2. Challenge conventional wisdom
3. Build toward transformation
4. Include practical "War Mode" actions

Format your response as JSON:
{{
    "title_en": "Main title in English",
    "title_pt": "Main title in Portuguese",
    "description_en": "2-3 sentence hook in English",
    "description_pt": "2-3 sentence hook in Portuguese",
    "chapters": [
        {{
            "number": 1,
            "title_en": "Chapter title EN",
            "title_pt": "Chapter title PT",
            "summary_en": "Brief summary EN",
            "summary_pt": "Brief summary PT",
            "key_points": ["point1", "point2", "point3"]
        }}
    ]
}}"""

CHAPTER_PROMPT = """Write Chapter {chapter_number}: "{chapter_title}"

CONTEXT:
- Ebook topic: {ebook_topic}
- Chapter summary: {chapter_summary}
- Key points to cover: {key_points}
- Research data: {research_data}

REQUIREMENTS:
1. Write in Wagner Nascimento's voice (anti-Matrix, Predator Protocol)
2. 1500-2500 words
3. Include at least one archive citation
4. End with a "War Mode Action" - practical step the reader must take
5. Use HTML formatting (<h2>, <p>, <strong>, <ul>, <li>)

Write the chapter content now. Be aggressive. Be transformative. Wake them up."""

CHAPTER_TRANSLATE_PROMPT = """Translate this chapter to Brazilian Portuguese, maintaining Wagner Nascimento's aggressive, anti-Matrix voice.

Keep:
- The provocative tone
- Matrix metaphors (adapt culturally if needed)
- Archive citations
- HTML formatting

Original content:
{content}"""

IMAGE_PROMPT_TEMPLATE = """Create a dark, cinematic image for an ebook chapter.

Theme: {chapter_theme}
Style requirements:
- Dark mode aesthetic (deep blacks, dramatic lighting)
- Cinematic quality, movie poster feel
- Masculine, aggressive energy
- Abstract or symbolic (no text, no faces)
- Colors: Deep reds, blacks, dark oranges
- Mood: Powerful, transformative, awakening

The image should evoke the feeling of breaking free from mental chains."""

EXTRACT_AND_CLASSIFY_PROMPT = """Extract and structure this ebook PDF content into blocks.

PDF CONTENT:
{pdf_content}

Return JSON with this structure:
{{
  "title": "Book title",
  "subtitle": "Book subtitle (or empty string)",
  "description": "2-3 sentence description based on the introduction",
  "summary": "Brief overall summary of the book",
  "cover_image_prompt": "Detailed prompt for dark, cinematic book cover image",
  "chapters": [
    {{
      "number": 1,
      "title": "Chapter title",
      "summary": "Brief chapter summary (2-3 sentences)",
      "image_prompt": "Detailed prompt for dark, cinematic chapter image",
      "blocks": [
        {{"type": "heading", "level": 2, "text": "Section Title"}},
        {{"type": "paragraph", "text": "Content paragraph..."}},
        {{"type": "list", "ordered": false, "items": ["item 1", "item 2"]}},
        {{"type": "table", "headers": ["Col1", "Col2"], "rows": [["a", "b"]]}},
        {{"type": "callout", "style": "tip", "title": "Pro Tip", "content": "Important info..."}},
        {{"type": "quote", "text": "Quote text", "author": "Author name"}}
      ]
    }}
  ]
}}

BLOCK TYPES (choose the most appropriate for each content section):
- paragraph: {{type, text}} - Regular text paragraphs
- heading: {{type, level (2-4), text}} - Section headers
- list: {{type, ordered (bool), items: [strings]}} - Bullet or numbered lists
- table: {{type, headers: [...], rows: [[...]]}} - Tabular data with rows/columns
- callout: {{type, style (info/warning/tip/note), title, content}} - Important highlighted info
- accordion: {{type, items: [{{title, content}}]}} - Expandable sections (for FAQs, related items)
- tabs: {{type, tabs: [{{label, content}}]}} - Alternative views of same topic
- code: {{type, language, filename (optional), code}} - Code snippets
- quote: {{type, text, author}} - Attributed quotes

RULES:
1. PRESERVE ALL CONTENT exactly - do not summarize or cut anything
2. Choose appropriate block types based on content meaning:
   - Use callouts for important notes, warnings, tips, key takeaways
   - Use tables for structured data with clear rows and columns
   - Use accordion for FAQ-style content or multiple related expandable items
   - Use lists for bullet points or numbered steps
   - Use quote for attributed quotes
3. Include Introduction and Conclusion as chapters
4. Image prompts must be: dark cinematic, abstract/symbolic, NO text/faces/humans, deep reds/blacks/oranges

Return ONLY valid JSON, no additional text."""

PDF_IMAGE_PROMPTS_PROMPT = """Generate image prompts for this ebook.

EBOOK TITLE: {title}
CHAPTERS:
{chapters}

Generate a JSON object with image prompts for the cover and each chapter.

Return JSON in this exact format:
{{
    "cover_image_prompt": "Detailed prompt for dark, cinematic book cover",
    "chapter_prompts": [
        "Detailed prompt for chapter 1 image",
        "Detailed prompt for chapter 2 image"
    ]
}}

IMAGE PROMPT REQUIREMENTS:
- Dark mode aesthetic (deep blacks, dramatic lighting)
- Cinematic quality, movie poster feel
- Abstract or symbolic (NO text, NO faces, NO human figures)
- Colors: Deep reds, blacks, dark oranges, electric blues
- Mood: Powerful, transformative, masculine energy
- Each prompt should capture the essence of that chapter's theme

Return ONLY valid JSON."""

PDF_IMAGE_PROMPT = """Create a cinematic image prompt for this ebook chapter.

CHAPTER: {chapter_title}
SUMMARY: {chapter_summary}

Generate a detailed prompt for an AI image generator. The image must be:
- Dark mode aesthetic (deep blacks, dramatic lighting, cinematic shadows)
- Abstract or symbolic representation of the chapter theme
- NO text, NO faces, NO human figures
- Colors: Deep reds, blacks, dark oranges, occasional electric blue accents
- Mood: Powerful, transformative, masculine energy
- Style: Movie poster quality, epic scale

Return ONLY the image prompt, nothing else."""


def get_research_prompt(topic: str) -> str:
    """Get the research phase prompt."""
    return RESEARCH_PROMPT.format(topic=topic)

def get_outline_prompt(topic: str, num_chapters: int = 5) -> str:
    """Get the outline generation prompt."""
    return OUTLINE_PROMPT.format(topic=topic, num_chapters=num_chapters)

def get_chapter_prompt(
    chapter_number: int,
    chapter_title: str,
    ebook_topic: str,
    chapter_summary: str,
    key_points: list[str],
    research_data: str
) -> str:
    """Get the chapter writing prompt."""
    return CHAPTER_PROMPT.format(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        ebook_topic=ebook_topic,
        chapter_summary=chapter_summary,
        key_points=", ".join(key_points),
        research_data=research_data
    )

def get_translation_prompt(content: str) -> str:
    """Get the translation prompt."""
    return CHAPTER_TRANSLATE_PROMPT.format(content=content)

def get_image_prompt(chapter_theme: str) -> str:
    """Get the image generation prompt."""
    return IMAGE_PROMPT_TEMPLATE.format(chapter_theme=chapter_theme)


def get_extract_and_classify_prompt(pdf_content: str) -> str:
    """Get the PDF extraction and block classification prompt."""
    return EXTRACT_AND_CLASSIFY_PROMPT.format(pdf_content=pdf_content)


def get_pdf_image_prompts_prompt(title: str, chapters: list[dict]) -> str:
    """Get prompt for generating all image prompts at once."""
    chapters_text = "\n".join(
        f"{ch['number']}. {ch['title']}: {ch.get('summary', '')}"
        for ch in chapters
    )
    return PDF_IMAGE_PROMPTS_PROMPT.format(title=title, chapters=chapters_text)


def get_pdf_image_prompt(chapter_title: str, chapter_summary: str) -> str:
    """Get image prompt for a PDF-extracted chapter."""
    return PDF_IMAGE_PROMPT.format(
        chapter_title=chapter_title,
        chapter_summary=chapter_summary
    )
