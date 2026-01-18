#!/usr/bin/env python3
"""
Generate images using Gemini/Imagen 3 API.

Usage:
    python gemini-image.py "your prompt here" --output image.png
    python gemini-image.py "arcane glider sigil" --style mystical --output glider.png

Requires:
    pip install google-generativeai pillow

    Set GOOGLE_API_KEY environment variable or pass --api-key
    Get your key at: https://aistudio.google.com/apikey
"""

import argparse
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    try:
        import google.generativeai
    except ImportError:
        missing.append("google-generativeai")
    try:
        from PIL import Image
    except ImportError:
        missing.append("pillow")

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)

def generate_image(prompt: str, output_path: str, api_key: str = None, style: str = None):
    """Generate an image using Gemini/Imagen."""
    import google.generativeai as genai
    from PIL import Image
    import io

    # Configure API
    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: Set GOOGLE_API_KEY environment variable or pass --api-key")
        print("Get your key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    genai.configure(api_key=api_key)

    # Build prompt with style hints
    full_prompt = prompt
    if style:
        style_hints = {
            "mystical": "arcane sigil, ethereal glow, magical energy, dark mysterious background",
            "minimal": "minimalist, clean lines, simple geometric, flat design",
            "cyberpunk": "neon glow, cyberpunk aesthetic, dark background, tech vibes",
            "watercolor": "watercolor painting style, soft edges, artistic brush strokes",
        }
        if style in style_hints:
            full_prompt = f"{prompt}. Style: {style_hints[style]}"
        else:
            full_prompt = f"{prompt}. Style: {style}"

    print(f"Generating image with prompt:\n{full_prompt}\n")

    try:
        # Use Imagen 3 model
        model = genai.ImageGenerationModel("imagen-3.0-generate-002")

        result = model.generate_images(
            prompt=full_prompt,
            number_of_images=1,
            aspect_ratio="1:1",  # Square for profile pics
            safety_filter_level="block_only_high",
        )

        if result.images:
            image_data = result.images[0]._pil_image
            image_data.save(output_path)
            print(f"Image saved to: {output_path}")
        else:
            print("No image generated. Try adjusting your prompt.")
            sys.exit(1)

    except Exception as e:
        error_msg = str(e)
        if "not found" in error_msg.lower() or "404" in error_msg:
            print("Error: Imagen model not available. You may need to:")
            print("  1. Enable the Imagen API in Google Cloud Console")
            print("  2. Use Google AI Studio web UI instead: https://aistudio.google.com")
        else:
            print(f"Error generating image: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini/Imagen 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("-o", "--output", default="output.png", help="Output file path")
    parser.add_argument("-k", "--api-key", help="Google API key (or set GOOGLE_API_KEY)")
    parser.add_argument("-s", "--style", choices=["mystical", "minimal", "cyberpunk", "watercolor"],
                        help="Pre-defined style to apply")

    args = parser.parse_args()

    check_dependencies()
    generate_image(args.prompt, args.output, args.api_key, args.style)

if __name__ == "__main__":
    main()
