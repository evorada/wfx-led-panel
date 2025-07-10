# Matrix CLI

A command-line interface tool for controlling LED matrix displays via serial communication.

## Installation

```bash
poetry install
```

## Usage

```bash
# List available serial ports
poetry run matrix-cli ports

# Set brightness (0-255)
poetry run matrix-cli brightness --port /dev/ttyUSB0 128

# Print text
poetry run matrix-cli print --port /dev/ttyUSB0 "Hello World"

# Set cursor position
poetry run matrix-cli cursor --port /dev/ttyUSB0 10 20

# Fill screen with color
poetry run matrix-cli fill --port /dev/ttyUSB0 255 0 0

# Fill rectangle
poetry run matrix-cli rect --port /dev/ttyUSB0 10 10 20 20 0 255 0

# Clear screen
poetry run matrix-cli clear --port /dev/ttyUSB0

# Display an image
poetry run matrix-cli bitmap --port /dev/ttyUSB0 image.png --x 0 --y 0

# Display test patterns
poetry run matrix-cli pattern --port /dev/ttyUSB0 gradient --width 32 --height 16

# Draw individual pixels
poetry run matrix-cli pixel --port /dev/ttyUSB0 10 10 255 0 0

# Draw lines
poetry run matrix-cli line --port /dev/ttyUSB0 0 0 31 15 0 255 0

# Draw rectangles
poetry run matrix-cli draw-rect --port /dev/ttyUSB0 5 5 20 10 255 255 0

# Draw vertical lines
poetry run matrix-cli vline --port /dev/ttyUSB0 15 0 16 0 0 255

# Draw horizontal lines
poetry run matrix-cli hline --port /dev/ttyUSB0 0 8 32 255 0 0

# Sprite commands
poetry run matrix-cli set-sprite --port /dev/ttyUSB0 0 sprite.png --x 0 --y 0
poetry run matrix-cli draw-sprite --port /dev/ttyUSB0 0 10 10
poetry run matrix-cli move-sprite --port /dev/ttyUSB0 0 20 20
poetry run matrix-cli clear-sprite --port /dev/ttyUSB0 0

# Sprite tests and examples
poetry run matrix-cli sprite-test --port /dev/ttyUSB0
poetry run matrix-cli sprite-image-example --port /dev/ttyUSB0
poetry run matrix-cli sprite-animation --port /dev/ttyUSB0
```

## Commands

### Basic Display Commands
- `ports`: List available serial ports
- `brightness <value>`: Set display brightness (0-255)
- `print <text>`: Print text at current cursor position
- `cursor <x> <y>`: Set cursor position
- `fill <r> <g> <b>`: Fill entire screen with color
- `rect <x> <y> <width> <height> <r> <g> <b>`: Fill rectangle with color
- `clear`: Clear the screen

### Drawing Commands
- `pixel <x> <y> <r> <g> <b>`: Draw a single pixel
- `line <x0> <y0> <x1> <y1> <r> <g> <b>`: Draw a line
- `draw-rect <x> <y> <width> <height> <r> <g> <b>`: Draw rectangle outline
- `vline <x> <y> <height> <r> <g> <b>`: Draw fast vertical line
- `hline <x> <y> <width> <r> <g> <b>`: Draw fast horizontal line

### Image Commands
- `bitmap <filename> [--x <x>] [--y <y>]`: Display an image file
- `pattern <pattern> [--x <x>] [--y <y>] [--width <w>] [--height <h>]`: Display test patterns
  - Patterns: `gradient`, `rainbow`, `checkerboard`

### Sprite Commands
- `set-sprite <sprite_id> <filename> [--x <x>] [--y <y>]`: Set a sprite with image data
- `clear-sprite <sprite_id>`: Clear a sprite from memory and screen
- `draw-sprite <sprite_id> <x> <y>`: Draw a sprite at a specific location
- `move-sprite <sprite_id> <x> <y>`: Move a sprite to a new location

### Test Commands
- `sprite-test`: Test sprite functionality
- `sprite-image-example`: Test sprite image functionality
- `sprite-animation`: Test sprite animation functionality

## Supported Image Formats

The CLI supports common image formats including:
- PNG
- JPG/JPEG
- GIF
- BMP
- And other formats supported by Pillow

## Sprite System

The Matrix CLI includes a sprite system that allows you to:
- Load images as sprites (sprite IDs 0-15)
- Position and move sprites on the display
- Create animations using multiple sprites
- Clear sprites when no longer needed

Sprites are stored in the device memory and can be drawn at different positions without reloading the image data. 