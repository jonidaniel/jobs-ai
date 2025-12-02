# JobsAI

An agentic AI system for end-to-end automated job finding and cover letter generation. Enter your skills and preferences once, and get personalized job recommendations with AI-generated cover letters.

## Overview

JobsAI automates the job search process by:

1. **Profiling** your skills and experience from a comprehensive questionnaire
2. **Searching** multiple job boards (Duunitori, Jobly) for relevant positions
3. **Scoring** job listings based on how well they match your profile
4. **Analyzing** top-scoring jobs with detailed reports
5. **Generating** personalized cover letters tailored to each position

## Architecture

The system consists of **5 components** arranged in a sequential pipeline:

### Agents (LLM-Powered)

1. **ProfilerAgent** (`src/jobsai/agents/profiler.py`)

   - Uses LLM to extract and structure candidate skills from form submissions
   - Creates a comprehensive skill profile with experience levels, technologies, and keywords

2. **ReporterAgent** (`src/jobsai/agents/reporter.py`)

   - Analyzes top-scoring job listings
   - Generates detailed reports highlighting job requirements and candidate fit

3. **GeneratorAgent** (`src/jobsai/agents/generator.py`)
   - Creates personalized cover letters based on job reports
   - Supports multiple writing styles (Professional, Friendly, Confident, Funny)

### Services (Deterministic)

4. **SearcherService** (`src/jobsai/agents/searcher.py`)

   - Scrapes job boards (Duunitori, Jobly) for relevant positions
   - Supports "deep mode" for fetching full job descriptions
   - Builds search queries from skill profile keywords

5. **ScorerService** (`src/jobsai/agents/scorer.py`)
   - Scores job listings based on skill profile match
   - Computes relevancy scores using keyword matching and experience alignment

## Technology Stack

### Backend

- **Python 3.12+** - Core language
- **FastAPI** - REST API framework
- **Pydantic** - Data validation and serialization
- **OpenAI API** - LLM-powered agents
- **BeautifulSoup** - Web scraping
- **python-docx** - Document generation
- **uv** - Package management (recommended)

### Frontend

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Modern JavaScript (ES6+)** - Language features

## Project Structure

```
JobsAI/
├── frontend/          # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── config/        # Configuration files
│   │   ├── styles/        # CSS files
│   │   └── utils/         # Utility functions
│   └── package.json
├── src/
│   └── jobsai/        # Python backend
│       ├── agents/         # Agent and service classes
│       ├── api/            # FastAPI server
│       ├── config/         # Configuration and schemas
│       ├── utils/           # Utility functions and scrapers
│       └── main.py          # Pipeline orchestration
├── docs/              # Project documentation
├── tests/             # Test files
└── README.md          # This file
```

## Setup

### Prerequisites

- **Python 3.12+**
- **Node.js** (for frontend)
- **uv** package manager (recommended for Python)

### Backend Setup

1. **Install dependencies using uv:**

   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root with:

   ```
   OPENAI_API_KEY=your_api_key_here
   MODEL_NAME=your_preferred_model
   ```

3. **Run the FastAPI server:**

   ```bash
   uv run python -m uvicorn jobsai.api.server:app --reload --app-dir src
   ```

   Or using uv directly:

   ```bash
   PYTHONPATH=src uv run uvicorn jobsai.api.server:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start development server:**

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. **Start both servers** (backend and frontend)
2. **Open the frontend** in your browser
3. **Fill out the questionnaire:**
   - General questions (job level, job boards, preferences)
   - Technology experience levels (8 sets)
   - Personal description
4. **Click "Find Jobs"** to trigger the pipeline
5. **Download** the generated cover letter document (.docx)

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **Frontend**: `docs/frontend.md` - Frontend architecture and components
- **API**: `docs/api.md` - API endpoint documentation
- **Architecture**: `docs/architecture.md` - System architecture overview
- **User Guide**: `docs/user-guide.md` - End-user instructions
- **How-To**: `docs/how-to.md` - Development and setup guides

## Development

### Running Tests

```bash
uv run pytest
```

### Code Style

- **Python**: Follow PEP 8 conventions
- **JavaScript**: ESLint configuration included
- **Frontend**: Uses Tailwind CSS for styling

## License

© 2025 Joni Mäkinen

## Version

0.9.0
