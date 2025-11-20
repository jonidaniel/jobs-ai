# ---------- JOBSAI MAIN ----------

from agents import AssessorAgent, SearcherAgent, INPUT_TEXT#, ScorerAgent, ReporterAgent, GeneratorAgent, NotifierAgent

def main():
    #planner = PlannerAgent()
    assessor = AssessorAgent()
    searcher = SearcherAgent()
    #scorer = ScorerAgent()
    #reporter = ReporterAgent()
    #generator = GeneratorAgent()
    #notifier = NotifierAgent()

    assessment = assessor.assess(INPUT_TEXT)
    searches = searcher.search_jobs(assessment.model_dump())
    #print(searches)

if __name__ == "__main__":
    main()
