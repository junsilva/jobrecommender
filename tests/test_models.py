import pytest
from io import StringIO
from unittest.mock import mock_open, patch, MagicMock
from recommender.models import CSVJobInput, CSVJobSeekerInput, JobMatch, JobSeeker, Job


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
def mock_job_seekers_csv():
    """Fixture that provides mock CSV data for job seekers."""
    mock_data = StringIO(
        "id,name,skills\n" '1,Alice,"Python, Java"\n' '2,Bob,"Python, Data Analysis"\n'
    )
    with patch("builtins.open", mock_open(read_data=mock_data.getvalue())):
        yield


@pytest.fixture
def mock_Alice():
    mock = MagicMock(spec=JobSeeker)
    mock.id = 1
    mock.name = "Alice Seeker"
    return mock


@pytest.fixture
def mock_Bob():
    mock = MagicMock(spec=JobSeeker)
    mock.id = 2
    mock.name = "Bob Applicant"
    return mock


@pytest.fixture
def mock_rubydev():
    mock = MagicMock(spec=Job)
    mock.id = 1
    mock.title = "Ruby Developer"
    return mock


@pytest.fixture
def mock_pythondev():
    mock = MagicMock(spec=Job)
    mock.id = 2
    mock.title = "Python Developer"
    return mock


@pytest.fixture
def job_match_cases(mock_Alice, mock_Bob, mock_rubydev, mock_pythondev):
    return {
        "a_pc100_ji1": JobMatch(
            jobseeker=mock_Alice,
            job=mock_rubydev,
            matching_skill_count=10,
            matching_skill_percent=100,
        ),
        "a_pc50_ji1": JobMatch(
            jobseeker=mock_Alice,
            job=mock_rubydev,
            matching_skill_count=10,
            matching_skill_percent=50,
        ),
        "a_pc100_ji2": JobMatch(
            jobseeker=mock_Alice,
            job=mock_pythondev,
            matching_skill_count=10,
            matching_skill_percent=100,
        ),
        "a_pc50_ji2": JobMatch(
            jobseeker=mock_Alice,
            job=mock_pythondev,
            matching_skill_count=10,
            matching_skill_percent=50,
        ),
        "b_pc100_ji1": JobMatch(
            jobseeker=mock_Bob,
            job=mock_rubydev,
            matching_skill_count=10,
            matching_skill_percent=100,
        ),
        "b_pc50_ji1": JobMatch(
            jobseeker=mock_Bob,
            job=mock_rubydev,
            matching_skill_count=10,
            matching_skill_percent=50,
        ),
        "b_pc100_ji2": JobMatch(
            jobseeker=mock_Bob,
            job=mock_pythondev,
            matching_skill_count=10,
            matching_skill_percent=100,
        ),
        "b_pc50_ji2": JobMatch(
            jobseeker=mock_Bob,
            job=mock_pythondev,
            matching_skill_count=10,
            matching_skill_percent=50,
        ),
    }


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


"""
Truth Table 
╔═══════════════════════════════════════════════╤═══════════╤═════════╤═══════╤════════╗
║ Case Identifier                               │ seeker_id │ percent │ job   │ Result ║
╠═══════════════════════════════════════════════╪═══════════╪═════════╪═══════╪════════╣
║ seeker_AeqB_percent_AeqB_job_AltB_then_A_lt_B │ A = B     │ A = B   │ A < B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AeqB_percent_AeqB_job_AgtB_then_A_gt_B │ A = B     │ A = B   │ A > B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AeqB_percent_AltB_job_AltB_then_A_gt_B │ A = B     │ A < B   │ A < B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AeqB_percent_AltB_job_AgtB_then_A_gt_B │ A = B     │ A < B   │ A > B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AeqB_percent_AgtB_job_AltB_then_A_lt_B │ A = B     │ A > B   │ A < B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AeqB_percent_AgtB_job_AgtB_then_A_lt_B │ A = B     │ A > B   │ A > B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AeqB_job_AeqB_then_A_lt_B │ A < B     │ A = B   │ A = B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AeqB_job_AltB_then_A_lt_B │ A < B     │ A = B   │ A < B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AeqB_job_AgtB_then_A_lt_B │ A < B     │ A = B   │ A > B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AltB_job_AeqB_then_A_lt_B │ A < B     │ A < B   │ A = B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AltB_job_AltB_then_A_lt_B │ A < B     │ A < B   │ A < B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AltB_job_AgtB_then_A_lt_B │ A < B     │ A < B   │ A > B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AgtB_job_AeqB_then_A_lt_B │ A < B     │ A > B   │ A = B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AgtB_job_AltB_then_A_lt_B │ A < B     │ A > B   │ A < B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AltB_percent_AgtB_job_AgtB_then_A_lt_B │ A < B     │ A > B   │ A > B │ A < B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AeqB_job_AeqB_then_A_gt_B │ A > B     │ A = B   │ A = B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AeqB_job_AltB_then_A_gt_B │ A > B     │ A = B   │ A < B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AeqB_job_AgtB_then_A_gt_B │ A > B     │ A = B   │ A > B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AltB_job_AeqB_then_A_gt_B │ A > B     │ A < B   │ A = B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AltB_job_AltB_then_A_gt_B │ A > B     │ A < B   │ A < B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AltB_job_AgtB_then_A_gt_B │ A > B     │ A < B   │ A > B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AgtB_job_AeqB_then_A_gt_B │ A > B     │ A > B   │ A = B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AgtB_job_AltB_then_A_gt_B │ A > B     │ A > B   │ A < B │ A > B  ║
╟───────────────────────────────────────────────┼───────────┼─────────┼───────┼────────╢
║ seeker_AgtB_percent_AgtB_job_AgtB_then_A_gt_B │ A > B     │ A > B   │ A > B │ A > B  ║
╚═══════════════════════════════════════════════╧═══════════╧═════════╧═══════╧════════╝
"""


