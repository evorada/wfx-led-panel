"""
Example script showing how to create sprites from image files.
"""

import time
import math
from PIL import Image

def image_to_sprite_data(image_path, target_width, target_height):
    """Convert an image file to sprite data.
    
    Args:
        image_path: Path to the image file
        target_width: Target sprite width
        target_height: Target sprite height
        
    Returns:
        bytes: RGB888 sprite data
    """
    # Open and resize the image
    img = Image.open(image_path)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Extract pixel data
    data = bytes()
    for y in range(target_height):
        for x in range(target_width):
            r, g, b = img.getpixel((x, y))
            data += bytes([r, g, b])
    
    return data

def create_simple_pattern(width, height, pattern_type="checker"):
    """Create a simple pattern for testing.
    
    Args:
        width: Pattern width
        height: Pattern height
        pattern_type: Type of pattern ("checker", "gradient", "stripes")
        
    Returns:
        bytes: RGB888 pattern data
    """
    data = bytes()
    
    if pattern_type == "checker":
        for y in range(height):
            for x in range(width):
                if (x + y) % 2 == 0:
                    data += bytes([255, 255, 255])  # White
                else:
                    data += bytes([0, 0, 0])  # Black
    elif pattern_type == "gradient":
        for y in range(height):
            for x in range(width):
                r = int((x / width) * 255)
                g = int((y / height) * 255)
                b = 128
                data += bytes([r, g, b])
    elif pattern_type == "stripes":
        for y in range(height):
            for x in range(width):
                if x % 4 < 2:
                    data += bytes([255, 0, 0])  # Red
                else:
                    data += bytes([0, 0, 255])  # Blue
    
    return data

def run_sprite_image_example(matrix):
    try:
        # Clear the screen
        print("Clearing screen...")
        success, msg = matrix.clear()
        print(f"Clear: {success} - {msg}")
        time.sleep(1)  # Wait to see the clear
        
        # Create sprites with different patterns
        print("Creating pattern sprites...")
        
        # Checker pattern sprite
        checker_data = create_simple_pattern(8, 8, "checker")
        success, msg = matrix.set_sprite(0, 0, 0, 8, 8, checker_data)
        print(f"Set checker sprite: {success} - {msg}")
        time.sleep(0.5)
        
        # Gradient pattern sprite
        gradient_data = create_simple_pattern(8, 8, "gradient")
        success, msg = matrix.set_sprite(1, 8, 0, 8, 8, gradient_data)
        print(f"Set gradient sprite: {success} - {msg}")
        time.sleep(0.5)
        
        # Stripes pattern sprite
        stripes_data = create_simple_pattern(8, 8, "stripes")
        success, msg = matrix.set_sprite(2, 16, 0, 8, 8, stripes_data)
        print(f"Set stripes sprite: {success} - {msg}")
        time.sleep(0.5)
        
        # Draw all sprites
        print("Drawing sprites...")
        for i in range(3):
            success, msg = matrix.draw_sprite(i, i * 8, 0)
            print(f"Draw sprite {i}: {success} - {msg}")
            time.sleep(0.3)
        
        time.sleep(2)  # Wait to see all sprites
        
        # Animate sprites by moving them
        print("Animating sprites...")
        
        # Animation sequence 1: Move in a circle
        print("Circle animation...")
        for frame in range(8):
            angle = frame * 0.785  # 45 degrees per frame
            x = int(16 + 8 * math.cos(angle))
            y = int(8 + 8 * math.sin(angle))
            success, msg = matrix.move_sprite(0, x, y)
            print(f"Move sprite 0 to ({x}, {y}): {success} - {msg}")
            time.sleep(0.2)
        
        time.sleep(1)
        
        # Animation sequence 2: Bounce around
        print("Bounce animation...")
        for frame in range(10):
            x = (frame * 3) % 24
            y = abs(8 - (frame * 2) % 16)
            success, msg = matrix.move_sprite(1, x, y)
            print(f"Move sprite 1 to ({x}, {y}): {success} - {msg}")
            time.sleep(0.2)
        
        time.sleep(1)
        
        # Animation sequence 3: Snake movement
        print("Snake animation...")
        for frame in range(12):
            x = frame * 2
            y = 4 + int(4 * math.sin(frame * 0.5))
            success, msg = matrix.move_sprite(2, x, y)
            print(f"Move sprite 2 to ({x}, {y}): {success} - {msg}")
            time.sleep(0.15)
        
        time.sleep(2)  # Final pause to see the result
        
        print("\nSprite animation completed!")
        
    except Exception as e:
        print(f"Error: {e}")
