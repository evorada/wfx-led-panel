import click
from rich.console import Console
from rich.table import Table
from .matrix import MatrixDisplay
from .image_utils import load_and_process_image, create_test_pattern
from .sprite_test import run_sprite_test
from .sprite_image_example import run_sprite_image_example
from .sprite_animation import run_sprite_animation

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
CMD_DRAW_FAST_VLINE = 0x0B
CMD_DRAW_FAST_HLINE = 0x0C
CMD_DRAW_BITMAP = 0x0D
# Sprite commands
CMD_SET_SPRITE = 0x0E
CMD_CLEAR_SPRITE = 0x0F
CMD_DRAW_SPRITE = 0x10
CMD_MOVE_SPRITE = 0x11


@click.group()
@click.option("--port", required=True, help="Serial port (e.g., /dev/ttyUSB0)")
@click.pass_context
def cli(ctx, port):
    """Matrix CLI - Control LED matrix displays via serial."""
    ctx.ensure_object(dict)
    ctx.obj["port"] = port


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
@click.argument(
    "filename", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option("--x", default=0, help="X position (default: 0)")
@click.option("--y", default=0, help="Y position (default: 0)")
@click.pass_context
def bitmap(ctx, filename, x, y):
    """Display an image file on the matrix display.

    Supports common image formats: PNG, JPG, JPEG, GIF, BMP, etc.
    """
    try:
        # Load and process the image
        console.print(f"[blue]Loading image: {filename}")
        width, height, rgb_data = load_and_process_image(filename)

        # Send to matrix
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_bitmap(x, y, width, height, rgb_data)

        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("pattern", type=click.Choice(["gradient", "rainbow", "checkerboard"]))
@click.option("--x", default=0, help="X position (default: 0)")
@click.option("--y", default=0, help="Y position (default: 0)")
@click.option("--width", default=32, help="Pattern width (default: 32)")
@click.option("--height", default=16, help="Pattern height (default: 16)")
@click.pass_context
def pattern(ctx, pattern, x, y, width, height):
    """Display a test pattern on the matrix display."""
    try:
        # Create test pattern
        console.print(f"[blue]Creating {pattern} pattern: {width}x{height}")
        width, height, rgb_data = create_test_pattern(width, height, pattern)

        # Send to matrix
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_bitmap(x, y, width, height, rgb_data)

        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")

    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.argument("r", type=click.IntRange(0, 255))
@click.argument("g", type=click.IntRange(0, 255))
@click.argument("b", type=click.IntRange(0, 255))
@click.pass_context
def pixel(ctx, x, y, r, g, b):
    """Draw a single pixel at (x, y) with RGB color."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_pixel(x, y, r, g, b)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("x0", type=int)
@click.argument("y0", type=int)
@click.argument("x1", type=int)
@click.argument("y1", type=int)
@click.argument("r", type=click.IntRange(0, 255))
@click.argument("g", type=click.IntRange(0, 255))
@click.argument("b", type=click.IntRange(0, 255))
@click.pass_context
def line(ctx, x0, y0, x1, y1, r, g, b):
    """Draw a line from (x0, y0) to (x1, y1) with RGB color."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_line(x0, y0, x1, y1, r, g, b)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.argument("width", type=int)
@click.argument("height", type=int)
@click.argument("r", type=click.IntRange(0, 255))
@click.argument("g", type=click.IntRange(0, 255))
@click.argument("b", type=click.IntRange(0, 255))
@click.pass_context
def draw_rect(ctx, x, y, width, height, r, g, b):
    """Draw rectangle outline at (x, y) with size width x height and RGB color."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_rect(x, y, width, height, r, g, b)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.argument("height", type=int)
@click.argument("r", type=click.IntRange(0, 255))
@click.argument("g", type=click.IntRange(0, 255))
@click.argument("b", type=click.IntRange(0, 255))
@click.pass_context
def vline(ctx, x, y, height, r, g, b):
    """Draw fast vertical line at x from y to y+height with RGB color."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_fast_vline(x, y, height, r, g, b)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.argument("width", type=int)
@click.argument("r", type=click.IntRange(0, 255))
@click.argument("g", type=click.IntRange(0, 255))
@click.argument("b", type=click.IntRange(0, 255))
@click.pass_context
def hline(ctx, x, y, width, r, g, b):
    """Draw fast horizontal line at y from x to x+width with RGB color."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_fast_hline(x, y, width, r, g, b)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except ValueError as e:
        console.print(f"[red]Error: {e}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("brightness", type=click.IntRange(0, 255))
@click.pass_context
def brightness(ctx, brightness):
    """Set display brightness (0-255)."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
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
@click.argument("text")
@click.pass_context
def print_text(ctx, text):
    """Print text at current cursor position."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.print_text(text)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.pass_context
def cursor(ctx, x, y):
    """Set cursor position."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.set_cursor(x, y)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("r", type=click.IntRange(0, 255))
@click.argument("g", type=click.IntRange(0, 255))
@click.argument("b", type=click.IntRange(0, 255))
@click.pass_context
def fill(ctx, r, g, b):
    """Fill entire screen with color."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
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
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.argument("width", type=int)
@click.argument("height", type=int)
@click.argument("r", type=click.IntRange(0, 255))
@click.argument("g", type=click.IntRange(0, 255))
@click.argument("b", type=click.IntRange(0, 255))
@click.pass_context
def rect(ctx, x, y, width, height, r, g, b):
    """Fill rectangle with color."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
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
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.clear()
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("sprite_id", type=click.IntRange(0, 15))
@click.argument(
    "filename", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option("--x", default=0, help="Initial X position (default: 0)")
@click.option("--y", default=0, help="Initial Y position (default: 0)")
@click.pass_context
def set_sprite(ctx, sprite_id, filename, x, y):
    """Set a sprite with image data from a file.

    Supports common image formats: PNG, JPG, JPEG, GIF, BMP, etc.
    """
    try:
        # Load and process the image
        console.print(f"[blue]Loading sprite image: {filename}")
        img_width, img_height, rgb_data = load_and_process_image(filename)

        # Send to matrix
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.set_sprite(
            sprite_id, x, y, img_width, img_height, rgb_data
        )

        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("sprite_id", type=click.IntRange(0, 15))
@click.pass_context
def clear_sprite(ctx, sprite_id):
    """Clear a sprite from memory and screen."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.clear_sprite(sprite_id)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("sprite_id", type=click.IntRange(0, 15))
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.pass_context
def draw_sprite(ctx, sprite_id, x, y):
    """Draw a sprite at a specific location."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.draw_sprite(sprite_id, x, y)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.argument("sprite_id", type=click.IntRange(0, 15))
@click.argument("x", type=int)
@click.argument("y", type=int)
@click.pass_context
def move_sprite(ctx, sprite_id, x, y):
    """Move a sprite to a new location and update its stored position."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        success, message = matrix.move_sprite(sprite_id, x, y)
        if success:
            console.print(f"[green]✓ {message}")
        else:
            console.print(f"[red]✗ Error: {message}")
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.pass_context
def sprite_test(ctx):
    """Test sprite functionality."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        run_sprite_test(matrix)
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.pass_context
def sprite_image_example(ctx):
    """Test sprite image functionality."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        run_sprite_image_example(matrix)
    except Exception as e:
        console.print(f"[red]Error: {e}")


@cli.command()
@click.pass_context
def sprite_animation(ctx):
    """Test sprite animation functionality."""
    try:
        matrix = MatrixDisplay(ctx.obj["port"])
        run_sprite_animation(matrix)
    except Exception as e:
        console.print(f"[red]Error: {e}")


if __name__ == "__main__":
    cli()
