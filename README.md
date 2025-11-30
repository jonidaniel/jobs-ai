# JobsAI (0.9.0)

## Description

### An agentic AI system for end-to-end automated job finding and cover letter generation: enter your skills and preferences to the system once and get job recommendations and cover letters continuously. Checks input resources consistently and updates search queries autonomously.

## Agent Architecture

### Entails 7 agents arranged in a _prompt chaining architecture_, each agent with predefined purposes and responsibilities:

1. Profiler Agent `JobsAI/src/jobsai/agents/skill_assessor.py`

   - Assesses a candidate's skillset and forms a skill profile for them

2. Searcher Agent `JobsAI/src/jobsai/agents/searcher.py`

   - Searches relevant jobs from various job boards

3. Scorer Agent `JobsAI/src/jobsai/agents/scorer.py`

   - Scores the found jobs based on relevancy

4. Reporter Agent `JobsAI/src/jobsai/agents/reporter.py`

   - Writes analysis reports on the highest-scored jobs

5. Generator Agent `JobsAI/src/jobsai/agents/generator.py`

   - Generates cover letters the jobs

6. Notifier agent `JobsAI/src/jobsai/agents/notifier.py`

   - Notifies the candidate of new cover letters

## Technologies

JobsAI is built using [Python]()

JobsAI requires minimum Python3.12 for it to work.

## Setup

JobAI was developed with `uv` package manager and we strongly recommend using it for running the system

## Author

© 2025 Joni Mäkinen
