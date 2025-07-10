"""
Sprite animation demo that loads coin frames and cycles through them.
"""

import os
import time
import glob
from typing import List
from PIL import Image
from .matrix import MatrixDisplay


def load_frames(directory: str = "../resources/knight/idle") -> List[Image.Image]:
    """Load all animation frames from the specified directory.

    Args:
        directory: Directory containing frame files

    Returns:
        List of RGB888 sprite data for each frame
    """
    # Find all frame files (PNG and GIF)
    png_files = glob.glob(os.path.join(directory, "*.png"))
    gif_files = glob.glob(os.path.join(directory, "*.gif"))
    frame_files = sorted(png_files + gif_files)

    if not frame_files:
        raise ValueError(f"No frames found in {directory}")

    frames = []
    for frame_file in frame_files:
        try:
            # Load and resize the image
            img = Image.open(frame_file)

            # Convert to RGB if needed
            if img.mode != "RGB":
                print(f"Converting {frame_file} to RGB")
                img = img.convert("RGB")

            # Extract pixel data
            frames.append(img)
            print(f"Loaded frame: {os.path.basename(frame_file)}")

        except Exception as e:
            print(f"Error loading {frame_file}: {e}")
            continue

    if not frames:
        raise ValueError("No valid frames could be loaded")

    print(f"Loaded {len(frames)} frames")
    return frames


def run_animation(matrix: MatrixDisplay, frame_delay: float = 0.1):
    """Run the animation in the center of the screen.

    Args:
        matrix: Matrix display instance
        frame_delay: Delay between frames in seconds
        cycles: Number of animation cycles to run
    """
    try:
        # Load frames
        print("Loading animation frames...")
        frames = load_frames()

        # Clear the screen
        print("Clearing screen...")
        success, msg = matrix.clear()
        print(f"Clear: {success} - {msg}")
        time.sleep(1)

        center_x = int((64 - frames[0].width) / 2)
        center_y = int((64 - frames[0].height) / 2)

        # Set up sprites for each frame (we'll use sprites 0-11 for the 12 frames)
        print("Setting up sprite frames...")
        for i, frame in enumerate(frames):
            if i >= 12:  # Limit to 12 sprites
                break
            success, msg = matrix.set_sprite(
                i, center_x, center_y, frame.width, frame.height, frame.tobytes()
            )
            print(f"Set sprite {i}: {success} - {msg}")
            time.sleep(0.1)

        # Run the animation
        while True:
            for frame in range(len(frames)):
                if frame >= 12:  # Limit to 12 sprites
                    break

                # Draw the current frame
                success, msg = matrix.draw_sprite(frame, center_x, center_y)

                time.sleep(frame_delay)

    except Exception as e:
        print(f"Error in animation: {e}")


def run_sprite_animation(matrix: MatrixDisplay):
    """Run the sprite animation demo."""
    print("=== Animation Demo ===")
    print("This demo loads animation frames and cycles through them")
    print("in the center of the screen.")
    print()

    # Run the animation
    run_animation(matrix, frame_delay=0.1)
