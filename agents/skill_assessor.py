# DESCRIPTION:
# • Builds a structured skill profile of the user, based on their résumé, web portfolio, GitHub repos, and any text inputs
# • The profile is stored in a vector database and refreshed over time
# • SkillAssessor is triggered by Planner

# RESPONSIBILITIES:
# A. Parses input text (resume, metadata)
#   • Extracts:
#     • Programming languages
#     • Frameworks
#     • Tools & libraries
#     • Cloud services
#     • AI/agentic experience
#     • Project descriptions
#     • Soft skills
#     • Estimated proficiency scores
#     • Job search keywords (LLM-generated)
# B. Normalizes the data
#   • Converts to a consistent format
# C. Saves to memory
#   • Writes JSON to /memory/vector_db/skills.json

# ACTS AS THE BASIS FOR:
# • Search keyword generation
# • Job scoring
# • Resume tailoring
# • Prioritization & recommendations
# • Iterative improvement

class SkillAssessor:
    def __init__(self, llm_client, memory_path):
        self.llm = llm_client
        self.memory_path = memory_path

    def assess(self, text_input: str) -> dict:
        """Call the LLM to parse skills and return structured profile."""
        print("In assess")

    def save(self, profile: dict):
        """Save profile to memory (JSON)."""
        print("In save")

    def load_existing(self) -> dict | None:
        """Load profile if it exists."""
        print("In load_existing")
