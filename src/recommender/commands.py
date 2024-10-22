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
import structlog
from .services import InMemoryRecommenderService
from .models import CSVJobInput, CSVJobSeekerInput
from .constants import NEW_LINE, LIMIT, WARNING_LIMIT_REACHED


logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


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
@click.option(
    "--output",
    type=click.File("w"),
    help="Output the results to a specified file instead of the terminal.",
)
@click.option(
    "--output_limit",
    type=click.INT,
    default=LIMIT,
    help="Max number of records to be displayed on terminal.",
)
def csv_input(
    jobseekers_path: Path, jobs_path: Path, output: Path, output_limit: int
) -> None:
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
    logger.info("Click command csv_input started")
    jobs = CSVJobInput(jobs_path)
    jobseekers = CSVJobSeekerInput(jobseekers_path)

    recommender = InMemoryRecommenderService(jobseekers=jobseekers, jobs=jobs)

    results = recommender.execute()
    logger.info("Done executing recommender service")

    logger.info("Start Writing results")
    if output:
        logger.info("Output to file selected.")
        with output as f:
            for line in results:
                f.write(line + NEW_LINE)
    else:
        logger.info("Output to terminal selected.")
        click.clear()

        header = next(results)
        click.secho(header, fg="cyan", bold=True)
        row_count = 1
        for line in results:
            if row_count > output_limit:
                logger.warning("Max number of results reached.  Stoping write.")
                click.secho(
                    WARNING_LIMIT_REACHED,
                    fg="red",
                    bold=True,
                )
                break

            click.secho(line, fg="green")
            row_count += 1

    logger.info("Done writing results")
    logger.info("Click command csv_input end")
