"""Core functionality for creating colored JPEG images."""

import logging
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


def create_image(
    width: int,
    height: int,
    color_code: str,
    output_dir: str | Path | None = None,
) -> None:
    """Create and save an image with the specified dimensions and color.

    Args:
        width: The width of the image in pixels.
        height: The height of the image in pixels.
        color_code: The HTML color code for the image background.
        output_dir: The directory to save the image. Accepts a string path or
            pathlib.Path. Defaults to "output_files".

    Raises:
        ValueError: If width/height are not positive or color_code is invalid.
    """
    _validate_dimensions(width, height)
    _validate_color_code(color_code)

    output_path = _resolve_output_path(output_dir)
    filename = _generate_filename(color_code)

    image = Image.new("RGB", (width, height), color=color_code)
    _ensure_directory_exists(output_path)

    full_path = output_path / f"{filename}.jpg"
    image.save(full_path)
    logger.info("Image saved to %s", full_path)


def _validate_dimensions(width: int, height: int) -> None:
    """Validate that image dimensions are positive integers."""
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")


def _validate_color_code(color_code: str) -> None:
    """Validate that color code is in proper HTML hex format."""
    if not isinstance(color_code, str) or not color_code.startswith("#"):
        raise ValueError(
            "Color code must be a string in HTML format, starting with '#'."
        )
    if len(color_code) != 7:
        raise ValueError("Color code must be exactly 7 characters (#RRGGBB).")


def _resolve_output_path(output_dir: str | Path | None) -> Path:
    """Convert output directory to Path object with default fallback."""
    if output_dir is None:
        return Path("output_files")
    return Path(output_dir)


def _generate_filename(color_code: str) -> str:
    """Generate filename from color code by removing hash prefix."""
    return color_code.lstrip("#")


def _ensure_directory_exists(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        width = int(input("Enter the width of the image: "))
        height = int(input("Enter the height of the image: "))
        color = input("Enter the color code (in HTML format): ")
        create_image(width, height, color)
    except ValueError as e:
        logger.error("Invalid input: %s", e)
