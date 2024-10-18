"""Models"""

import csv
from dataclasses import dataclass, field
from collections import namedtuple


csv_job_fields = (
    "id",
    "title",
    "required_skills",
)
JobCSV = namedtuple("JobCSV", csv_job_fields)


@dataclass
class JobSeeker:
    id: int
    name: str
    skills: set[str] = field(default_factory=set)


@dataclass
class Jobs:
    id: int
    title: str
    required_skills: set[str] = field(default_factory=set)


@dataclass
class CSVJobInput:
    filename: str

    @property
    def jobs(self):
        with open(self.filename, "r", encoding="utf-8") as data:
            reader = csv.DictReader(data)
            for row in reader:
                yield Jobs(
                    id=int(row["id"]),
                    title=row["title"],
                    required_skills={
                        skill.strip().upper()
                        for skill in row["required_skills"].split(",")
                    },
                )


@dataclass
class CSVJobSeekerInput:
    filename: str

    @property
    def job_seekers(self):
        with open(self.filename, "r", encoding="utf-8") as data:
            reader = csv.DictReader(data)
            for row in reader:
                yield JobSeeker(
                    id=int(row["id"]),
                    name=row["name"],
                    skills={
                        skill.strip().upper()
                        for skill in row["skills"].split(",")
                    },
                )
