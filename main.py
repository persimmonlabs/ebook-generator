#!/usr/bin/env python3
"""
Alpha Grit E-Book Generator CLI
Transforms content into a complete bilingual ebook with Wagner Nascimento's voice.
Outputs SQL seed file for Supabase database.

Two input modes:
1. Topic mode: Generate from a sentence (uses Perplexity research + Claude)
2. PDF mode: Import existing EN/PT PDFs, generate image prompts and images

Usage:
    # Topic mode (generates content from scratch)
    python main.py "How to escape the modern food matrix"
    python main.py "Mental discipline for entrepreneurs" --chapters 7

    # PDF mode (imports existing bilingual content)
    python main.py --pdf-en ./ebook-en.pdf --pdf-pt ./ebook-pt.pdf
    python main.py --pdf-en ./alpha-body-en.pdf --pdf-pt ./alpha-body-pt.pdf --output ./my-ebook
"""

import argparse
import asyncio
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from generator import EbookGenerator


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a complete ebook from topic or PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Topic mode (generates content from scratch)
    python main.py "How to escape the modern food matrix"
    python main.py "Mental discipline for entrepreneurs" --chapters 7

    # PDF mode (imports existing bilingual content)
    python main.py --pdf-en ./ebook-en.pdf --pdf-pt ./ebook-pt.pdf
    python main.py --pdf-en ./alpha-body-en.pdf --pdf-pt ./alpha-body-pt.pdf -o ./output
        """,
    )

    parser.add_argument(
        "topic",
        type=str,
        nargs="?",
        default=None,
        help="One sentence describing the ebook topic (topic mode)",
    )

    parser.add_argument(
        "--pdf-en",
        type=str,
        default=None,
        help="Path to English PDF file (PDF mode)",
    )

    parser.add_argument(
        "--pdf-pt",
        type=str,
        default=None,
        help="Path to Portuguese PDF file (PDF mode)",
    )

    parser.add_argument(
        "--chapters",
        "-c",
        type=int,
        default=5,
        help="Number of chapters to generate (topic mode only, default: 5)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output directory (default: ./output/<timestamp>)",
    )

    args = parser.parse_args()

    # Validate: must have either topic or both PDFs
    has_pdfs = args.pdf_en or args.pdf_pt
    if not args.topic and not has_pdfs:
        parser.error("Either provide a topic or use --pdf-en and --pdf-pt to import from PDFs")

    if args.topic and has_pdfs:
        parser.error("Cannot use both topic and PDF mode. Choose one.")

    if has_pdfs and not (args.pdf_en and args.pdf_pt):
        parser.error("PDF mode requires both --pdf-en and --pdf-pt files")

    return args


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    import re
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')[:50]  # Limit length


def setup_output_dir(output_path: str | None, name_hint: str | None = None) -> Path:
    """Create and return the output directory.

    Format: output/yyyy-mm-dd_ebook-slug/
    """
    if output_path:
        output_dir = Path(output_path)
    else:
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        if name_hint:
            slug = slugify(name_hint)
            dir_name = f"{date_prefix}_{slug}"
        else:
            dir_name = date_prefix
        output_dir = Path("output") / dir_name

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def escape_sql_string(value: str | None) -> str:
    """Escape a string for SQL insertion."""
    if value is None:
        return "NULL"
    # Escape single quotes by doubling them
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def generate_seed_sql(ebook_data: dict) -> str:
    """Generate SQL seed file content from ebook data."""
    ebook = ebook_data["ebook"]
    chapters = ebook_data["chapters"]

    # Generate UUIDs
    ebook_id = str(uuid.uuid4())

    # Calculate total read time from chapters
    total_read_time = sum(ch.get("estimated_read_time_minutes", 0) for ch in chapters)

    lines = [
        "-- E-book Seed File",
        f"-- Generated: {datetime.now().isoformat()}",
        f"-- Title: {ebook['title_en']}",
        "",
        "-- Insert ebook",
        "INSERT INTO ebooks (",
        "  id, title_en, title_pt, slug, description_en, description_pt,",
        "  cover_image_url, price_usd, price_brl, estimated_read_time_minutes, status",
        ") VALUES (",
        f"  '{ebook_id}',",
        f"  {escape_sql_string(ebook.get('title_en'))},",
        f"  {escape_sql_string(ebook.get('title_pt'))},",
        f"  {escape_sql_string(ebook.get('slug'))},",
        f"  {escape_sql_string(ebook.get('description_en'))},",
        f"  {escape_sql_string(ebook.get('description_pt'))},",
        f"  {escape_sql_string(ebook.get('cover_image_url'))},",
        f"  {ebook.get('price_usd', 0)},",
        f"  {ebook.get('price_brl', 0)},",
        f"  {total_read_time},",
        f"  {escape_sql_string(ebook.get('status', 'draft'))}",
        ");",
        "",
        "-- Insert chapters",
    ]

    for chapter in chapters:
        chapter_id = str(uuid.uuid4())
        lines.extend([
            f"INSERT INTO chapters (",
            "  id, ebook_id, chapter_number, title_en, title_pt, slug,",
            "  cover_image_url, content_en, content_pt, summary_en, summary_pt,",
            "  estimated_read_time_minutes, is_free_preview, is_published",
            ") VALUES (",
            f"  '{chapter_id}',",
            f"  '{ebook_id}',",
            f"  {chapter.get('chapter_number', 0)},",
            f"  {escape_sql_string(chapter.get('title_en'))},",
            f"  {escape_sql_string(chapter.get('title_pt'))},",
            f"  {escape_sql_string(chapter.get('slug'))},",
            f"  {escape_sql_string(chapter.get('cover_image_url'))},",
            f"  {escape_sql_string(chapter.get('content_en'))},",
            f"  {escape_sql_string(chapter.get('content_pt'))},",
            f"  {escape_sql_string(chapter.get('summary_en'))},",
            f"  {escape_sql_string(chapter.get('summary_pt'))},",
            f"  {chapter.get('estimated_read_time_minutes', 0)},",
            f"  {str(chapter.get('is_free_preview', False)).lower()},",
            f"  {str(chapter.get('is_published', False)).lower()}",
            ");",
            "",
        ])

    return "\n".join(lines)


def save_seed_file(ebook_data: dict, output_dir: Path) -> Path:
    """Save ebook data as SQL seed file."""
    output_file = output_dir / "seed.sql"
    sql_content = generate_seed_sql(ebook_data)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sql_content)
    return output_file


def print_summary(ebook_data: dict, output_file: Path) -> None:
    """Print generation summary."""
    ebook = ebook_data["ebook"]
    chapters = ebook_data["chapters"]
    total_read_time = sum(ch.get("estimated_read_time_minutes", 0) for ch in chapters)

    print("\n" + "=" * 60)
    print("EBOOK SEED FILE GENERATED")
    print("=" * 60)
    print(f"\nTitle (EN): {ebook['title_en']}")
    print(f"Title (PT): {ebook['title_pt']}")
    print(f"Slug: {ebook['slug']}")
    print(f"Chapters: {len(chapters)}")
    print(f"Total Read Time: ~{total_read_time} min")
    print(f"Status: {ebook['status']}")
    print(f"\nPrice USD: ${ebook['price_usd'] / 100:.2f}")
    print(f"Price BRL: R${ebook['price_brl'] / 100:.2f}")
    print("\nChapters:")
    for ch in chapters:
        preview = " [FREE PREVIEW]" if ch["is_free_preview"] else ""
        print(f"  {ch['chapter_number']}. {ch['title_en']}{preview}")
        print(f"     ~{ch['estimated_read_time_minutes']} min read")

    print(f"\nSeed file saved to: {output_file.absolute()}")
    print("\nTo apply to database:")
    print(f"  psql -f {output_file.name}")
    print("  -- or run in Supabase SQL Editor")
    print("=" * 60)


async def main() -> int:
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse arguments
    args = parse_args()

    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("Create a .env file with: OPENROUTER_API_KEY=your_key_here")
        return 1

    # Determine name hint for output directory
    if args.pdf_en:
        pdf_en_path = Path(args.pdf_en)
        pdf_pt_path = Path(args.pdf_pt)
        if not pdf_en_path.exists():
            print(f"Error: English PDF file not found: {pdf_en_path}")
            return 1
        if not pdf_pt_path.exists():
            print(f"Error: Portuguese PDF file not found: {pdf_pt_path}")
            return 1
        name_hint = pdf_en_path.stem  # Use English PDF filename
    else:
        name_hint = args.topic

    # Setup output directory
    output_dir = setup_output_dir(args.output, name_hint)
    print(f"\nOutput directory: {output_dir.absolute()}")

    # Create generator
    generator = EbookGenerator(api_key, output_dir)

    try:
        if args.pdf_en:
            # PDF mode: import from PDF files
            print(f"\nImporting ebook from PDFs:")
            print(f"  English: {pdf_en_path}")
            print(f"  Portuguese: {pdf_pt_path}")
            print("-" * 60)
            ebook_data = await generator.generate_from_pdfs(pdf_en_path, pdf_pt_path)
        else:
            # Topic mode: generate from scratch
            print(f"\nGenerating ebook for: \"{args.topic}\"")
            print(f"Chapters: {args.chapters}")
            print("-" * 60)
            ebook_data = await generator.generate(args.topic, args.chapters)

    except Exception as e:
        print(f"\nError generating ebook: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Save output as SQL seed file
    output_file = save_seed_file(ebook_data, output_dir)

    # Print summary
    print_summary(ebook_data, output_file)

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
