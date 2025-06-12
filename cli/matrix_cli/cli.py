import serial
import serial.tools.list_ports
import click
from rich.console import Console
from rich.table import Table

console = Console()

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

def get_serial(port):
    """Get a serial connection to the specified port."""
    return serial.Serial(port, 115200, timeout=1)

def send_command(port, cmd, data):
    """Send a command to the matrix display."""
    with get_serial(port) as ser:
        # Send start byte, command, and data length
        ser.write(bytes([START_BYTE, cmd, len(data)]))
        # Send data
        ser.write(data)
        # Wait for any response
        ser.flush()

@click.group()
def cli():
    """Matrix CLI - Control LED matrix displays via serial."""
    pass

@cli.command()
def ports():
    """List available serial ports."""
    ports = serial.tools.list_ports.comports()
    table = Table(title="Available Serial Ports")
    table.add_column("Port", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Hardware ID", style="yellow")
    
    for port in ports:
        table.add_row(port.device, port.description, port.hwid)
    
    console.print(table)

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('brightness', type=click.IntRange(0, 255))
def brightness(port, brightness):
    """Set display brightness (0-255)."""
    send_command(port, CMD_SET_BRIGHTNESS, bytes([brightness]))
    console.print(f"[green]Brightness set to {brightness}")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('text')
def print_text(port, text):
    """Print text at current cursor position."""
    send_command(port, CMD_PRINT, text.encode())
    console.print(f"[green]Printed: {text}")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('x', type=int)
@click.argument('y', type=int)
def cursor(port, x, y):
    """Set cursor position."""
    send_command(port, CMD_SET_CURSOR, bytes([x, y]))
    console.print(f"[green]Cursor set to ({x}, {y})")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('r', type=click.IntRange(0, 255))
@click.argument('g', type=click.IntRange(0, 255))
@click.argument('b', type=click.IntRange(0, 255))
def fill(port, r, g, b):
    """Fill entire screen with color."""
    send_command(port, CMD_FILL_SCREEN, bytes([r, g, b]))
    console.print(f"[green]Screen filled with RGB({r}, {g}, {b})")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('x', type=int)
@click.argument('y', type=int)
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.argument('r', type=click.IntRange(0, 255))
@click.argument('g', type=click.IntRange(0, 255))
@click.argument('b', type=click.IntRange(0, 255))
def rect(port, x, y, width, height, r, g, b):
    """Fill rectangle with color."""
    send_command(port, CMD_FILL_RECT, bytes([x, y, width, height, r, g, b]))
    console.print(f"[green]Rectangle filled at ({x}, {y}) {width}x{height} with RGB({r}, {g}, {b})")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
def clear(port):
    """Clear the screen."""
    send_command(port, CMD_CLEAR, bytes([]))
    console.print("[green]Screen cleared")

def main():
    cli() 