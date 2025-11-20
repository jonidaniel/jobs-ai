# ---------- JOBSAI ----------

# Version: 0.1.0
# Date: Fall 2025
# Author: Joni Mäkinen

# An agentic AI system for end-to-end automated job searching and job application document generation:
# enter your skills and preferences to the system once and get job recommendations and cover letters delivered to you continuously.
# Checks input resources consistently and updates search queries autonomously.

from agents import (
    AssessorAgent,
    SearcherAgent,
    ScorerAgent,
    ReporterAgent,
    )

from config import (
    USER_INPUT, # Initial skill and experience description of a candidate
    SKILL_PROFILE_PATH
    )

def main():
    # 1. Assess candidate
    # Returns a SkillProfile object
    skill_profile = AssessorAgent().assess(USER_INPUT)

    # 2. Search jobs based on assessment
    # Uses skill_profile to form keyword searches
    # The keyword searches are then used to scrape popular job listing websites
    # Stores acquired job listings as JSON to /data/job_listings/raw/*.json
    SearcherAgent(job_boards=["duunitori"], deep=True).search_jobs(skill_profile.model_dump())
    print("Searching job listings complete. Listings saved in /data/job_listings/")

    # 3. Score the jobs
    # Loads raw job listings JSON from /data/job_listings/raw/*.json
    # Saves scored job listings as JSON to /data/job_listings/scored/*.json
    ScorerAgent().score_jobs(skill_profile=skill_profile)
    print("Scoring jobs complete. Scored jobs saved in /data/job_listings/scored/")

    # 4. Write a job listing report
    # Saves the report to /data/reports/job_report.txt
    ReporterAgent().generate_report(top_n=10)
    print("Writing job listing report complete. Report saved to /data/reports/job_report.txt successfully")

if __name__ == "__main__":
    main()
