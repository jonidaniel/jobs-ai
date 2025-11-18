from agents.skill_assessor import SkillAssessor

def main():
    assessor = SkillAssessor()

    text = """
    Joni strated programming in 2020.
    He is a developer with 2 years of experience with JavaScript, and half a year with Python.
    He is very familiar with Node.js, and fairly familiar with LangChain and OpenAI Agents.
    He has built multiple full-stack apps over the years.
    """
    result = assessor.assess(text)
    print(result)

if __name__ == "__main__":
    main()
