"""
E-Book Generator - AI Pipeline
Uses OpenRouter API for Perplexity (research), Claude (content), Gemini (images)
Supports both topic-based generation and PDF import.
"""

import asyncio
import base64
import json
import re
from pathlib import Path
from typing import Any

import httpx

from voice import (
    WAGNER_SYSTEM_PROMPT,
    get_research_prompt,
    get_outline_prompt,
    get_chapter_prompt,
    get_translation_prompt,
    get_image_prompt,
    get_extract_and_classify_prompt,
    get_pdf_image_prompt,
    get_pdf_image_prompts_prompt,
)
from html_builder import build_html

# OpenRouter API configuration
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_IMAGE_URL = "https://openrouter.ai/api/v1/images/generations"

# Model IDs
PERPLEXITY_MODEL = "perplexity/llama-3.1-sonar-huge-128k-online"
CLAUDE_MODEL = "anthropic/claude-sonnet-4-20250514"
GEMINI_IMAGE_MODEL = "google/gemini-2.0-flash-exp:free"


class EbookGenerator:
    """Generates complete ebooks from a single sentence using AI pipeline."""

    def __init__(self, api_key: str, output_dir: Path):
        self.api_key = api_key
        self.output_dir = output_dir
        self.images_dir = output_dir / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)

    async def _call_openrouter(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """Make a request to OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://alphagrit.com",
            "X-Title": "Alpha Grit Ebook Generator",
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _generate_image(self, prompt: str, filename: str) -> str:
        """Generate an image using Gemini via OpenRouter."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Use chat completion with image generation capability
        messages = [
            {"role": "user", "content": f"Generate an image: {prompt}"}
        ]

        payload = {
            "model": GEMINI_IMAGE_MODEL,
            "messages": messages,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                # Check if image data is in response
                content = data["choices"][0]["message"]["content"]

                # For now, save a placeholder and return the path
                # Real implementation would extract base64 image data
                image_path = self.images_dir / filename

                # If content contains base64 image data, decode and save
                if "base64" in str(content).lower() or content.startswith("data:image"):
                    # Extract base64 data
                    match = re.search(r'data:image/\w+;base64,([A-Za-z0-9+/=]+)', content)
                    if match:
                        img_data = base64.b64decode(match.group(1))
                        image_path.write_bytes(img_data)
                        return f"images/{filename}"

                # Fallback: return placeholder path
                return f"images/{filename}"

        except Exception as e:
            print(f"Image generation failed: {e}")
            return f"images/{filename}"

    async def research(self, topic: str) -> str:
        """Phase 1: Research the topic using Perplexity."""
        print(f"Researching: {topic}")
        prompt = get_research_prompt(topic)
        messages = [{"role": "user", "content": prompt}]
        return await self._call_openrouter(PERPLEXITY_MODEL, messages, temperature=0.3)

    async def create_outline(self, topic: str, num_chapters: int) -> dict:
        """Phase 2: Create ebook outline using Claude."""
        print(f"Creating outline with {num_chapters} chapters")
        prompt = get_outline_prompt(topic, num_chapters)
        messages = [
            {"role": "system", "content": WAGNER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        response = await self._call_openrouter(CLAUDE_MODEL, messages, temperature=0.8)

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback structure
            return {
                "title_en": f"The {topic} Protocol",
                "title_pt": f"O Protocolo {topic}",
                "description_en": f"Break free from the Matrix with {topic}.",
                "description_pt": f"Liberte-se da Matrix com {topic}.",
                "chapters": [
                    {
                        "number": i + 1,
                        "title_en": f"Chapter {i + 1}",
                        "title_pt": f"Capitulo {i + 1}",
                        "summary_en": "Summary",
                        "summary_pt": "Resumo",
                        "key_points": ["point1", "point2"],
                    }
                    for i in range(num_chapters)
                ],
            }

    async def write_chapter(
        self,
        chapter_info: dict,
        ebook_topic: str,
        research_data: str,
    ) -> dict:
        """Phase 3: Write a single chapter in both languages."""
        chapter_num = chapter_info["number"]
        print(f"Writing chapter {chapter_num}: {chapter_info['title_en']}")

        # Write English version
        prompt = get_chapter_prompt(
            chapter_number=chapter_num,
            chapter_title=chapter_info["title_en"],
            ebook_topic=ebook_topic,
            chapter_summary=chapter_info["summary_en"],
            key_points=chapter_info.get("key_points", []),
            research_data=research_data,
        )
        messages = [
            {"role": "system", "content": WAGNER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        content_en = await self._call_openrouter(CLAUDE_MODEL, messages, max_tokens=6000)

        # Translate to Portuguese
        print(f"Translating chapter {chapter_num} to Portuguese")
        translate_prompt = get_translation_prompt(content_en)
        messages = [
            {"role": "system", "content": WAGNER_SYSTEM_PROMPT},
            {"role": "user", "content": translate_prompt},
        ]
        content_pt = await self._call_openrouter(CLAUDE_MODEL, messages, max_tokens=6000)

        # Generate chapter image
        print(f"Generating image for chapter {chapter_num}")
        image_prompt = get_image_prompt(chapter_info["title_en"])
        image_filename = f"chapter_{chapter_num}.png"
        image_url = await self._generate_image(image_prompt, image_filename)

        return {
            "chapter_number": chapter_num,
            "title_en": chapter_info["title_en"],
            "title_pt": chapter_info["title_pt"],
            "slug": self._slugify(chapter_info["title_en"]),
            "cover_image_url": image_url,
            "content_en": content_en,
            "content_pt": content_pt,
            "summary_en": chapter_info["summary_en"],
            "summary_pt": chapter_info["summary_pt"],
            "estimated_read_time_minutes": len(content_en.split()) // 200,
            "is_free_preview": chapter_num == 1,
            "is_published": False,
        }

    async def generate_cover(self, title: str) -> str:
        """Generate ebook cover image."""
        print("Generating cover image")
        prompt = get_image_prompt(f"Book cover for '{title}' - epic, transformative, dark cinematic style")
        return await self._generate_image(prompt, "cover.png")

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')

    async def generate(self, topic: str, num_chapters: int = 5) -> dict:
        """
        Generate complete ebook from a single sentence topic.

        Args:
            topic: One sentence describing the ebook topic
            num_chapters: Number of chapters to generate (default 5)

        Returns:
            Complete ebook data matching Supabase schema
        """
        # Phase 1: Research
        research_data = await self.research(topic)

        # Phase 2: Create outline
        outline = await self.create_outline(topic, num_chapters)

        # Phase 3: Generate cover
        cover_url = await self.generate_cover(outline["title_en"])

        # Phase 4: Write all chapters in parallel
        chapter_tasks = [
            self.write_chapter(ch, topic, research_data)
            for ch in outline["chapters"]
        ]
        chapters = await asyncio.gather(*chapter_tasks)

        # Build final ebook structure
        ebook = {
            "ebook": {
                "title_en": outline["title_en"],
                "title_pt": outline["title_pt"],
                "slug": self._slugify(outline["title_en"]),
                "description_en": outline["description_en"],
                "description_pt": outline["description_pt"],
                "cover_image_url": cover_url,
                "price_usd": 1997,  # $19.97 in cents
                "price_brl": 9970,  # R$99.70 in cents
                "status": "draft",
            },
            "chapters": sorted(chapters, key=lambda x: x["chapter_number"]),
        }

        return ebook

    def extract_pdf_content(self, pdf_path: Path) -> str:
        """Extract text content from a PDF file."""
        from pypdf import PdfReader

        print(f"Extracting content from: {pdf_path}")
        reader = PdfReader(pdf_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(f"--- Page {i + 1} ---\n{text}")
        return "\n\n".join(pages)

    async def extract_pdf_content_structured(self, pdf_content: str) -> dict:
        """Use Claude to extract and structure PDF content into blocks."""
        print("Extracting and classifying PDF content with Claude...")
        prompt = get_extract_and_classify_prompt(pdf_content)
        messages = [
            {"role": "user", "content": prompt},
        ]
        # Use higher token limit for large PDFs
        response = await self._call_openrouter(CLAUDE_MODEL, messages, max_tokens=64000, temperature=0.3)

        # Extract JSON from response
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Response preview: {response[:500]}...")
            raise ValueError("Failed to extract PDF content into valid JSON")

    async def generate_chapter_image(self, chapter_info: dict, chapter_num: int) -> str:
        """Generate image for a chapter using its image prompt."""
        print(f"Generating image for chapter {chapter_num}")

        # Use provided image_prompt or generate one
        if "image_prompt" in chapter_info and chapter_info["image_prompt"]:
            image_prompt = chapter_info["image_prompt"]
        else:
            image_prompt = get_pdf_image_prompt(
                chapter_info.get("title_en", f"Chapter {chapter_num}"),
                chapter_info.get("summary_en", "")
            )

        image_filename = f"chapter_{chapter_num}.png"
        return await self._generate_image(image_prompt, image_filename)

    async def generate_image_prompts(self, title: str, chapters: list[dict]) -> dict:
        """Generate image prompts for cover and all chapters."""
        print("Generating image prompts...")
        prompt = get_pdf_image_prompts_prompt(title, chapters)
        messages = [{"role": "user", "content": prompt}]
        response = await self._call_openrouter(CLAUDE_MODEL, messages, max_tokens=4096, temperature=0.7)

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback: generate basic prompts
            return {
                "cover_image_prompt": f"Dark cinematic book cover for '{title}', abstract symbolic imagery, deep blacks and reds",
                "chapter_prompts": [
                    f"Dark cinematic image for '{ch['title']}', abstract symbolic, deep blacks and orange accents"
                    for ch in chapters
                ]
            }

    async def generate_from_pdfs(self, pdf_en_path: Path, pdf_pt_path: Path) -> dict:
        """
        Generate complete ebook from separate English and Portuguese PDF files.

        Args:
            pdf_en_path: Path to the English PDF file
            pdf_pt_path: Path to the Portuguese PDF file

        Returns:
            Complete ebook data matching Supabase schema
        """
        # Phase 1: Extract PDF text content from both files
        print("Extracting English PDF...")
        pdf_en_content = self.extract_pdf_content(pdf_en_path)
        print(f"  {len(pdf_en_content)} characters")

        print("Extracting Portuguese PDF...")
        pdf_pt_content = self.extract_pdf_content(pdf_pt_path)
        print(f"  {len(pdf_pt_content)} characters")

        # Phase 2: Extract and structure content from both PDFs in parallel
        print("Processing PDFs with Claude...")
        extracted_en, extracted_pt = await asyncio.gather(
            self.extract_pdf_content_structured(pdf_en_content),
            self.extract_pdf_content_structured(pdf_pt_content)
        )
        print(f"English: {extracted_en['title']} ({len(extracted_en['chapters'])} chapters)")
        print(f"Portuguese: {extracted_pt['title']} ({len(extracted_pt['chapters'])} chapters)")

        # Phase 3: Generate cover image (using prompt from extraction)
        print("Generating cover image...")
        cover_prompt = extracted_en.get('cover_image_prompt', f"Dark cinematic book cover for '{extracted_en['title']}'")
        cover_url = await self._generate_image(cover_prompt, "cover.png")

        # Phase 4: Generate chapter images in parallel (using prompts from extraction)
        num_chapters = len(extracted_en['chapters'])
        print(f"Generating {num_chapters} chapter images...")

        chapter_image_tasks = []
        for ch in extracted_en['chapters']:
            # Use image_prompt from extraction or generate fallback
            prompt = ch.get('image_prompt') or get_pdf_image_prompt(ch['title'], ch.get('summary', ''))
            chapter_image_tasks.append(self._generate_image(prompt, f"chapter_{ch['number']}.png"))

        chapter_images = await asyncio.gather(*chapter_image_tasks)

        # Build chapters combining EN and PT content
        # Phase 6: Deterministically build HTML from classified blocks
        print("Building HTML from classified blocks...")
        chapters = []
        for i, (ch_en, image_url) in enumerate(zip(extracted_en['chapters'], chapter_images)):
            # Match Portuguese chapter by number
            ch_pt = next((c for c in extracted_pt['chapters'] if c['number'] == ch_en['number']), {})

            # Deterministically generate HTML from blocks
            blocks_en = ch_en.get('blocks', [])
            blocks_pt = ch_pt.get('blocks', [])
            content_en = build_html(blocks_en) if blocks_en else ''
            content_pt = build_html(blocks_pt) if blocks_pt else ''

            chapter = {
                "chapter_number": ch_en['number'],
                "title_en": ch_en['title'],
                "title_pt": ch_pt.get('title', ch_en['title']),
                "slug": self._slugify(ch_en['title']),
                "cover_image_url": image_url,
                "content_en": content_en,
                "content_pt": content_pt,
                "summary_en": ch_en.get('summary', ''),
                "summary_pt": ch_pt.get('summary', ''),
                "estimated_read_time_minutes": max(1, len(content_en.split()) // 200),
                "is_free_preview": ch_en['number'] == 1,
                "is_published": False,
            }
            chapters.append(chapter)

        # Build final ebook structure
        ebook = {
            "ebook": {
                "title_en": extracted_en['title'],
                "title_pt": extracted_pt['title'],
                "slug": self._slugify(extracted_en['title']),
                "description_en": extracted_en.get('description', ''),
                "description_pt": extracted_pt.get('description', ''),
                "cover_image_url": cover_url,
                "price_usd": 1997,  # $19.97 in cents
                "price_brl": 9970,  # R$99.70 in cents
                "status": "draft",
            },
            "chapters": sorted(chapters, key=lambda x: x["chapter_number"]),
        }

        return ebook
