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
    jobseeker_id: int
    job_id: int

    matching_skill_count: int
    matching_skill_percent: int

    def __lt__(self, other):
        # Sort by matching_skill_percent desc, then by job_id asc
        if self.matching_skill_percent == other.matching_skill_percent:
            return self.job_id < other.job_id
        return self.matching_skill_percent > other.matching_skill_percent

    def __gt__(self, other):
        # Sort by matching_skill_percent desc, then by job_id asc
        if self.matching_skill_percent == other.matching_skill_percent:
            return self.job_id > other.job_id
        return self.matching_skill_percent < other.matching_skill_percent

    def __eq__(self, other):
        return (
            self.matching_skill_percent == other.matching_skill_percent
            and self.job_id == other.job_id
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
                        skill.strip().upper()
                        for skill in row["skills"].split(",")
                    },
                )


if __name__ == "__main__":
    jobseekers = Path("G:\\Files\\Downloads\\jobseekers.csv")

    js_input = CSVJobSeekerInput(jobseekers)

    for seeker in js_input.get_job_seekers():
        print(seeker)
