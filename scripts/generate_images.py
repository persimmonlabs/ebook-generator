#!/usr/bin/env python3
"""
Generate images for ALPHA BODY PROTOCOL using free Pollinations.ai API.
No API key required - completely free.
"""

import os
import time
import urllib.parse
import urllib.request
from pathlib import Path


# Image prompts matching the ebook structure
PROMPTS = {
    "cover": "Dark cinematic book cover for 'ALPHA BODY PROTOCOL'. Abstract representation of masculine power and strength. Silhouette of a powerful male figure with geometric shapes suggesting muscle and structure. Color palette: deep blacks, dark reds, orange accents. Epic scale, dramatic lighting. No text, no faces. Movie poster quality. 8k resolution, professional photography",

    "ch1_intro": "Dark cinematic abstract image representing introduction and purpose. Geometric shapes, pathways leading forward, light emerging from darkness. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting, cinematic shadows. No text, no faces, no human figures. Epic scale. 8k",

    "ch2_body_weapon": "Dark cinematic abstract image representing the body as power and authority. Geometric shield and sword shapes, crystalline structures suggesting strength. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch3_training": "Dark cinematic abstract image representing minimalist training efficiency. Geometric weights, clean lines, precision engineering aesthetic. Iron and steel textures. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch4_nutrition": "Dark cinematic abstract image representing strategic nutrition. Molecular structures, DNA helix, crystalline food elements. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch5_hormones": "Dark cinematic abstract image representing hormonal optimization. Chemical structures, flowing energy patterns, molecular bonds. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch6_sleep": "Dark cinematic abstract image representing sleep and recovery. Moon phases, waves of energy, restoration patterns. Dark blues transitioning to blacks and orange accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch7_posture": "Dark cinematic abstract image representing posture and presence. Vertical geometric structures, perfect alignment, architectural spine-like forms. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch8_protocol": "Dark cinematic abstract image representing the complete integrated protocol. Multiple geometric systems working in harmony, dashboard aesthetic. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch9_conclusion": "Dark cinematic abstract image representing transformation and achievement. Rising phoenix-like geometric shapes, victory formation. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",

    "ch10_resources": "Dark cinematic abstract image representing knowledge resources. Geometric book shapes, data visualization, organized structures. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. 8k",
}


def generate_image(prompt: str, output_path: Path, width: int = 1024, height: int = 1024) -> bool:
    """
    Generate an image using Pollinations.ai free API.

    Args:
        prompt: The image generation prompt
        output_path: Where to save the image
        width: Image width (default 1024)
        height: Image height (default 1024)

    Returns:
        True if successful, False otherwise
    """
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)

    # Pollinations.ai URL - completely free, no API key
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&model=flux"

    try:
        print(f"Generating: {output_path.name}...")

        # Create request with timeout
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
        )

        # Download the image (may take 30-60 seconds per image)
        with urllib.request.urlopen(request, timeout=120) as response:
            image_data = response.read()

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_data)

        file_size = len(image_data) / 1024
        print(f"  [OK] Saved: {output_path} ({file_size:.1f} KB)")
        return True

    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def main():
    """Generate all images for the ebook."""

    # Output directory
    output_dir = Path("output/2025-11-30_alpha-body-protocol/images")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("ALPHA BODY PROTOCOL - Image Generation")
    print("Using Pollinations.ai (FREE - no API key needed)")
    print("=" * 60)
    print()

    success_count = 0
    total = len(PROMPTS)

    for name, prompt in PROMPTS.items():
        output_path = output_dir / f"{name}.png"

        # Skip if already exists
        if output_path.exists():
            print(f"Skipping {name}.png (already exists)")
            success_count += 1
            continue

        if generate_image(prompt, output_path):
            success_count += 1

        # Rate limiting - wait 2 seconds between requests
        if name != list(PROMPTS.keys())[-1]:
            time.sleep(2)

    print()
    print("=" * 60)
    print(f"Complete: {success_count}/{total} images generated")
    print(f"Location: {output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
