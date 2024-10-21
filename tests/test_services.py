import pytest
from recommender.services import (
    InMemoryRecommenderService,
    format_job_matches_as_csv,
)
import csv
from io import StringIO
from recommender.models import Job, JobSeeker


# Sample data
class MockJobInput:
    def __init__(self, jobs):
        self._jobs = jobs

    def get_jobs(self):
        return iter(self._jobs)


class MockJobSeekerInput:
    def __init__(self, job_seekers):
        self._job_seekers = job_seekers

    def get_job_seekers(self):
        return iter(self._job_seekers)


csv_jobs_raw = [
    "id,title,required_skills",
    '1,Ruby Developer,"Ruby, SQL, Problem Solving"',
    '2,Frontend Developer,"JavaScript, HTML/CSS, React, Teamwork"',
    '3,Backend Developer,"Java, SQL, Node.js, Problem Solving"',
    '4,Fullstack Developer,"JavaScript, HTML/CSS, Node.js, Ruby, SQL, Communication"',
    '5,Machine Learning Engineer,"Python, Machine Learning, Adaptability"',
    '6,Cloud Architect,"Cloud Computing, Python, Communication"',
    '7,Data Analyst,"Python, SQL, Machine Learning, Adaptability"',
    '8,Web Developer,"HTML/CSS, JavaScript, Ruby, Teamwork"',
    '9,Python Developer,"Python, SQL, Problem Solving, Self Motivated"',
    '10,JavaScript Developer,"JavaScript, React, Node.js, Self Motivated"',
]

csv_job_seekers_raw = [
    "id,name,skills",
    '1,Alice Seeker,"Ruby, SQL, Problem Solving"',
    '2,Bob Applicant,"JavaScript, HTML/CSS, Teamwork"',
    '3,Charlie Jobhunter,"Java, SQL, Problem Solving"',
    '4,Danielle Searcher,"Python, Machine Learning, Adaptability"',
    '5,Eddie Aspirant,"Cloud Computing, Communication"',
    '6,Fiona Candidate,"Python, SQL, Adaptability"',
    '7,George Prospect,"HTML/CSS, JavaScript, Ruby, Teamwork"',
    '8,Hannah Hunter,"Python, Problem Solving"',
    '9,Ian Jobhunter,"JavaScript, React, Self Motivated"',
    '10,Jane Applicant,"Ruby, Self Motivated"',
]

jobs_io = StringIO("\n".join(csv_jobs_raw))
job_seekers_io = StringIO("\n".join(csv_job_seekers_raw))


jobs = [
    Job(
        int(row["id"]),
        row["title"],
        {skill.strip().upper() for skill in row["required_skills"].split(",")},
    )
    for row in csv.DictReader(jobs_io)
]
job_seekers = [
    JobSeeker(
        int(row["id"]),
        row["name"],
        {skill.strip().upper() for skill in row["skills"].split(",")},
    )
    for row in csv.DictReader(job_seekers_io)
]


# Test Suite
@pytest.fixture
def in_memory_recommender_service():
    job_input = MockJobInput(jobs)
    job_seeker_input = MockJobSeekerInput(job_seekers)
    return InMemoryRecommenderService(jobseekers=job_seeker_input, jobs=job_input)


def test_get_job_indexes(in_memory_recommender_service):
    jobs_by_id, jobs_by_skills = in_memory_recommender_service._get_job_indexes()

    expected_jobs_by_id = len(jobs)

    skills = set()
    for job in jobs:
        skills |= job.required_skills

    # check size of indexes
    assert len(jobs_by_id) == expected_jobs_by_id
    assert len(jobs_by_skills) == len(skills)

    # check for absent records
    assert jobs_by_id.get(25, None) is None
    assert jobs_by_skills.get("CLOUD WATCHING", None) is None

    # manual check of item in skills index
    assert jobs_by_skills["PYTHON"] == {9, 5, 6, 7}
    assert jobs_by_skills["RUBY"] == {1, 4, 8}


def test_get_job_matches(in_memory_recommender_service):
    jobseeker = job_seekers[0]  # Alice Seeker
    jobs_by_id, jobs_by_skills = in_memory_recommender_service._get_job_indexes()

    matches = in_memory_recommender_service._get_job_matches(
        jobseeker, jobs_by_skills, jobs_by_id
    )

    # """1,Alice Seeker,1,Ruby Developer,3,100
    # 1,Alice Seeker,3,Backend Developer,2,50
    # 1,Alice Seeker,9,Python Developer,2,50
    # 1,Alice Seeker,4,Fullstack Developer,2,33
    # 1,Alice Seeker,7,Data Analyst,1,25
    # 1,Alice Seeker,8,Web Developer,1,25"""

    assert len(matches) == 6

    expected_job_matches = {
        ("Ruby Developer", 100),
        ("Backend Developer", 50),
        ("Python Developer", 50),
        ("Fullstack Developer", 33),
        ("Data Analyst", 25),
        ("Web Developer", 25),
    }

    resulting_matches = {
        (job_match.job.title, job_match.matching_skill_percent) for job_match in matches
    }

    assert expected_job_matches == resulting_matches


def test_format_job_matches_as_csv(in_memory_recommender_service):
    jobseeker = job_seekers[0]  # Alice Seeker
    jobs_by_id, jobs_by_skills = in_memory_recommender_service._get_job_indexes()

    matches = in_memory_recommender_service._get_job_matches(
        jobseeker, jobs_by_skills, jobs_by_id
    )

    # """1,Alice Seeker,1,Ruby Developer,3,100
    # 1,Alice Seeker,3,Backend Developer,2,50
    # 1,Alice Seeker,9,Python Developer,2,50
    # 1,Alice Seeker,4,Fullstack Developer,2,33
    # 1,Alice Seeker,7,Data Analyst,1,25
    # 1,Alice Seeker,8,Web Developer,1,25"""

    formatted_csv = list(format_job_matches_as_csv(matches))
    expected_header = (
        "jobseeker_id,jobseeker_name,job_id,job_title,"
        "matching_skill_count,matching_skill_percent"
    )
    assert formatted_csv[0] == expected_header

    # num of rows expected:
    assert len(formatted_csv) - 1 == 6  # remove header from count

    # num of columns expected
    assert len(formatted_csv[0].split(",")) == 6


def test_execute(in_memory_recommender_service):
    results = in_memory_recommender_service.execute()

    expected_rows = 49
    formatted_results = list(results)

    assert len(formatted_results) - 1 == expected_rows  # remove header row

    # check ordering...
    prev_job_seeker = -1
    prev_percent = 1000
    prev_job_id = -1

    JOB_SEEKER_ID_FIELD = 0
    JOB_ID_FIELD = 2
    MATCHING_SKILL_PERCENT_FIELD = 5

    for row in formatted_results[1:]:
        fields = row.split(",")

        assert prev_job_seeker <= int(fields[JOB_SEEKER_ID_FIELD])

        if prev_job_seeker == int(fields[JOB_SEEKER_ID_FIELD]):
            assert prev_percent >= int(fields[MATCHING_SKILL_PERCENT_FIELD])

            if prev_percent == int(fields[MATCHING_SKILL_PERCENT_FIELD]):
                assert prev_job_id < int(fields[JOB_ID_FIELD])

        prev_job_seeker = int(fields[JOB_SEEKER_ID_FIELD])
        prev_percent = int(fields[MATCHING_SKILL_PERCENT_FIELD])
        prev_job_id = int(fields[JOB_ID_FIELD])
