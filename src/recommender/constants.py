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
