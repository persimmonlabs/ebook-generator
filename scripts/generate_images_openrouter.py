#!/usr/bin/env python3
"""
Generate images for ALPHA BODY PROTOCOL using OpenRouter's Nano Banana Pro.
Uses google/gemini-3-pro-image-preview model.
"""

import base64
import json
import time
import urllib.request
from pathlib import Path

# OpenRouter API key
OPENROUTER_API_KEY = "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"

# Image prompts matching the ebook structure
PROMPTS = {
    "cover": "Create a dark, cinematic book cover image for 'ALPHA BODY PROTOCOL'. Abstract representation of masculine power and strength. Silhouette of a powerful male figure with geometric shapes suggesting muscle and structure. Color palette: deep blacks, dark reds, orange accents. Epic scale, dramatic lighting. No text on the image. Movie poster quality. Professional photography, 8k resolution.",

    "ch1_intro": "Dark cinematic abstract image representing introduction and purpose. Geometric shapes forming pathways leading forward, light emerging from darkness. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting with cinematic shadows. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch2_body_weapon": "Dark cinematic abstract image representing the body as power and authority. Geometric shield and sword shapes, crystalline structures suggesting raw strength. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch3_training": "Dark cinematic abstract image representing minimalist training and efficiency. Geometric weights, clean lines, precision engineering aesthetic. Iron and steel textures. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch4_nutrition": "Dark cinematic abstract image representing strategic nutrition. Molecular structures, DNA helix patterns, crystalline food elements. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch5_hormones": "Dark cinematic abstract image representing hormonal optimization and biochemistry. Chemical molecular structures, flowing energy patterns, molecular bonds glowing. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch6_sleep": "Dark cinematic abstract image representing sleep and recovery. Moon phases, waves of restorative energy, restoration patterns. Dark blues transitioning to blacks with orange accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch7_posture": "Dark cinematic abstract image representing posture and commanding presence. Vertical geometric structures in perfect alignment, architectural spine-like forms. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch8_protocol": "Dark cinematic abstract image representing the complete integrated protocol system. Multiple geometric systems working in perfect harmony, dashboard aesthetic with data visualization. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch9_conclusion": "Dark cinematic abstract image representing transformation and achievement. Rising phoenix-like geometric shapes, victory formation ascending. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",

    "ch10_resources": "Dark cinematic abstract image representing knowledge and resources. Geometric book shapes, data visualization patterns, organized structural elements. Color palette: deep blacks, reds, orange electric accents. Dramatic lighting. No text, no faces, no human figures. Epic scale. Professional photography.",
}


def generate_image(prompt: str, output_path: Path) -> bool:
    """
    Generate an image using OpenRouter's Nano Banana Pro.

    Args:
        prompt: The image generation prompt
        output_path: Where to save the image

    Returns:
        True if successful, False otherwise
    """
    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": "google/gemini-3-pro-image-preview",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["image", "text"]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://thealphagrit.com",
        "X-Title": "AlphaGrit Ebook Generator"
    }

    try:
        print(f"Generating: {output_path.name}...")

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        # Extract image from response
        message = result.get("choices", [{}])[0].get("message", {})
        images = message.get("images", [])

        if not images:
            # Check for content with image parts
            content = message.get("content", [])
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "image_url":
                        image_url = part.get("image_url", {}).get("url", "")
                        if image_url.startswith("data:image"):
                            # Extract base64 data
                            base64_data = image_url.split(",", 1)[1]
                            image_bytes = base64.b64decode(base64_data)
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            with open(output_path, "wb") as f:
                                f.write(image_bytes)
                            file_size = len(image_bytes) / 1024
                            print(f"  [OK] Saved: {output_path} ({file_size:.1f} KB)")
                            return True

            print(f"  [FAIL] No image in response: {json.dumps(result, indent=2)[:500]}")
            return False

        # Get first image
        image_data = images[0]
        if isinstance(image_data, dict):
            image_url = image_data.get("image_url", {}).get("url", "")
        else:
            image_url = str(image_data)

        if image_url.startswith("data:image"):
            # Base64 encoded image
            base64_data = image_url.split(",", 1)[1]
            image_bytes = base64.b64decode(base64_data)
        else:
            print(f"  [FAIL] Unexpected image format: {image_url[:100]}")
            return False

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        file_size = len(image_bytes) / 1024
        print(f"  [OK] Saved: {output_path} ({file_size:.1f} KB)")
        return True

    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def main():
    """Generate all images for the ebook."""

    # Output directory - use new folder for Nano Banana images
    output_dir = Path("output/2025-11-30_alpha-body-protocol/images_nano")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("ALPHA BODY PROTOCOL - Image Generation")
    print("Using OpenRouter Nano Banana Pro (Gemini 3 Pro Image)")
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

        # Rate limiting - wait 3 seconds between requests
        if name != list(PROMPTS.keys())[-1]:
            time.sleep(3)

    print()
    print("=" * 60)
    print(f"Complete: {success_count}/{total} images generated")
    print(f"Location: {output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
