from agents.skill_assessor import SkillAssessor

def main():
    assessor = SkillAssessor()
    result = assessor.assess("")
    print(result)

if __name__ == "__main__":
    main()
