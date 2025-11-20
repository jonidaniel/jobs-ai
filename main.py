# ---------- JOBSAI MAIN ----------

from agents import AssessorAgent, SearcherAgent, ScorerAgent, INPUT_TEXT#, ReporterAgent, GeneratorAgent, NotifierAgent

def main():
    #planner = PlannerAgent()
    assessor = AssessorAgent()
    searcher = SearcherAgent()
    scorer = ScorerAgent()
    #reporter = ReporterAgent()
    #generator = GeneratorAgent()
    #notifier = NotifierAgent()

    assessment = assessor.assess(INPUT_TEXT)
    searcher.search_jobs(assessment.model_dump())
    result = scorer.score_jobs()
    print(result)

if __name__ == "__main__":
    main()
