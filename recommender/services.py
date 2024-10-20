"""services"""

from typing import Protocol, Iterator, Tuple
from .models import JobSeeker, Job, JobMatch
from collections import defaultdict


class JobInput(Protocol):
    def get_jobs(self) -> Iterator[Job]: ...


class JobSeekerInput(Protocol):
    def get_job_seekers(self) -> Iterator[JobSeeker]: ...


def get_matching_percentage(qualified_count: int, required_count: int) -> int:
    percentage = qualified_count / required_count
    return int(percentage * 100)


class Recommender:
    def __init__(self, jobseekers: JobSeekerInput, jobs: JobInput):
        self.jobseekers = jobseekers
        self.jobs = jobs

    def get_job_indexes(self) -> Tuple[dict[int, Job], dict[str, set[int]]]:
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
            job = jobs_by_id.get(job_id, None)

            if not job:
                # log for now?  Change raise an exception if need to stop.
                # will only happen for case where multiple pages of jobs are
                # being processed...
                # TODO: confirm desired behaviour for this case.
                continue

            total_required_skills = len(job.required_skills)
            qualifications = jobseeker.skills & job.required_skills

            matches.append(
                JobMatch(
                    jobseeker_id=jobseeker.id,
                    job_id=job.id,
                    matching_skill_count=len(qualifications),
                    matching_skill_percent=get_matching_percentage(
                        len(qualifications), total_required_skills
                    ),
                )
            )

        return matches

    def execute(
        self,
        job_seekers: Iterator[JobSeeker],
        jobs_by_skills: dict[str, set[int]],
        jobs_by_id: dict[int, Job],
    ) -> Tuple[JobSeeker, list[JobMatch]]:
        results = []
        for seeker in job_seekers:
            job_matches = self._get_job_matches(
                jobseeker=seeker,
                jobs_by_id=jobs_by_id,
                jobs_by_skills=jobs_by_skills,
            )
            results.append((seeker, sorted(job_matches)))

        return results


# def sort_matches(match_list: list[JobMatch]) -> list[JobMatch]:
#     ### heap sort?
#     ### merge sort?
