import pytest
from io import StringIO
from unittest.mock import mock_open, patch
from recommender.input import CSVJobInput, CSVJobSeekerInput


@pytest.fixture
def mock_jobs_csv():
    """Fixture that provides mock CSV data for jobs."""
    mock_data = StringIO(
        "id,title,required_skills\n"
        '1,Software Engineer,"Python,Java"\n'
        '2,Data Scientist,"Python,Machine Learning"\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_jobs_csv_not_unique():
    """Fixture that provides mock CSV data for jobs."""
    mock_data = StringIO(
        "id,title,required_skills\n"
        '1,Software Engineer,"Python,Java"\n'
        '2,Data Scientist,"Python,Machine Learning"\n'
        '3,Data Scientist,"Python,Machine Learning"\n'
        '2,Data Scientist,"Python,Machine Learning"\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_jobs_csv_invalid_schema_type():
    """Fixture that provides mock CSV data for jobs."""
    mock_data = StringIO(
        "id,title,required_skills\n"
        '1,Software Engineer,"Python,Java"\n'
        '2,Data Scientist,"Python,Machine Learning"\n'
        '3,Data Scientist,"Python,Machine Learning"\n'
        'A,Data Scientist,"Python,Machine Learning"\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_jobs_csv_invalid_schema_title():
    """Fixture that provides mock CSV data for jobs."""
    mock_data = StringIO(
        "XX,title,required_skills\n"
        '1,Software Engineer,"Python,Java"\n'
        '2,Data Scientist,"Python,Machine Learning"\n'
        '3,Data Scientist,"Python,Machine Learning"\n'
        '2,Data Scientist,"Python,Machine Learning"\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_job_seekers_csv():
    """Fixture that provides mock CSV data for job seekers."""
    mock_data = StringIO(
        "id,name,skills\n" '1,Alice,"Python, Java"\n' '2,Bob,"Python, Data Analysis"\n'
    )
    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_job_seekers_csv_not_unique():
    """Fixture that provides mock CSV data for job seekers."""
    mock_data = StringIO(
        "id,name,skills\n"
        '1,Alice,"Python, Java"\n'
        '2,Bob,"Python, Data Analysis"\n'
        '3,Bob,"Python, Data Analysis"\n'
        '4,Bob,"Python, Data Analysis"\n'
        '2,Bob,"Python, Data Analysis"\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_job_seekers_csv_invalid_schema_type():
    """Fixture that provides mock CSV data for job seekers."""
    mock_data = StringIO(
        "id,name,skills\n"
        '1,Alice,"Python, Java"\n'
        '2,Bob,"Python, Data Analysis"\n'
        '3,Bob,"Python, Data Analysis"\n'
        '4,Bob,"Python, Data Analysis"\n'
        'A,Bob,"Python, Data Analysis"\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_job_seekers_csv_invalid_schema_title():
    """Fixture that provides mock CSV data for job seekers."""
    mock_data = StringIO(
        "XX,name,skills\n"
        '1,Alice,"Python, Java"\n'
        '2,Bob,"Python, Data Analysis"\n'
        '3,Bob,"Python, Data Analysis"\n'
        '4,Bob,"Python, Data Analysis"\n'
        '2,Bob,"Python, Data Analysis"\n'
    )

    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


def test_job_creation(mock_jobs_csv):
    """Test job creation from mocked CSV data."""
    job_input = CSVJobInput("mock_jobs.csv")  # File name can be anything
    jobs = list(job_input.get_jobs())

    assert len(jobs) == 2

    assert jobs[0].id == 1
    assert jobs[0].title == "Software Engineer"
    assert jobs[0].required_skills == {"PYTHON", "JAVA"}

    assert jobs[1].id == 2
    assert jobs[1].title == "Data Scientist"
    assert jobs[1].required_skills == {"PYTHON", "MACHINE LEARNING"}


def test_job_creation_not_unique_id(mock_jobs_csv_not_unique):
    """Error path test job creation."""

    with pytest.raises(ValueError) as excinfo:
        job_input = CSVJobInput("mock_jobs_csv_not_unique.csv")
        list(job_input.get_jobs())

    error_message = str(excinfo.value)
    assert "Duplicate row ID found" in error_message


def test_job_creation_invalid_schema_type(mock_jobs_csv_invalid_schema_type):
    """Error path test job creation."""

    with pytest.raises(ValueError) as excinfo:
        job_input = CSVJobInput("mock_jobs_csv_invalid_schema_type.csv")
        list(job_input.get_jobs())

    assert "ValueError" in str(excinfo.typename)


def test_job_creation_invalid_schema_title(mock_jobs_csv_invalid_schema_title):
    """Error path test job creation."""

    with pytest.raises(KeyError) as excinfo:
        job_input = CSVJobInput("mock_jobs_csv_not_unique.csv")
        list(job_input.get_jobs())

    assert "KeyError" in str(excinfo.typename)


def test_job_seekers_creation_invalid_schema_title(
    mock_job_seekers_csv_invalid_schema_title,
):
    """Error path test job creation."""

    with pytest.raises(KeyError) as excinfo:
        jobseeker_input = CSVJobSeekerInput(
            "mock_job_seekers_csv_invalid_schema_title.csv"
        )
        list(jobseeker_input.get_job_seekers())

    assert "KeyError" in str(excinfo.typename)


def test_job_seekers_creation_invalid_schema_type(
    mock_job_seekers_csv_invalid_schema_type,
):
    """Error path test job creation."""

    with pytest.raises(ValueError) as excinfo:
        jobseeker_input = CSVJobSeekerInput(
            "mock_job_seekers_csv_invalid_schema_type.csv"
        )
        list(jobseeker_input.get_job_seekers())

    assert "ValueError" in str(excinfo.typename)


def test_job_seekers_creation_not_unique_id(mock_job_seekers_csv_not_unique):
    """Error path test job seeker creation."""

    with pytest.raises(ValueError) as excinfo:
        jobseeker_input = CSVJobSeekerInput("mock_job_seekers_csv_not_unique.csv")
        list(jobseeker_input.get_job_seekers())

    assert "Duplicate row ID found" == str(excinfo.value)


def test_job_seekers_creation(mock_job_seekers_csv):
    """Test job seeker creation from mocked CSV data."""
    seeker_input = CSVJobSeekerInput(
        "mock_job_seekers.csv"
    )  # File name can be anything
    job_seekers = list(seeker_input.get_job_seekers())

    assert len(job_seekers) == 2

    assert job_seekers[0].id == 1
    assert job_seekers[0].name == "Alice"
    assert job_seekers[0].skills == {"PYTHON", "JAVA"}

    assert job_seekers[1].id == 2
    assert job_seekers[1].name == "Bob"
    assert job_seekers[1].skills == {"PYTHON", "DATA ANALYSIS"}
