# Serial Communication Protocol

This document describes the serial communication protocol used by the ESP32 LED Matrix GPU firmware.

## Protocol Overview

All communication follows a simple packet-based protocol:

```
START_BYTE (0xFF) + COMMAND + LENGTH + DATA
```

### Packet Structure

| Field | Size | Description |
|-------|------|-------------|
| START_BYTE | 1 byte | Always 0xFF |
| COMMAND | 1 byte | Command identifier |
| LENGTH | 1 byte | Length of data payload |
| DATA | N bytes | Command-specific data |

### Response Format

All commands receive an acknowledgment response:

```
START_BYTE (0xFF) + ACK_BYTE (0xAC) + CMD + SUCCESS + MSG_LENGTH + MESSAGE
```

| Field | Size | Description |
|-------|------|-------------|
| START_BYTE | 1 byte | Always 0xFF |
| ACK_BYTE | 1 byte | Always 0xAC |
| CMD | 1 byte | Original command |
| SUCCESS | 1 byte | 0x01 for success, 0x00 for failure |
| MSG_LENGTH | 1 byte | Length of message (0 if no message) |
| MESSAGE | N bytes | Optional error/success message |

## Commands

### Drawing Commands

#### CMD_DRAW_PIXEL (0x01)
Draw a single pixel.

**Data Format:**
```
X (1 byte) + Y (1 byte) + R (1 byte) + G (1 byte) + B (1 byte)
```

**Example:**
```
0xFF 0x01 0x05 0x0A 0x0B 0xFF 0x00 0x00
```
Draws a red pixel at position (10, 11).

#### CMD_FILL_SCREEN (0x02)
Fill the entire screen with a color.

**Data Format:**
```
R (1 byte) + G (1 byte) + B (1 byte)
```

**Example:**
```
0xFF 0x02 0x03 0x00 0x00 0xFF
```
Fills screen with red.

#### CMD_DRAW_LINE (0x03)
Draw a line between two points.

**Data Format:**
```
X0 (1 byte) + Y0 (1 byte) + X1 (1 byte) + Y1 (1 byte) + R (1 byte) + G (1 byte) + B (1 byte)
```

**Example:**
```
0xFF 0x03 0x07 0x00 0x00 0x1F 0x0F 0x00 0xFF 0x00
```
Draws a green line from (0,0) to (31,15).

#### CMD_DRAW_RECT (0x04)
Draw a rectangle outline.

**Data Format:**
```
X (1 byte) + Y (1 byte) + WIDTH (1 byte) + HEIGHT (1 byte) + R (1 byte) + G (1 byte) + B (1 byte)
```

#### CMD_FILL_RECT (0x05)
Fill a rectangle with color.

**Data Format:**
```
X (1 byte) + Y (1 byte) + WIDTH (1 byte) + HEIGHT (1 byte) + R (1 byte) + G (1 byte) + B (1 byte)
```

#### CMD_DRAW_FAST_VLINE (0x06)
Draw a fast vertical line.

**Data Format:**
```
X (1 byte) + Y (1 byte) + HEIGHT (1 byte) + R (1 byte) + G (1 byte) + B (1 byte)
```

#### CMD_DRAW_FAST_HLINE (0x07)
Draw a fast horizontal line.

**Data Format:**
```
X (1 byte) + Y (1 byte) + WIDTH (1 byte) + R (1 byte) + G (1 byte) + B (1 byte)
```

### Text Commands

#### CMD_PRINT (0x08)
Print text at current cursor position.

**Data Format:**
```
TEXT (N bytes, null-terminated)
```

**Example:**
```
0xFF 0x08 0x0B "Hello World"
```
Prints "Hello World".

#### CMD_SET_CURSOR (0x09)
Set text cursor position.

**Data Format:**
```
X (1 byte) + Y (1 byte)
```

### Screen Control Commands

#### CMD_CLEAR (0x0A)
Clear the entire screen.

**Data Format:**
```
(No data)
```

#### CMD_SET_BRIGHTNESS (0x0B)
Set display brightness.

**Data Format:**
```
BRIGHTNESS (1 byte, 0-255)
```

### Image Commands

