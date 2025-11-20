# ---------- JOBSAI MAIN ----------

from agents import AssessorAgent, SearcherAgent, ScorerAgent, ReporterAgent, INPUT_TEXT#, GeneratorAgent, NotifierAgent

def main():
    # 1️⃣ Assess input text / user profile
    assessor = AssessorAgent()
    assessment = assessor.assess(INPUT_TEXT)  # Returns a SkillProfile object

    # 2️⃣ Search jobs based on assessment
    searcher = SearcherAgent(job_boards=["duunitori"], deep=True)
    searcher.search_jobs(assessment.model_dump())  # Stores JSON to /data/job_listings/

    # 3️⃣ Score the jobs automatically
    scorer = ScorerAgent()
    scorer.score_jobs(skill_profile=assessment)  # Loads from /data/job_listings/, saves scored JSON

    # 4️⃣ ReporterAgent (example usage)
    # reporter = ReporterAgent()
    # reporter.generate_report()  # Reads scored jobs from data/job_listings/scored/

    reporter = ReporterAgent()
    report_text = reporter.generate_report(top_n=10)
    print(report_text)

    print("Job search & scoring pipeline complete. Scored jobs saved in data/job_listings/scored/")

if __name__ == "__main__":
    main()