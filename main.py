from agents import SkillAssessor, SearcherAgent

def main():
    assessor = SkillAssessor()
    searcher = SearcherAgent()

    text = """
    Joni Mäkinen has developed software since 2020.
    He has built and published multiple full-stack apps (frontend, backend, database, desktop, mobile).
    He has 3 years of experience with Git.
    He has 2 years of experience with web development.
    He has 2 years of experience with Node.js development.
    He has 2 years of experience with JavaScript.
    He has 1.5 years of experience with SQL.
    He has 1 year of experience with AWS.
    He has 1 year of experience with Python.
    He has 1 year of experience with React.
    He has little experience with React Native.
    He has little experience with Java, Kotlin, C++, and C#.
    He has little experience with LangChain, OpenAI Agents, and CrewAI.
    He has very good soft skills.
    He is an AWS Certified Solutions Architect (SAA-C03).
    He is an AWS Certified Cloud Practitioner (CLF-C02).
    """

    assessment = assessor.assess(text)
    searches = searcher.search_jobs(assessment.model_dump())
    print(searches)

    #assessor.save(result)
    #loaded = assessor.load_existing()
    #print(loaded == result)

    #loaded = assessor.load_existing()
    #print(loaded)

if __name__ == "__main__":
    main()
