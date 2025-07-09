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
    ACK_BYTE = 0xAC
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

    def _wait_for_ack(self, ser: serial.Serial, expected_cmd: int) -> Tuple[bool, str]:
        """Wait for and parse acknowledgment response.
        
        Args:
            ser: Serial connection
            expected_cmd: Expected command that was sent
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Wait for start byte
            if ser.read(1) != bytes([self.START_BYTE]):
                return False, "Invalid response start byte"
            
            # Check for ACK byte
            if ser.read(1) != bytes([self.ACK_BYTE]):
                return False, "Invalid ACK byte"
            
            # Read command byte
            cmd_bytes = ser.read(1)
            if not cmd_bytes:
                return False, "No command byte received"
            cmd = cmd_bytes[0]
            
            # Read success byte
            success_bytes = ser.read(1)
            if not success_bytes:
                return False, "No success byte received"
            success = success_bytes[0] == 0x01
            
            # Read message length
            msg_len_bytes = ser.read(1)
            if not msg_len_bytes:
                return False, "No message length received"
            msg_len = msg_len_bytes[0]
            
            # Read message if present
            message = ""
            if msg_len > 0:
                message_bytes = ser.read(msg_len)
                if len(message_bytes) == msg_len:
                    message = message_bytes.decode('utf-8', errors='ignore')
                else:
                    return False, "Incomplete message received"
            
            return success, message
            
        except Exception as e:
            return False, f"Error reading ACK: {str(e)}"

    def _send_command(self, cmd: int, data: bytes) -> Tuple[bool, str]:
        """Send a command to the matrix display and wait for acknowledgment.
        
        Args:
            cmd: Command byte
            data: Command data
            
        Returns:
            Tuple of (success, message)
        """
        with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
            # Send start byte, command, and data length
            ser.write(bytes([self.START_BYTE, cmd, len(data)]))
            # Send data
            ser.write(data)
            # Wait for acknowledgment
            ser.flush()
            return self._wait_for_ack(ser, cmd)

    def set_brightness(self, brightness: int) -> Tuple[bool, str]:
        """Set display brightness.
        
        Args:
            brightness: Brightness value (0-255)
            
        Returns:
            Tuple of (success, message)
        """
        if not 0 <= brightness <= 255:
            raise ValueError("Brightness must be between 0 and 255")
        return self._send_command(self.CMD_SET_BRIGHTNESS, bytes([brightness]))

    def print_text(self, text: str) -> Tuple[bool, str]:
        """Print text at current cursor position.
        
        Args:
            text: Text to print
            
        Returns:
            Tuple of (success, message)
        """
        return self._send_command(self.CMD_PRINT, text.encode())

    def set_cursor(self, x: int, y: int) -> Tuple[bool, str]:
        """Set cursor position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple of (success, message)
        """
        return self._send_command(self.CMD_SET_CURSOR, bytes([x, y]))

    def fill_screen(self, r: int, g: int, b: int) -> Tuple[bool, str]:
        """Fill entire screen with color.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            
        Returns:
            Tuple of (success, message)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        return self._send_command(self.CMD_FILL_SCREEN, bytes([r, g, b]))

    def fill_rect(self, x: int, y: int, width: int, height: int, r: int, g: int, b: int) -> Tuple[bool, str]:
        """Fill rectangle with color.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Rectangle width
            height: Rectangle height
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            
        Returns:
            Tuple of (success, message)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        return self._send_command(self.CMD_FILL_RECT, bytes([x, y, width, height, r, g, b]))

    def clear(self) -> Tuple[bool, str]:
        """Clear the screen.
        
        Returns:
            Tuple of (success, message)
        """
        return self._send_command(self.CMD_CLEAR, bytes([]))

    @staticmethod
    def list_ports() -> List[Tuple[str, str, str]]:
        """List available serial ports.
        
        Returns:
            List of tuples containing (port, description, hardware_id)
        """
        return [(p.device, p.description, p.hwid) for p in serial.tools.list_ports.comports()] 