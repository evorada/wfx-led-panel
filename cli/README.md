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
```

## Commands

- `ports`: List available serial ports
- `brightness`: Set display brightness (0-255)
- `print`: Print text at current cursor position
- `cursor`: Set cursor position
- `fill`: Fill entire screen with color
- `rect`: Fill rectangle with color
- `clear`: Clear the screen 