from pathlib import Path

import pytest
from PIL import Image

from coloursamples.core import create_image


def test_successful_image_creation(tmp_path: Path) -> None:
    """Test successful image creation with valid parameters."""
    width, height, colour_code = 100, 100, "#FF5733"
    output_dir = tmp_path / "output_files"
    create_image(width, height, colour_code, output_dir)
    img_path = output_dir / "FF5733.jpg"
    assert img_path.exists()
    img = Image.open(img_path)
    assert img.size == (width, height)
    assert img.getpixel((0, 0)) == (
        int(colour_code[1:3], 16),
        int(colour_code[3:5], 16),
        int(colour_code[5:7], 16),
    )


def test_invalid_width_height() -> None:
    """Test that ValueError is raised for non-positive dimensions."""
    with pytest.raises(ValueError) as excinfo:
        create_image(0, 100, "#FF5733")
    assert "positive integers" in str(excinfo.value)


def test_invalid_colour_code() -> None:
    """Test that ValueError is raised for invalid colour code format."""
    with pytest.raises(ValueError) as excinfo:
        create_image(100, 100, "FF5733")
    assert "HTML format" in str(excinfo.value)


def test_output_directory_creation(tmp_path: Path) -> None:
    """Test that output directory is created when it doesn't exist."""
    width, height, colour_code = 100, 100, "#FF5733"
    output_dir = tmp_path / "output_files"
    create_image(width, height, colour_code, output_dir)
    assert output_dir.exists()


def test_string_output_dir(tmp_path: Path) -> None:
    """Ensure create_image works when output_dir is provided as a string."""
    width, height, colour_code = 50, 50, "#00FF00"
    output_dir = tmp_path / "string_output"
    create_image(width, height, colour_code, str(output_dir))
    assert (output_dir / "00FF00.jpg").exists()


def test_invalid_colour_code_length() -> None:
    """Test that ValueError is raised for incorrect colour code length."""
    with pytest.raises(ValueError) as excinfo:
        create_image(100, 100, "#FF")
    assert "exactly 7 characters" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        create_image(100, 100, "#FFAABBCC")
    assert "exactly 7 characters" in str(excinfo.value)
