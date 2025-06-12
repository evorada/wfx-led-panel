import click
from rich.console import Console
from rich.table import Table
from .matrix import MatrixDisplay

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

@click.group()
def cli():
    """Matrix CLI - Control LED matrix displays via serial."""
    pass

@cli.command()
def ports():
    """List available serial ports."""
    ports = MatrixDisplay.list_ports()
    table = Table(title="Available Serial Ports")
    table.add_column("Port", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Hardware ID", style="yellow")
    
    for port, desc, hwid in ports:
        table.add_row(port, desc, hwid)
    
    console.print(table)

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('brightness', type=click.IntRange(0, 255))
def brightness(port, brightness):
    """Set display brightness (0-255)."""
    try:
        matrix = MatrixDisplay(port)
        matrix.set_brightness(brightness)
        console.print(f"[green]Brightness set to {brightness}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('text')
def print_text(port, text):
    """Print text at current cursor position."""
    try:
        matrix = MatrixDisplay(port)
        matrix.print_text(text)
        console.print(f"[green]Printed: {text}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('x', type=int)
@click.argument('y', type=int)
def cursor(port, x, y):
    """Set cursor position."""
    try:
        matrix = MatrixDisplay(port)
        matrix.set_cursor(x, y)
        console.print(f"[green]Cursor set to ({x}, {y})")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.argument('r', type=click.IntRange(0, 255))
@click.argument('g', type=click.IntRange(0, 255))
@click.argument('b', type=click.IntRange(0, 255))
def fill(port, r, g, b):
    """Fill entire screen with color."""
    try:
        matrix = MatrixDisplay(port)
        matrix.fill_screen(r, g, b)
        console.print(f"[green]Screen filled with RGB({r}, {g}, {b})")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

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
    try:
        matrix = MatrixDisplay(port)
        matrix.fill_rect(x, y, width, height, r, g, b)
        console.print(f"[green]Rectangle filled at ({x}, {y}) {width}x{height} with RGB({r}, {g}, {b})")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
def clear(port):
    """Clear the screen."""
    try:
        matrix = MatrixDisplay(port)
        matrix.clear()
        console.print("[green]Screen cleared")
    except Exception as e:
        console.print(f"[red]Error: {e}")

def main():
    cli() 