#### CMD_DRAW_BITMAP (0x0C)
Draw a bitmap image.

**Data Format:**
```
X (1 byte) + Y (1 byte) + WIDTH (1 byte) + HEIGHT (1 byte) + BITMAP_DATA (N bytes)
```

**Bitmap Data Format:**
- RGB565 format (2 bytes per pixel)
- Data sent row by row, left to right
- Flow control: Receiver sends 0xFF every 64 pixels

### Sprite Commands

#### CMD_SET_SPRITE (0x0E)
Set a sprite with image data.

**Data Format:**
```
SPRITE_ID (1 byte) + X (1 byte) + Y (1 byte) + WIDTH (1 byte) + HEIGHT (1 byte) + SPRITE_DATA (N bytes)
```

**Sprite Data Format:**
- RGB565 format (2 bytes per pixel)
- Maximum size: 64x64 pixels (8KB)
- Flow control: Receiver sends 0xFF every 64 pixels

**Example:**
```
0xFF 0x0E 0x05 0x00 0x00 0x08 0x08 [sprite_data...]
```
Sets sprite 0 as an 8x8 image at position (0,0).

#### CMD_CLEAR_SPRITE (0x0F)
Clear a sprite from memory and screen.

**Data Format:**
```
SPRITE_ID (1 byte)
```

#### CMD_DRAW_SPRITE (0x10)
Draw a sprite at a specific location.

**Data Format:**
```
SPRITE_ID (1 byte) + X (1 byte) + Y (1 byte)
```

#### CMD_MOVE_SPRITE (0x11)
Move a sprite to a new location (updates stored position).

**Data Format:**
```
SPRITE_ID (1 byte) + X (1 byte) + Y (1 byte)
```

## Color Formats

### RGB888
Used for input commands:
- R: 8 bits (0-255)
- G: 8 bits (0-255)
- B: 8 bits (0-255)

### RGB565
Used for storage and transmission:
- R: 5 bits (0-31)
- G: 6 bits (0-63)
- B: 5 bits (0-31)

## Flow Control

For large data transfers (bitmaps, sprites), the protocol uses flow control:

1. Sender transmits data in chunks
2. Receiver processes data and sends 0xFF acknowledgment
3. Sender continues with next chunk
4. Prevents buffer overflow

## Error Handling

### Common Error Responses

| Error | Message |
|-------|---------|
| Invalid data length | "Invalid [command] data" |
| Sprite not active | "Sprite not active" |
| Invalid sprite ID | "Invalid sprite ID" |
| Sprite too large | "Sprite too large" |
| Timeout | "[Command] data read timeout" |

### Timeout Values

- Bitmap data: 5 seconds
- Sprite data: 5 seconds
- General commands: Immediate

## Examples

### Complete Session Example

```
# Set brightness
TX: 0xFF 0x0B 0x01 0x80
RX: 0xFF 0xAC 0x0B 0x01 0x0D "Brightness set"

# Clear screen
TX: 0xFF 0x0A 0x00
RX: 0xFF 0xAC 0x0A 0x01 0x0C "Screen cleared"

# Draw a red pixel
TX: 0xFF 0x01 0x05 0x0A 0x0B 0xFF 0x00 0x00
RX: 0xFF 0xAC 0x01 0x01 0x0B "Pixel drawn"

# Set a sprite
TX: 0xFF 0x0E 0x05 0x00 0x00 0x08 0x08 [sprite_data...]
RX: 0xFF 0xAC 0x0E 0x01 0x0A "Sprite set"

# Move sprite
TX: 0xFF 0x11 0x03 0x10 0x10
RX: 0xFF 0xAC 0x11 0x01 0x0B "Sprite moved"
```

## Implementation Notes

### Serial Configuration
- Baud rate: 115200
- Data bits: 8
- Parity: None
- Stop bits: 1
- Flow control: None

### Buffer Management
- Maximum command data: 64 bytes
- Maximum sprite size: 8KB
- Flow control prevents buffer overflow

### Performance Considerations
- Commands are processed immediately
- Large data transfers use flow control
- Sprites are stored in device memory
- Position tracking enables efficient sprite movement 