"""services"""

from typing import Protocol, Iterator, Tuple
from .models import JobSeeker, Job, JobMatch
from .constants import CSV_HEADERS
from collections import defaultdict
from typing import Callable, Any, TypeVar


class JobInput(Protocol):
    def get_jobs(self) -> Iterator[Job]: ...


class JobSeekerInput(Protocol):
    def get_job_seekers(self) -> Iterator[JobSeeker]: ...


T = TypeVar("T")

ResultFormatter = Callable[[list[JobMatch]], Any]


def get_matching_percentage(qualified_count: int, required_count: int) -> int:
    percentage = qualified_count / required_count
    return int(percentage * 100)


def format_job_matches_as_csv(
    job_matches: list[JobMatch],
) -> Iterator[str]:
    yield ",".join(CSV_HEADERS)

    for job_match in job_matches:
        yield (
            ",".join(
                (
                    str(job_match.jobseeker.id),
                    job_match.jobseeker.name,
                    str(job_match.job.id),
                    job_match.job.title,
                    str(job_match.matching_skill_count),
                    str(job_match.matching_skill_percent),
                )
            )
        )


class InMemoryRecommenderService:
    def __init__(
        self,
        jobseekers: JobSeekerInput,
        jobs: JobInput,
        formatter: ResultFormatter = format_job_matches_as_csv,
    ):
        self.jobseekers = jobseekers
        self.jobs = jobs
        self.formatter = formatter

    def _get_job_indexes(self) -> Tuple[dict[int, Job], dict[str, set[int]]]:
        job_by_id = {}
        job_by_skills_index = defaultdict(set)

        for job in self.jobs.get_jobs():
            job_by_id[job.id] = job

            for skill in job.required_skills:
                job_by_skills_index[skill].add(job.id)

        return job_by_id, job_by_skills_index

    def _get_job_matches(
        self,
        jobseeker: JobSeeker,
        jobs_by_skills: dict[str, set[int]],
        jobs_by_id: dict[int, Job],
    ) -> list[JobMatch]:
        qualified_jobs = set()

        for skill in jobseeker.skills:
            qualified_jobs |= jobs_by_skills.get(skill, set())

        matches = []
        for job_id in qualified_jobs:
            job = jobs_by_id[job_id]

            total_required_skills = len(job.required_skills)
            qualifications = jobseeker.skills & job.required_skills

            matches.append(
                JobMatch(
                    jobseeker=jobseeker,
                    job=job,
                    matching_skill_count=len(qualifications),
                    matching_skill_percent=get_matching_percentage(
                        len(qualifications), total_required_skills
                    ),
                )
            )

        return matches

    def execute(self) -> Any:
        job_seekers = self.jobseekers.get_job_seekers()
        jobs_by_id, jobs_by_skills = self._get_job_indexes()

        results = []
        for seeker in job_seekers:
            job_matches = self._get_job_matches(
                jobseeker=seeker,
                jobs_by_id=jobs_by_id,
                jobs_by_skills=jobs_by_skills,
            )
            results.extend(job_matches)

        return self.formatter(sorted(results))
