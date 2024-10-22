"""input.py"""

import csv
from pathlib import Path
from dataclasses import dataclass, field
import structlog
from typing import Iterator, Any
from .models import Job, JobSeeker
from .constants import (
    JOB_CSV_SCHEMA,
    JOBSEEKER_CSV_SCHEMA,
    JOB_ID,
    JOB_REQUIRED_SKILLS,
    JOB_TITLE,
    JOBSEEKER_ID,
    JOBSEEKER_NAME,
    JOBSEEKER_SKILLS,
)


logger: structlog.stdlib.BoundLogger = structlog.get_logger()


def convert_csv_row(
    schema: dict[str, Any],
    csv_row: dict[str, str],
    encountered_ids: set[int],
    id_field: str,
    name: str,
) -> dict[str, Any]:
    try:
        converted_row = {key: schema[key](value) for key, value in csv_row.items()}
        if converted_row[id_field] not in encountered_ids:
            encountered_ids.add(converted_row[id_field])
        else:
            raise ValueError("Duplicate row ID found")

        return converted_row

    except ValueError as e:
        logger.error(
            f"Error converting row for {name}",
            error=str(e),
        )
        raise


@dataclass
class CSVJobInput:
    filename: Path
    ids_encountered: set[int] = field(default_factory=set)

    def get_jobs(self) -> Iterator[Job]:
        with open(self.filename, "r", encoding="utf-8") as data:
            reader = csv.DictReader(data)

            for row in reader:
                converted_row = convert_csv_row(
                    schema=JOB_CSV_SCHEMA,
                    csv_row=row,
                    encountered_ids=self.ids_encountered,
                    id_field=JOB_ID,
                    name=Job.__name__,
                )

                yield Job(
                    id=converted_row[JOB_ID],
                    title=converted_row[JOB_TITLE],
                    required_skills={
                        skill.strip().upper()
                        for skill in converted_row[JOB_REQUIRED_SKILLS].split(",")
                    },
                )


@dataclass
class CSVJobSeekerInput:
    filename: Path
    ids_encountered: set[int] = field(default_factory=set)

    def get_job_seekers(self) -> Iterator[JobSeeker]:
        with open(self.filename, "r", encoding="utf-8") as data:
            reader = csv.DictReader(data)
            for row in reader:
                converted_row = convert_csv_row(
                    schema=JOBSEEKER_CSV_SCHEMA,
                    csv_row=row,
                    encountered_ids=self.ids_encountered,
                    id_field=JOB_ID,
                    name=JobSeeker.__name__,
                )

                yield JobSeeker(
                    id=converted_row[JOBSEEKER_ID],
                    name=converted_row[JOBSEEKER_NAME],
                    skills={
                        skill.strip().upper()
                        for skill in converted_row[JOBSEEKER_SKILLS].split(",")
                    },
                )
