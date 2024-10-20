import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from recommender import commands
from io import StringIO
from pathlib import Path


def test_csv_input():
    """Testing...."""
    runner = CliRunner()
    result = runner.invoke(
        commands.csv_input,
        ["I do not exist", "I do not exist too"],
        catch_exceptions=False,
    )
    assert result.exit_code != 0


# def test_csv_input_valid():
#     """Test the csv_input command with mocked file inputs."""
#     # Create a mock for the Path object
#     mock_jobseekers_path = MagicMock()
#     mock_jobs_path = MagicMock()

#     # Mock the `open` method to return a StringIO object instead of a file
#     with patch("click.Path.convert") as mock_path_convert:
#         with patch("click.format_filename") as mock_format_filename:
#             # Set the return value to a StringIO object containing our CSV data
#             mock_path_convert.side_effect = MagicMock(spec=Path)
#             mock_format_filename.side_effect = "Wow..."

#             # Call the command with the mocked paths
#             runner = CliRunner()
#             result = runner.invoke(
#                 commands.csv_input, [mock_jobseekers_path, mock_jobs_path]
#             )

#     # Check that the command executed successfully
#     assert result.exit_code == 0
