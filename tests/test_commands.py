import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from recommender import commands
from recommender import logging_config

# from io import StringIO
from pathlib import Path


@pytest.fixture(autouse=True)
def setup_logging():
    logging_config.configure_logging()


def test_csv_input_error_expected():
    runner = CliRunner()
    result = runner.invoke(
        commands.csv_input,
        ["non_existent_file", "non_existent_file"],
        catch_exceptions=False,
    )
    assert result.exit_code != 0


@patch("click.Path.convert")
def test_csv_input_terminal_output(mock_path_convert):
    """Test the csv_input command with mocked file inputs."""
    # Create a mock for the Path object
    mock_jobseekers_path = MagicMock()
    mock_jobs_path = MagicMock()

    mock_path_convert.return_value = MagicMock(spec=Path)

    with patch("recommender.services.InMemoryRecommenderService.execute") as r_service:
        r_service.return_value = iter(
            [
                "jobseeker_id,jobseeker_name,job_id,job_title,matching_skill_count,matching_skill_percent",
                "1,Alice Seeker,1,Ruby Developer,3,100",
            ]
        )
        # Call the command with the mocked paths
        runner = CliRunner()
        result = runner.invoke(
            commands.csv_input, [mock_jobseekers_path, mock_jobs_path]
        )

    # Check that the command executed successfully
    assert result.exit_code == 0
    assert result.output == (
        "jobseeker_id,jobseeker_name,job_id,job_title,matching_skill_count,matching_skill_percent\n"
        "1,Alice Seeker,1,Ruby Developer,3,100\n"
    )


@patch("click.Path.convert")
def test_csv_input_terminal_output_limit_reached(mock_path_convert):
    """Test the csv_input command with mocked file inputs."""
    # Create a mock for the Path object
    mock_jobseekers_path = MagicMock()
    mock_jobs_path = MagicMock()

    mock_path_convert.return_value = MagicMock(spec=Path)

    with patch("recommender.services.InMemoryRecommenderService.execute") as r_service:
        r_service.return_value = iter(
            [
                "jobseeker_id,jobseeker_name,job_id,job_title,matching_skill_count,matching_skill_percent",
                "1,Alice Seeker,1,Ruby Developer,3,100",
                "1,Alice Seeker,3,Backend Developer,2,50",
                "1,Alice Seeker,9,Python Developer,2,50",
                "1,Alice Seeker,19,Python Developer,2,50",
                "1,Alice Seeker,29,Python Developer,2,50",
                "1,Alice Seeker,119,Python Developer,2,50",
                "1,Alice Seeker,46,Python Developer,2,50",
            ]
        )
        # Call the command with the mocked paths
        runner = CliRunner()
        result = runner.invoke(
            commands.csv_input,
            [mock_jobseekers_path, mock_jobs_path, "--output_limit", "2"],
        )

    # Check that the command executed successfully
    assert result.exit_code == 0
    assert result.output == (
        "jobseeker_id,jobseeker_name,job_id,job_title,matching_skill_count,matching_skill_percent\n"
        "1,Alice Seeker,1,Ruby Developer,3,100\n"
        "1,Alice Seeker,3,Backend Developer,2,50\n"
        "Warning, result count greater than configured limit. "
        "Output to file to view the rest of the results.\n"
    )


@patch("click.Path.convert")
@patch("click.File")
def test_csv_input_file_output(mock_path_convert, mock_file):
    """Test the csv_input command with mocked file inputs."""
    # Create a mock for the Path object
    mock_jobseekers_path = MagicMock()
    mock_jobs_path = MagicMock()

    # Create a mock for the output file
    mock_output_file = MagicMock()

    # Set up the click.File mock to behave like a context manager
    mock_file.return_value.__enter__.return_value = mock_output_file
    mock_file.return_value.__exit__.return_value = None

    with patch("recommender.services.InMemoryRecommenderService.execute") as r_service:
        r_service.return_value = iter(
            [
                "jobseeker_id,jobseeker_name,job_id,job_title,matching_skill_count,matching_skill_percent",
                "1,Alice Seeker,1,Ruby Developer,3,100",
            ]
        )
        # Call the command with the mocked paths
        runner = CliRunner()
        result = runner.invoke(
            commands.csv_input,
            [mock_jobseekers_path, mock_jobs_path, "--output", "mock_output.csv"],
        )

    # Check that the command executed successfully
    assert result.exit_code == 0

    # TODO:
    # research how to track the actual writes and add to checks
