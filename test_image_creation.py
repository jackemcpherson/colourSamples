import pytest
from PIL import Image
from main import create_image
from pathlib import Path


def test_successful_image_creation(tmp_path: Path) -> None:
    """
    Test that an image is successfully created with valid input parameters.

    Args:
        tmp_path (Path): A pytest fixture providing a temporary directory unique to the test invocation.

    Returns:
        None
    """
    width, height, color_code = 100, 100, "#FF5733"
    output_dir = tmp_path / "output_files"
    create_image(width, height, color_code, output_dir)
    assert (output_dir / "FF5733.jpg").exists()


def test_invalid_width_height() -> None:
    """
    Test that a ValueError is raised when provided with invalid width or height.

    Args:
        None

    Returns:
        None
    """
    with pytest.raises(ValueError) as excinfo:
        create_image(0, 100, "#FF5733")
    assert "positive integers" in str(excinfo.value)


def test_invalid_color_code() -> None:
    """
    Test that a ValueError is raised when provided with an invalid color code format.

    Args:
        None

    Returns:
        None
    """
    with pytest.raises(ValueError) as excinfo:
        create_image(100, 100, "FF5733")
    assert "HTML format" in str(excinfo.value)


def test_output_directory_creation(tmp_path: Path) -> None:
    """
    Test that the output directory is created if it does not exist.

    Args:
        tmp_path (Path): A pytest fixture providing a temporary directory unique to the test invocation.

    Returns:
        None
    """
    width, height, color_code = 100, 100, "#FF5733"
    output_dir = tmp_path / "output_files"
    create_image(width, height, color_code, output_dir)
    assert output_dir.exists()
