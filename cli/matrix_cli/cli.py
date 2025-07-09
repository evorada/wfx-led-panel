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
@click.option('--port', required=True, help='Serial port (e.g., /dev/ttyUSB0)')
@click.pass_context
def cli(ctx, port):
    """Matrix CLI - Control LED matrix displays via serial."""
    ctx.ensure_object(dict)
    ctx.obj['port'] = port

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
@click.argument('brightness', type=click.IntRange(0, 255))
@click.pass_context
def brightness(ctx, brightness):
    """Set display brightness (0-255)."""
    try:
        matrix = MatrixDisplay(ctx.obj['port'])
        success, message = matrix.set_brightness(brightness)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.argument('text')
@click.pass_context
def print_text(ctx, text):
    """Print text at current cursor position."""
    try:
        matrix = MatrixDisplay(ctx.obj['port'])
        success, message = matrix.print_text(text)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.argument('x', type=int)
@click.argument('y', type=int)
@click.pass_context
def cursor(ctx, x, y):
    """Set cursor position."""
    try:
        matrix = MatrixDisplay(ctx.obj['port'])
        success, message = matrix.set_cursor(x, y)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.argument('r', type=click.IntRange(0, 255))
@click.argument('g', type=click.IntRange(0, 255))
@click.argument('b', type=click.IntRange(0, 255))
@click.pass_context
def fill(ctx, r, g, b):
    """Fill entire screen with color."""
    try:
        matrix = MatrixDisplay(ctx.obj['port'])
        success, message = matrix.fill_screen(r, g, b)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.argument('x', type=int)
@click.argument('y', type=int)
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.argument('r', type=click.IntRange(0, 255))
@click.argument('g', type=click.IntRange(0, 255))
@click.argument('b', type=click.IntRange(0, 255))
@click.pass_context
def rect(ctx, x, y, width, height, r, g, b):
    """Fill rectangle with color."""
    try:
        matrix = MatrixDisplay(ctx.obj['port'])
        success, message = matrix.fill_rect(x, y, width, height, r, g, b)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")

@cli.command()
@click.pass_context
def clear(ctx):
    """Clear the screen."""
    try:
        matrix = MatrixDisplay(ctx.obj['port'])
        success, message = matrix.clear()
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")