@pytest.mark.parametrize(
    "request_params",
    [
        ("a_pc100_ji1", "a_pc100_ji2", -1),
        ("a_pc100_ji2", "a_pc100_ji1", 1),
        ("a_pc50_ji1", "a_pc100_ji2", 1),
        ("a_pc50_ji2", "a_pc100_ji1", 1),
        ("a_pc100_ji1", "a_pc50_ji2", -1),
        ("a_pc100_ji2", "a_pc50_ji1", -1),
        ("a_pc100_ji1", "b_pc100_ji1", -1),
        ("a_pc100_ji1", "b_pc100_ji2", -1),
        ("a_pc100_ji2", "b_pc100_ji1", -1),
        ("a_pc50_ji1", "b_pc100_ji1", -1),
        ("a_pc50_ji1", "b_pc100_ji2", -1),
        ("a_pc50_ji2", "b_pc100_ji1", -1),
        ("a_pc100_ji1", "b_pc50_ji1", -1),
        ("a_pc100_ji1", "b_pc50_ji2", -1),
        ("a_pc100_ji2", "b_pc50_ji1", -1),
        ("b_pc100_ji1", "a_pc100_ji1", 1),
        ("b_pc100_ji1", "a_pc100_ji2", 1),
        ("b_pc100_ji2", "a_pc100_ji1", 1),
        ("b_pc50_ji1", "a_pc100_ji1", 1),
        ("b_pc50_ji1", "a_pc100_ji2", 1),
        ("b_pc50_ji2", "a_pc100_ji1", 1),
        ("b_pc100_ji1", "a_pc50_ji1", 1),
        ("b_pc100_ji1", "a_pc50_ji2", 1),
        ("b_pc100_ji2", "a_pc50_ji1", 1),
    ],
    ids=[
        "seeker_AeqB_percent_AeqB_job_AltB_then_A_lt_B",
        "seeker_AeqB_percent_AeqB_job_AgtB_then_A_gt_B",
        "seeker_AeqB_percent_AltB_job_AltB_then_A_gt_B",
        "seeker_AeqB_percent_AltB_job_AgtB_then_A_gt_B",
        "seeker_AeqB_percent_AgtB_job_AltB_then_A_lt_B",
        "seeker_AeqB_percent_AgtB_job_AgtB_then_A_lt_B",
        "seeker_AltB_percent_AeqB_job_AeqB_then_A_lt_B",
        "seeker_AltB_percent_AeqB_job_AltB_then_A_lt_B",
        "seeker_AltB_percent_AeqB_job_AgtB_then_A_lt_B",
        "seeker_AltB_percent_AltB_job_AeqB_then_A_lt_B",
        "seeker_AltB_percent_AltB_job_AltB_then_A_lt_B",
        "seeker_AltB_percent_AltB_job_AgtB_then_A_lt_B",
        "seeker_AltB_percent_AgtB_job_AeqB_then_A_lt_B",
        "seeker_AltB_percent_AgtB_job_AltB_then_A_lt_B",
        "seeker_AltB_percent_AgtB_job_AgtB_then_A_lt_B",
        "seeker_AgtB_percent_AeqB_job_AeqB_then_A_gt_B",
        "seeker_AgtB_percent_AeqB_job_AltB_then_A_gt_B",
        "seeker_AgtB_percent_AeqB_job_AgtB_then_A_gt_B",
        "seeker_AgtB_percent_AltB_job_AeqB_then_A_gt_B",
        "seeker_AgtB_percent_AltB_job_AltB_then_A_gt_B",
        "seeker_AgtB_percent_AltB_job_AgtB_then_A_gt_B",
        "seeker_AgtB_percent_AgtB_job_AeqB_then_A_gt_B",
        "seeker_AgtB_percent_AgtB_job_AltB_then_A_gt_B",
        "seeker_AgtB_percent_AgtB_job_AgtB_then_A_gt_B",
    ],
)
def test_job_match_ordering(
    request_params,
    job_match_cases,
):
    job_match_a_key, job_match_b_key, expected = request_params

    job_match_a = job_match_cases[job_match_a_key]
    job_match_b = job_match_cases[job_match_b_key]

    result = (job_match_a > job_match_b) - (job_match_a < job_match_b)
    assert result == expected


def test_job_match_equality(mock_Alice, mock_pythondev):
    match_a = JobMatch(
        jobseeker=mock_Alice,
        job=mock_pythondev,
        matching_skill_count=10,
        matching_skill_percent=100,
    )

    match_b = JobMatch(
        jobseeker=mock_Alice,
        job=mock_pythondev,
        matching_skill_count=50,
        matching_skill_percent=100,
    )

    assert match_a == match_b
