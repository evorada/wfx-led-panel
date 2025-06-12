"""
Matrix display client library for controlling LED matrix displays via serial.
"""

import serial
import serial.tools.list_ports
from typing import List, Tuple, Optional

class MatrixDisplay:
    """Client for controlling LED matrix displays via serial."""
    
    # Command bytes
    START_BYTE = 0xAA
    CMD_DRAW_PIXEL = 0x01
    CMD_FILL_SCREEN = 0x02
    CMD_DRAW_LINE = 0x03
    CMD_DRAW_RECT = 0x04
    CMD_DRAW_TEXT = 0x05
    CMD_CLEAR = 0x06
    CMD_SET_BRIGHTNESS = 0x07
    CMD_PRINT = 0x08
    CMD_SET_CURSOR = 0x09
    CMD_FILL_RECT = 0x0A

    def __init__(self, port: str, baudrate: int = 115200):
        """Initialize the matrix display client.
        
        Args:
            port: Serial port (e.g., '/dev/ttyUSB0')
            baudrate: Serial baudrate (default: 115200)
        """
        self.port = port
        self.baudrate = baudrate

    def _send_command(self, cmd: int, data: bytes) -> None:
        """Send a command to the matrix display.
        
        Args:
            cmd: Command byte
            data: Command data
        """
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            # Send start byte, command, and data length
            ser.write(bytes([self.START_BYTE, cmd, len(data)]))
            # Send data
            ser.write(data)
            # Wait for any response
            ser.flush()

    def set_brightness(self, brightness: int) -> None:
        """Set display brightness.
        
        Args:
            brightness: Brightness value (0-255)
        """
        if not 0 <= brightness <= 255:
            raise ValueError("Brightness must be between 0 and 255")
        self._send_command(self.CMD_SET_BRIGHTNESS, bytes([brightness]))

    def print_text(self, text: str) -> None:
        """Print text at current cursor position.
        
        Args:
            text: Text to print
        """
        self._send_command(self.CMD_PRINT, text.encode())

    def set_cursor(self, x: int, y: int) -> None:
        """Set cursor position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self._send_command(self.CMD_SET_CURSOR, bytes([x, y]))

    def fill_screen(self, r: int, g: int, b: int) -> None:
        """Fill entire screen with color.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        self._send_command(self.CMD_FILL_SCREEN, bytes([r, g, b]))

    def fill_rect(self, x: int, y: int, width: int, height: int, r: int, g: int, b: int) -> None:
        """Fill rectangle with color.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Rectangle width
            height: Rectangle height
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        self._send_command(self.CMD_FILL_RECT, bytes([x, y, width, height, r, g, b]))

    def clear(self) -> None:
        """Clear the screen."""
        self._send_command(self.CMD_CLEAR, bytes([]))

    @staticmethod
    def list_ports() -> List[Tuple[str, str, str]]:
        """List available serial ports.
        
        Returns:
            List of tuples containing (port, description, hardware_id)
        """
        return [(p.device, p.description, p.hwid) for p in serial.tools.list_ports.comports()] 