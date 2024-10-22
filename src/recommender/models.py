"""Models"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class JobSeeker:
    id: int
    name: str
    skills: set[str] = field(default_factory=set)


@dataclass(slots=True)
class Job:
    id: int
    title: str
    required_skills: set[str] = field(default_factory=set)


@dataclass(order=False, slots=True)
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
