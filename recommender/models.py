"""Models"""

import csv
from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class JobSeeker:
    id: int
    name: str
    skills: set[str] = field(default_factory=set)


@dataclass
class Job:
    id: int
    title: str
    required_skills: set[str] = field(default_factory=set)


@dataclass(order=False)
class JobMatch:
    jobseeker: JobSeeker
    job: Job

    matching_skill_count: int
    matching_skill_percent: int

    def __lt__(self, other):
        # Sort by jobseeker.id asc, matching_skill_percent desc, job.id asc
        if self.jobseeker.id != other.jobseeker.id:
            return self.jobseeker.id < other.jobseeker.id
        if self.matching_skill_percent != other.matching_skill_percent:
            return (
                self.matching_skill_percent > other.matching_skill_percent
            )  # Descending
        return self.job.id < other.job.id

    def __gt__(self, other):
        # Sort by jobseeker.id asc, matching_skill_percent desc, job.id asc
        if self.jobseeker.id != other.jobseeker.id:
            return self.jobseeker.id > other.jobseeker.id
        if self.matching_skill_percent != other.matching_skill_percent:
            return (
                self.matching_skill_percent < other.matching_skill_percent
            )  # Descending
        return self.job.id > other.job.id

    def __eq__(self, other):
        return (
            self.jobseeker.id == other.jobseeker.id
            and self.matching_skill_percent == other.matching_skill_percent
            and self.job.id == other.job.id
        )


@dataclass
class CSVJobInput:
    filename: Path

    def get_jobs(self) -> Iterator[Job]:
        with open(self.filename, "r", encoding="utf-8") as data:
            reader = csv.DictReader(data)
            for row in reader:
                yield Job(
                    id=int(row["id"]),
                    title=row["title"],
                    required_skills={
                        skill.strip().upper()
                        for skill in row["required_skills"].split(",")
                    },
                )


@dataclass
class CSVJobSeekerInput:
    filename: Path

    def get_job_seekers(self) -> Iterator[JobSeeker]:
        with open(self.filename, "r", encoding="utf-8") as data:
            reader = csv.DictReader(data)
            for row in reader:
                yield JobSeeker(
                    id=int(row["id"]),
                    name=row["name"],
                    skills={
                        skill.strip().upper() for skill in row["skills"].split(",")
                    },
                )
