"""Command-line interface for coloursamples using typer."""

import logging
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt

from .core import create_image

logger = logging.getLogger(__name__)

app = typer.Typer(
    name="coloursamples",
    help="Generate JPEG images with specified dimensions and colors.",
    no_args_is_help=True,
)
console = Console()


def _setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level.

    Args:
        verbose: Enable debug level logging if True, info level otherwise.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger.info("Logging configured with level: %s", logging.getLevelName(level))


def _validate_color_format(color: str) -> str:
    """Validate and normalize color code format.

    Args:
        color: Raw color code input from user.

    Returns:
        Normalized color code in uppercase with # prefix.

    Raises:
        typer.BadParameter: If color format is invalid.
    """
    if not color.startswith("#"):
        color = f"#{color}"

    if len(color) != 7:
        raise typer.BadParameter(
            f"Color code must be 6 hex characters (got {len(color) - 1}). "
            f"Example: #FF5733 or FF5733"
        )

    try:
        int(color[1:], 16)
    except ValueError as e:
        raise typer.BadParameter(
            f"Invalid hex color code: {color}. "
            f"Must contain only hex digits (0-9, A-F). Example: #FF5733"
        ) from e

    return color.upper()


def _interactive_mode() -> tuple[int, int, str]:
    """Run interactive mode to collect user input.

    Returns:
        Tuple of (width, height, color) from user input.
    """
    console.print(Panel.fit(
        "[bold cyan]Interactive Image Creator[/bold cyan]\n"
        "Enter image dimensions and color",
        border_style="cyan"
    ))

    width = IntPrompt.ask(
        "[bold]Image width[/bold] (pixels)",
        default=800,
        show_default=True
    )
    height = IntPrompt.ask(
        "[bold]Image height[/bold] (pixels)",
        default=600,
        show_default=True
    )

    color = Prompt.ask(
        "[bold]Color code[/bold] (hex format)",
        default="#3498db",
        show_default=True
    )

    return width, height, color


def _validate_input_parameters(width: int, height: int) -> None:
    """Validate that input parameters are within acceptable ranges.

    Args:
        width: Image width in pixels.
        height: Image height in pixels.

    Raises:
        typer.BadParameter: If width or height are outside valid range.
    """
    if width <= 0 or width > 10000:
        raise typer.BadParameter("Width must be between 1 and 10000 pixels")
    if height <= 0 or height > 10000:
        raise typer.BadParameter("Height must be between 1 and 10000 pixels")


def _handle_input_collection(
    interactive: bool, width: int | None, height: int | None, color: str | None
) -> tuple[int, int, str]:
    """Handle input collection from arguments or interactive mode.

    Args:
        interactive: Whether to force interactive mode.
        width: Width from command line arguments or None.
        height: Height from command line arguments or None.
        color: Color from command line arguments or None.

    Returns:
        Tuple of (width, height, color) from arguments or interactive input.
    """
    if interactive or not all([width, height, color]):
        if not interactive and (width or height or color):
            console.print(
                "[yellow]Warning:[/yellow] Some arguments provided but not all. "
                "Use --interactive or provide all three arguments.",
                style="yellow"
            )
        return _interactive_mode()
    return width, height, color


def _create_and_save_image(
    width: int, height: int, color: str, output_dir: Path | None
) -> None:
    """Create and save the image with status indicator.

    Args:
        width: Image width in pixels.
        height: Image height in pixels.
        color: Normalized color code with # prefix.
        output_dir: Directory to save image or None for default.
    """
    with console.status(f"[bold green]Creating {width}x{height} image..."):
        create_image(width, height, color, output_dir)


def _display_success_message(
    width: int, height: int, color: str, output_dir: Path | None
) -> None:
    """Display formatted success message with image details.

    Args:
        width: Image width in pixels.
        height: Image height in pixels.
        color: Normalized color code with # prefix.
        output_dir: Directory where image was saved or None for default.
    """
    output_path = output_dir or Path("output_files")
    filename = color.lstrip("#") + ".jpg"
    full_path = output_path / filename

    console.print(Panel.fit(
        f"[bold green]✓ Image created successfully![/bold green]\n\n"
        f"[bold]Dimensions:[/bold] {width}x{height} pixels\n"
        f"[bold]Color:[/bold] {color}\n"
        f"[bold]Saved to:[/bold] {full_path}",
        border_style="green",
        title="Success"
    ))


@app.command()
def create(
    width: Annotated[int | None, typer.Argument(
        help="Width of the image in pixels (1-10000)"
    )] = None,
    height: Annotated[int | None, typer.Argument(
        help="Height of the image in pixels (1-10000)"
    )] = None,
    color: Annotated[str | None, typer.Argument(
        help="Hex color code (e.g., #FF5733 or FF5733)"
    )] = None,
    output_dir: Annotated[Path | None, typer.Option(
        "--output-dir", "-o",
        help="Directory to save the image (default: output_files)"
    )] = None,
    interactive: Annotated[bool, typer.Option(
        "--interactive", "-i",
        help="Run in interactive mode with prompts"
    )] = False,
    verbose: Annotated[bool, typer.Option(
        "--verbose", "-v",
        help="Enable verbose logging"
    )] = False,
) -> None:
    """Create a JPEG image with specified dimensions and color.

    Args:
        width: Width of the image in pixels (1-10000) or None for interactive.
        height: Height of the image in pixels (1-10000) or None for interactive.
        color: Hex color code (e.g., #FF5733) or None for interactive.
        output_dir: Directory to save the image or None for default.
        interactive: Force interactive mode with prompts.
        verbose: Enable verbose logging output.

    Raises:
        typer.Exit: If any validation fails or image creation errors occur.

    Examples:
        coloursamples create 800 600 "#FF5733"
        coloursamples create 400 300 "3498db" --output-dir ./images
        coloursamples create --interactive
    """
    _setup_logging(verbose)

    try:
        width, height, color = _handle_input_collection(
            interactive, width, height, color
        )
        _validate_input_parameters(width, height)

        normalized_color = _validate_color_format(color)
        _create_and_save_image(width, height, normalized_color, output_dir)
        _display_success_message(width, height, normalized_color, output_dir)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="red")
        raise typer.Exit(1) from e


@app.command()
def info() -> None:
    """Display information about the coloursamples tool."""
    console.print(Panel.fit(
        "[bold cyan]Colour Samples[/bold cyan] v0.1.0\n\n"
        "A Python utility for generating JPEG images with specified "
        "dimensions and colors.\n\n"
        "[bold]Repository:[/bold] https://github.com/jackemcpherson/colourSamples\n"
        "[bold]Documentation:[/bold] See README.md for detailed usage",
        border_style="cyan",
        title="Info"
    ))


def main() -> None:
    """Entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()

