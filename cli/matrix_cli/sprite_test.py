"""
Test script for the sprite system.
"""

import time

def create_test_sprite(width, height, color):
    """Create a simple test sprite with a solid color."""
    data = bytes()
    for _ in range(width * height):
        data += bytes(color)
    return data

def run_sprite_test(matrix):
    try:
        # Clear the screen
        print("Clearing screen...")
        success, msg = matrix.clear()
        print(f"Clear: {success} - {msg}")
        time.sleep(1)  # Wait to see the clear
        
        # Create a red 8x8 sprite
        print("Creating red sprite...")
        red_sprite = create_test_sprite(8, 8, [255, 0, 0])  # Red
        success, msg = matrix.set_sprite(0, 0, 0, 8, 8, red_sprite)
        print(f"Set sprite 0: {success} - {msg}")
        time.sleep(0.5)
        
        # Create a green 8x8 sprite
        print("Creating green sprite...")
        green_sprite = create_test_sprite(8, 8, [0, 255, 0])  # Green
        success, msg = matrix.set_sprite(1, 8, 0, 8, 8, green_sprite)
        print(f"Set sprite 1: {success} - {msg}")
        time.sleep(0.5)
        
        # Create a blue 8x8 sprite
        print("Creating blue sprite...")
        blue_sprite = create_test_sprite(8, 8, [0, 0, 255])  # Blue
        success, msg = matrix.set_sprite(2, 16, 0, 8, 8, blue_sprite)
        print(f"Set sprite 2: {success} - {msg}")
        time.sleep(0.5)
        
        # Draw all sprites at their initial positions
        print("Drawing sprites...")
        success, msg = matrix.draw_sprite(0, 0, 0)
        print(f"Draw sprite 0: {success} - {msg}")
        time.sleep(0.3)
        
        success, msg = matrix.draw_sprite(1, 8, 0)
        print(f"Draw sprite 1: {success} - {msg}")
        time.sleep(0.3)
        
        success, msg = matrix.draw_sprite(2, 16, 0)
        print(f"Draw sprite 2: {success} - {msg}")
        time.sleep(1)  # Wait to see all sprites
        
        # Move sprites around
        print("Moving sprites...")
        success, msg = matrix.move_sprite(0, 0, 8)
        print(f"Move sprite 0: {success} - {msg}")
        time.sleep(0.5)
        
        success, msg = matrix.move_sprite(1, 8, 8)
        print(f"Move sprite 1: {success} - {msg}")
        time.sleep(0.5)
        
        success, msg = matrix.move_sprite(2, 16, 8)
        print(f"Move sprite 2: {success} - {msg}")
        time.sleep(1)  # Wait to see the moved sprites
        
        # Clear one sprite
        print("Clearing sprite 1...")
        success, msg = matrix.clear_sprite(1)
        print(f"Clear sprite 1: {success} - {msg}")
        time.sleep(1)  # Wait to see the cleared sprite
        
        print("\nSprite test completed!")
        
    except Exception as e:
        print(f"Error: {e}")