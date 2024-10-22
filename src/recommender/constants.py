"""Constants."""

CSV_HEADERS = [
    "jobseeker_id",
    "jobseeker_name",
    "job_id",
    "job_title",
    "matching_skill_count",
    "matching_skill_percent",
]

NEW_LINE = "\n"

LIMIT = 100

WARNING_LIMIT_REACHED = (
    "Warning, result count greater than configured limit. "
    "Output to file to view the rest of the results."
)

JOB_ID = "id"
JOB_TITLE = "title"
JOB_REQUIRED_SKILLS = "required_skills"

JOBSEEKER_ID = "id"
JOBSEEKER_NAME = "name"
JOBSEEKER_SKILLS = "skills"

JOB_CSV_SCHEMA = {
    JOB_ID: int,
    JOB_TITLE: str,
    JOB_REQUIRED_SKILLS: str,
}

JOBSEEKER_CSV_SCHEMA = {
    JOBSEEKER_ID: int,
    JOBSEEKER_NAME: str,
    JOBSEEKER_SKILLS: str,
}
