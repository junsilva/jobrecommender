"""Contains individual commands for the Recommender application.

Each command will be a unique way to perform Job recommendation.
For the first iteration, the recommender application only supports
CSV files and does this in memory

Additional commands can be introduced to extend the functionality
e.g.
 - other input sources like DB
 - store intermediate results to handle larger inputs

"""

import click
from pathlib import Path
from .services import Recommender
from .models import CSVJobInput, CSVJobSeekerInput


@click.command(help="Use CSV inputs for Recommender")
@click.argument(
    "jobseekers_path",
    required=True,
    type=click.Path(exists=True, readable=True, path_type=Path),
)
@click.argument(
    "jobs_path",
    required=True,
    type=click.Path(exists=True, readable=True, path_type=Path),
)
def csv_input(jobseekers_path: Path, jobs_path: Path) -> None:
    """Match jobs with jobseekers.

    Args:
        jobseekers (Path): The path to the CSV file containing job seeker data.
                           Must exist and be readable.
        jobs (Path): The path to the CSV file containing job listings.
                     Must also exist and be readable.

    Raises:
        FileNotFoundError: If either of the provided file paths do not exist.
        PermissionError: If either of the provided files are not readable.

    """
    jobs = CSVJobInput(jobs_path)
    jobseekers = CSVJobSeekerInput(jobseekers_path)

    recommender = Recommender(jobseekers=jobseekers, jobs=jobs)

    jobs_by_id, jobs_by_skills = recommender.get_job_indexes()

    results = recommender.execute(
        job_seekers=jobseekers.get_job_seekers(),
        jobs_by_id=jobs_by_id,
        jobs_by_skills=jobs_by_skills,
    )

    print(results)
    # print(jobs_by_skills)
