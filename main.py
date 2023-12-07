from PIL import Image
import os
from typing import Tuple, Optional
from pathlib import Path


def create_image(
    width: int, height: int, color_code: str, output_dir: Optional[Path] = None
) -> None:
    """
    Create and save an image with the specified dimensions and color.

    Args:
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        color_code (str): The HTML color code for the image background.
        output_dir (Optional[Path]): The directory to save the image. Defaults to "output_files".

    Returns:
        None
    """
    # Validate input parameters
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")
    if not isinstance(color_code, str) or not color_code.startswith("#"):
        raise ValueError(
            "Color code must be a string in HTML format, starting with '#'."
        )

    # Set the default output directory if not provided
    if output_dir is None:
        output_dir = Path("output_files")

    # Create an image with the given color
    img = Image.new("RGB", (width, height), color=color_code)

    # Check if output directory exists, create if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Remove '#' from the start of the color code for the filename
    filename = color_code.lstrip("#")

    # Save the image
    img.save(output_dir / f"{filename}.jpg")


if __name__ == "__main__":
    try:
        width = int(input("Enter the width of the image: "))
        height = int(input("Enter the height of the image: "))
        color = input("Enter the color code (in HTML format): ")
        create_image(width, height, color)
    except ValueError as e:
        print(f"Error: {e}")
