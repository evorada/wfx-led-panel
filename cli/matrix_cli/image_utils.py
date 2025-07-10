"""
Image processing utilities for matrix display.
"""

from PIL import Image
from typing import Tuple


def load_and_process_image(filename: str) -> Tuple[int, int, bytes]:
    """
    Load an image file and convert it to RGB bitmap data.

    Args:
        filename: Path to the image file

    Returns:
        Tuple of (width, height, rgb_data)

    Raises:
        ValueError: If image cannot be loaded or processed
    """
    try:
        with Image.open(filename) as img:
            width, height = img.size

            img = img.convert("RGB")
            rgb_data = img.tobytes()
            return width, height, rgb_data

    except Exception as e:
        raise ValueError(f"Failed to load image '{filename}': {str(e)}")


def create_test_pattern(
    width: int, height: int, pattern_type: str = "gradient"
) -> Tuple[int, int, bytes]:
    """
    Create a test pattern for testing the display.

    Args:
        width: Pattern width
        height: Pattern height
        pattern_type: Type of pattern ("gradient", "rainbow", "checkerboard")

    Returns:
        Tuple of (width, height, rgb_data)
    """
    if pattern_type == "gradient":
        # Create RGB gradient
        data = []
        for y in range(height):
            for x in range(width):
                r = int(255 * x / width)
                g = int(255 * y / height)
                b = int(255 * (x + y) / (width + height))
                data.extend([r, g, b])
        return width, height, bytes(data)

    elif pattern_type == "rainbow":
        # Create rainbow pattern
        data = []
        for y in range(height):
            for x in range(width):
                hue = (x + y) / (width + height)
                # Simple HSV to RGB conversion
                h = hue * 6
                c = 255
                x_h = c * (1 - abs(h % 2 - 1))
                if h < 1:
                    r, g, b = c, x_h, 0
                elif h < 2:
                    r, g, b = x_h, c, 0
                elif h < 3:
                    r, g, b = 0, c, x_h
                elif h < 4:
                    r, g, b = 0, x_h, c
                elif h < 5:
                    r, g, b = x_h, 0, c
                else:
                    r, g, b = c, 0, x_h
                data.extend([r, g, b])
        return width, height, bytes(data)

    elif pattern_type == "checkerboard":
        # Create checkerboard pattern
        data = []
        for y in range(height):
            for x in range(width):
                if (x // 8 + y // 8) % 2 == 0:
                    r, g, b = 255, 255, 255  # White
                else:
                    r, g, b = 0, 0, 0  # Black
                data.extend([r, g, b])
        return width, height, bytes(data)

    else:
        raise ValueError(f"Unknown pattern type: {pattern_type}")
