"""
Matrix display client library for controlling LED matrix displays via serial.
"""

from typing import List, Tuple
import serial
import serial.tools.list_ports


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
    CMD_DRAW_FAST_VLINE = 0x0B
    CMD_DRAW_FAST_HLINE = 0x0C
    CMD_DRAW_BITMAP = 0x0D
    # Sprite commands
    CMD_SET_SPRITE = 0x0E
    CMD_CLEAR_SPRITE = 0x0F
    CMD_DRAW_SPRITE = 0x10
    CMD_MOVE_SPRITE = 0x11

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
                    message = message_bytes.decode("utf-8", errors="ignore")
                else:
                    return False, "Incomplete message received"

            return success, message

        except Exception as e:
            return False, f"Error reading ACK: {str(e)}"

    def _send_command(
        self, cmd: int, data: bytes, payload: bytes = None
    ) -> Tuple[bool, str]:
        """Send a command to the matrix display and wait for acknowledgment.

        Args:
            cmd: Command byte
            data: Command data
            payload: Additional payload to be sent
        Returns:
            Tuple of (success, message)
        """
        with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
            # Send start byte, command
            ser.write(bytes([self.START_BYTE, cmd, len(data)]))
            # Send data
            ser.write(data)
            if payload:
                ser.write(payload)
            # Wait for acknowledgment
            ser.flush()
            return self._wait_for_ack(ser, cmd)

    def _send_bitmap_with_flow_control(
        self, cmd: int, data: bytes, payload: bytes
    ) -> Tuple[bool, str]:
        """Send bitmap command with flow control for large payloads.

        Args:
            cmd: Command byte
            data: Command data (header)
            payload: Bitmap payload data
        Returns:
            Tuple of (success, message)
        """
        with serial.Serial(
            self.port, self.baudrate, timeout=10
        ) as ser:  # Longer timeout for large data
            # Send start byte, command, and header data
            ser.write(bytes([self.START_BYTE, cmd, len(data)]))
            ser.write(data)
            ser.flush()

            # Send payload in chunks with flow control
            chunk_size = 128  # 64 pixels * 2 bytes per pixel
            total_sent = 0

            while total_sent < len(payload):
                # Calculate how much to send in this chunk
                remaining = len(payload) - total_sent
                current_chunk_size = min(chunk_size, remaining)

                # Send the chunk
                chunk = payload[total_sent : total_sent + current_chunk_size]
                ser.write(chunk)
                ser.flush()
                total_sent += current_chunk_size

                # Wait for ready signal (0xFF) if not the last chunk
                if total_sent < len(payload):
                    try:
                        ready_signal = ser.read(1)
                        if not ready_signal or ready_signal[0] != 0xFF:
                            return (
                                False,
                                f"Flow control error: expected 0xFF, got {ready_signal}",
                            )
                    except Exception as e:
                        return False, f"Error reading flow control signal: {str(e)}"

            return self._wait_for_ack(ser, cmd)

    def draw_pixel(self, x: int, y: int, r: int, g: int, b: int) -> Tuple[bool, str]:
        """Draw a single pixel.

        Args:
            x: X coordinate
            y: Y coordinate
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            Tuple of (success, message)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        return self._send_command(self.CMD_DRAW_PIXEL, bytes([x, y, r, g, b]))

    def draw_line(
        self, x0: int, y0: int, x1: int, y1: int, r: int, g: int, b: int
    ) -> Tuple[bool, str]:
        """Draw a line from (x0, y0) to (x1, y1).

        Args:
            x0: Start X coordinate
            y0: Start Y coordinate
            x1: End X coordinate
            y1: End Y coordinate
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            Tuple of (success, message)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        return self._send_command(self.CMD_DRAW_LINE, bytes([x0, y0, x1, y1, r, g, b]))

    def draw_rect(
        self, x: int, y: int, width: int, height: int, r: int, g: int, b: int
    ) -> Tuple[bool, str]:
        """Draw rectangle outline.

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
        return self._send_command(
            self.CMD_DRAW_RECT, bytes([x, y, width, height, r, g, b])
        )

    def draw_fast_vline(
        self, x: int, y: int, height: int, r: int, g: int, b: int
    ) -> Tuple[bool, str]:
        """Draw fast vertical line.

        Args:
            x: X coordinate
            y: Y coordinate
            height: Line height
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            Tuple of (success, message)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        return self._send_command(
            self.CMD_DRAW_FAST_VLINE, bytes([x, y, height, r, g, b])
        )

    def draw_fast_hline(
        self, x: int, y: int, width: int, r: int, g: int, b: int
    ) -> Tuple[bool, str]:
        """Draw fast horizontal line.

        Args:
            x: X coordinate
            y: Y coordinate
            width: Line width
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            Tuple of (success, message)
        """
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color components must be between 0 and 255")
        return self._send_command(
            self.CMD_DRAW_FAST_HLINE, bytes([x, y, width, r, g, b])
        )

    def draw_bitmap(
        self, x: int, y: int, width: int, height: int, bitmap_data: bytes
    ) -> Tuple[bool, str]:
        """Draw bitmap at specified location using RGB565 format.

        Args:
            x: X coordinate
            y: Y coordinate
            width: Bitmap width
            height: Bitmap height
            bitmap_data: RGB888 data for bitmap (width * height * 3 bytes)

        Returns:
            Tuple of (success, message)
        """
        expected_size = width * height * 3
        if len(bitmap_data) != expected_size:
            raise ValueError(
                f"Bitmap data size mismatch. Expected {expected_size} bytes, got {len(bitmap_data)}"
            )

        # Convert RGB888 to RGB565
        data = bytes()
        for i in range(0, len(bitmap_data), 3):
            if i + 2 < len(bitmap_data):
                r, g, b = bitmap_data[i], bitmap_data[i + 1], bitmap_data[i + 2]
                # Convert to RGB565: R(5 bits) + G(6 bits) + B(5 bits)
                r565 = (r >> 3) & 0x1F  # 5 bits
                g565 = (g >> 2) & 0x3F  # 6 bits
                b565 = (b >> 3) & 0x1F  # 5 bits
                color = (r565 << 11) | (g565 << 5) | b565
                color_h = int((color >> 8) & 0xFF)
                color_l = int(color & 0xFF)
                data = data + bytes([int(color_h) & 0xFF, int(color_l) & 0xFF])

        # Use flow control for bitmap data
        return self._send_bitmap_with_flow_control(
            self.CMD_DRAW_BITMAP, bytes([x, y, width, height]), data
        )

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

    def fill_rect(
        self, x: int, y: int, width: int, height: int, r: int, g: int, b: int
    ) -> Tuple[bool, str]:
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
        return self._send_command(
            self.CMD_FILL_RECT, bytes([x, y, width, height, r, g, b])
        )

    def clear(self) -> Tuple[bool, str]:
        """Clear the screen.

        Returns:
            Tuple of (success, message)
        """
        return self._send_command(self.CMD_CLEAR, bytes([]))

    def set_sprite(
        self,
        sprite_id: int,
        x: int,
        y: int,
        width: int,
        height: int,
        bitmap_data: bytes,
    ) -> Tuple[bool, str]:
        """Set a sprite with image data.

        Args:
            sprite_id: Sprite ID (0-15)
            x: Initial X coordinate
            y: Initial Y coordinate
            width: Sprite width
            height: Sprite height
            bitmap_data: RGB888 data for sprite (width * height * 3 bytes)

        Returns:
            Tuple of (success, message)
        """
        if not 0 <= sprite_id <= 15:
            raise ValueError("Sprite ID must be between 0 and 15")

        expected_size = width * height * 3
        if len(bitmap_data) != expected_size:
            raise ValueError(
                f"Bitmap data size mismatch. Expected {expected_size} bytes, got {len(bitmap_data)}"
            )

        # Convert RGB888 to RGB565
        data = bytes()
        for i in range(0, len(bitmap_data), 3):
            if i + 2 < len(bitmap_data):
                r, g, b = bitmap_data[i], bitmap_data[i + 1], bitmap_data[i + 2]
                # Convert to RGB565: R(5 bits) + G(6 bits) + B(5 bits)
                r565 = (r >> 3) & 0x1F  # 5 bits
                g565 = (g >> 2) & 0x3F  # 6 bits
                b565 = (b >> 3) & 0x1F  # 5 bits
                color = (r565 << 11) | (g565 << 5) | b565
                color_h = int((color >> 8) & 0xFF)
                color_l = int(color & 0xFF)
                data = data + bytes([int(color_h) & 0xFF, int(color_l) & 0xFF])

        # Use flow control for sprite data
        return self._send_bitmap_with_flow_control(
            self.CMD_SET_SPRITE, bytes([sprite_id, x, y, width, height]), data
        )

    def clear_sprite(self, sprite_id: int) -> Tuple[bool, str]:
        """Clear a sprite from memory and screen.

        Args:
            sprite_id: Sprite ID (0-15)

        Returns:
            Tuple of (success, message)
        """
        if not 0 <= sprite_id <= 15:
            raise ValueError("Sprite ID must be between 0 and 15")
        return self._send_command(self.CMD_CLEAR_SPRITE, bytes([sprite_id]))

    def draw_sprite(self, sprite_id: int, x: int, y: int) -> Tuple[bool, str]:
        """Draw a sprite at a specific location.

        Args:
            sprite_id: Sprite ID (0-15)
            x: X coordinate
            y: Y coordinate

        Returns:
            Tuple of (success, message)
        """
        if not 0 <= sprite_id <= 15:
            raise ValueError("Sprite ID must be between 0 and 15")
        return self._send_command(self.CMD_DRAW_SPRITE, bytes([sprite_id, x, y]))

    def move_sprite(self, sprite_id: int, x: int, y: int) -> Tuple[bool, str]:
        """Move a sprite to a new location and update its stored position.

        Args:
            sprite_id: Sprite ID (0-15)
            x: New X coordinate
            y: New Y coordinate

        Returns:
            Tuple of (success, message)
        """
        if not 0 <= sprite_id <= 15:
            raise ValueError("Sprite ID must be between 0 and 15")
        return self._send_command(self.CMD_MOVE_SPRITE, bytes([sprite_id, x, y]))

    @staticmethod
    def list_ports() -> List[Tuple[str, str, str]]:
        """List available serial ports.

        Returns:
            List of tuples containing (port, description, hardware_id)
        """
        return [
            (p.device, p.description, p.hwid)
            for p in serial.tools.list_ports.comports()
        ]
