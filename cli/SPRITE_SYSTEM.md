# Sprite System Documentation

The sprite system allows you to store up to 16 images in memory and draw them at specific locations on the LED matrix display. Sprites can be moved around the screen, and the system automatically handles clearing the previous position when sprites are moved.

## Features

- **16 Sprite Slots**: Store up to 16 different sprites in memory
- **Automatic Position Tracking**: Sprites remember their last position for proper clearing
- **RGB565 Format**: Efficient color storage (5-6-5 bit RGB)
- **Flow Control**: Large sprite data is transmitted with flow control to prevent buffer overflow
- **Image Resizing**: Automatic resizing of images to fit sprite dimensions

## Sprite Commands

### Python API

```python
from matrix_cli.matrix import MatrixDisplay

matrix = MatrixDisplay('/dev/ttyUSB0')

# Set a sprite with image data
success, msg = matrix.set_sprite(sprite_id, x, y, width, height, bitmap_data)

# Draw a sprite at a specific location
success, msg = matrix.draw_sprite(sprite_id, x, y)

# Move a sprite to a new location (updates stored position)
success, msg = matrix.move_sprite(sprite_id, x, y)

# Clear a sprite from memory and screen
success, msg = matrix.clear_sprite(sprite_id)
```

### CLI Commands

```bash
# Set a sprite from an image file
python -m matrix_cli.cli --port /dev/ttyUSB0 set-sprite 0 image.png --x 0 --y 0 --width 8 --height 8

# Draw a sprite at a specific location
python -m matrix_cli.cli --port /dev/ttyUSB0 draw-sprite 0 10 5

# Move a sprite to a new location
python -m matrix_cli.cli --port /dev/ttyUSB0 move-sprite 0 15 8

# Clear a sprite
python -m matrix_cli.cli --port /dev/ttyUSB0 clear-sprite 0
```

## Technical Details

### Sprite Structure

Each sprite contains:
- `active`: Boolean indicating if the sprite is in use
- `x, y`: Current position coordinates
- `width, height`: Sprite dimensions
- `data`: RGB565 pixel data (2 bytes per pixel)
- `last_x, last_y`: Previous position for proper clearing

### Data Format

- **Input**: RGB888 format (3 bytes per pixel: R, G, B)
- **Storage**: RGB565 format (2 bytes per pixel: 5-bit R, 6-bit G, 5-bit B)
- **Maximum Size**: 64x64 pixels (8KB of data per sprite)

### Protocol

The sprite system uses the same protocol as the bitmap system with additional commands:

- `CMD_SET_SPRITE (0x0E)`: Set sprite data and properties
- `CMD_CLEAR_SPRITE (0x0F)`: Clear sprite from memory
- `CMD_DRAW_SPRITE (0x10)`: Draw sprite at location
- `CMD_MOVE_SPRITE (0x11)`: Move sprite and update position

### Flow Control

For large sprites, the system uses flow control:
- Data is sent in 64-pixel chunks
- Receiver sends 0xFF after each chunk
- Prevents buffer overflow during transmission

## Examples

### Basic Sprite Usage

```python
# Create a simple red sprite
red_data = bytes([255, 0, 0] * 64)  # 8x8 red sprite
matrix.set_sprite(0, 0, 0, 8, 8, red_data)
matrix.draw_sprite(0, 0, 0)

# Move the sprite
matrix.move_sprite(0, 10, 5)
```

### Animation Example

```python
# Create a sprite
matrix.set_sprite(0, 0, 0, 8, 8, sprite_data)

# Animate by moving
for i in range(10):
    matrix.move_sprite(0, i * 2, i)
    time.sleep(0.1)
```

### Multiple Sprites

```python
# Set multiple sprites
matrix.set_sprite(0, 0, 0, 8, 8, sprite1_data)
matrix.set_sprite(1, 8, 0, 8, 8, sprite2_data)
matrix.set_sprite(2, 16, 0, 8, 8, sprite3_data)

# Draw all sprites
for i in range(3):
    matrix.draw_sprite(i, i * 8, 0)
```

## Error Handling

The system provides detailed error messages:
- Invalid sprite ID (must be 0-15)
- Sprite too large (max 64x64)
- Sprite not active
- Data transmission timeout
- Invalid data format

## Performance Considerations

- **Memory Usage**: Each sprite uses up to 8KB of RAM
- **Transmission Time**: Large sprites take time to upload
- **Drawing Speed**: Sprites are drawn pixel by pixel
- **Position Updates**: Moving sprites clears the old position automatically

## Limitations

- Maximum 16 sprites simultaneously
- Maximum sprite size: 64x64 pixels
- RGB565 color format (reduced color depth)
- Serial transmission speed limits
- Memory constraints on the ESP32 