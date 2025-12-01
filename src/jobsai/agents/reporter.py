"""
Orchestrates the reporting of the best-scored jobs.

CLASSES:
    ReporterAgent

FUNCTIONS (in order of workflow):
    1. generate_report      (public use)
    2. _load_scored_jobs    (internal use)
"""

import os
import logging
import json
from typing import List, Dict

from jobsai.config.paths import SCORED_JOB_LISTING_PATH, JOB_REPORT_PATH
from jobsai.config.prompts import (
    REPORTER_SYSTEM_PROMPT as SYSTEM_PROMPT,
    REPORTER_USER_PROMPT as USER_PROMPT,
)
from jobsai.config.schemas import SkillProfile

from jobsai.utils.llms import call_llm

logger = logging.getLogger(__name__)


class ReporterAgent:
    """Orchestrates the reporting of the best-scored jobs.

    Responsibilities:
    1. Load scored job listings
    2. Write a report/an analysis of the scored job listings

    Args:
        timestamp (str): The backend-wide timestamp of the moment when the main function was started.
    """

    def __init__(self, timestamp: str):
        self.timestamp = timestamp

    # ------------------------------
    # Public interface
    # ------------------------------
    def generate_report(self, skill_profile: SkillProfile, report_size: int) -> str:
        """
        Generate a summary report on the most-scored jobs.

        For each top-scoring job, the function:
        1. Uses an LLM to generate personalized cover letter instructions
        2. Formats the job details (title, company, location, score, etc.)
        3. Combines everything into a readable report

        The report is saved to /src/jobsai/data/job_reports/ and returned.

        Args:
            skill_profile (SkillProfile): The skill profile.
            report_size (int): The desired number of top jobs to include in the report.

        Returns:
            str: The complete job report as a formatted text string.
        """

        # Load scored jobs from previous step
        scored_jobs = self._load_scored_jobs()
        if not scored_jobs:
            logger.warning(" No scored jobs found for reporting.")
            return ""

        # Sort jobs by score descending (already done in scorer, but safe to re-sort)
        scored_jobs.sort(key=lambda x: x.get("score", 0), reverse=True)

        # Initialize report with header
        report_lines = ["Job Report", "=" * 40, f"Top {report_size} Jobs:\n"]

        # Process each top-scoring job
        for job in scored_jobs[:report_size]:
            full_description = job.get("full_description")

            # Generate personalized cover letter instructions using LLM
            # The LLM analyzes the job description and skill profile to create
            # specific instructions for writing a tailored cover letter
            instructions = call_llm(
                SYSTEM_PROMPT,
                USER_PROMPT.format(
                    full_description=full_description,
                    skill_profile=skill_profile,
                ),
            )

            # Get the job details
            title = job.get("title") or "N/A"
            company = job.get("company") or "N/A"
            location = job.get("location") or "N/A"
            score = job.get("score", 0)
            matched = ", ".join(job.get("matched_skills", []))
            missing = ", ".join(job.get("missing_skills", []))
            url = job.get("url") or "N/A"

            # Add the job details to the report
            report_lines.append(f"Title: {title}")
            report_lines.append(f"Company: {company}")
            report_lines.append(f"Location: {location}")
            report_lines.append(f"Score: {score}%")
            report_lines.append(f"Matched Skills: {matched}")
            report_lines.append(f"Missing Skills: {missing}")
            report_lines.append(f"URL: {url}")
            report_lines.append(f"Instructions: {instructions}")
            report_lines.append("-" * 40)

        report_text = "\n".join(report_lines)

        # Form a dated filename and join it with the report path
        filename = f"{self.timestamp}_job_report.txt"
        path = os.path.join(JOB_REPORT_PATH, filename)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(report_text)

            logger.info(f" Saved job report to /{path}")
        except Exception as e:
            logger.error(f" Failed to save job report: {e}")

        return report_text

    # ------------------------------
    # Internal function
    # ------------------------------
    def _load_scored_jobs(self) -> List[Dict]:
        """Load the scored job listings.

        Loads the scored job listings from SCORED_JOB_LISTING_PATH.

        Returns:
            List[Dict]: The list of scored job listings.
        """

        path = os.path.join(
            SCORED_JOB_LISTING_PATH, f"{self.timestamp}_scored_jobs.json"
        )
        if not os.path.exists(path):
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            logger.error(f" Failed to load scored jobs: {e}")
            return []
