# ---------- PATHS ----------

from pathlib import Path

# ----- LOCAL PATHS -----

SKILL_PROFILE_PATH = Path("src/jobsai/memory/vector_db/")
RAW_JOB_LISTING_PATH = Path("src/jobsai/data/job_listings/raw/")
SCORED_JOB_LISTING_PATH = Path("src/jobsai/data/job_listings/scored/")
JOB_REPORT_PATH = Path("src/jobsai/data/job_reports/")
COVER_LETTER_PATH = Path("src/jobsai/data/cover_letters/")

SKILL_PROFILE_PATH.mkdir(parents=True, exist_ok=True)
RAW_JOB_LISTING_PATH.mkdir(parents=True, exist_ok=True)
SCORED_JOB_LISTING_PATH.mkdir(parents=True, exist_ok=True)
JOB_REPORT_PATH.mkdir(parents=True, exist_ok=True)
COVER_LETTER_PATH.mkdir(parents=True, exist_ok=True)

# ----- URLS -----

HOST_URL_DUUNITORI = "https://duunitori.fi"
SEARCH_URL_BASE_DUUNITORI = (
    "https://duunitori.fi/tyopaikat/haku/{query_slug}?sivu={page}"
)
HOST_URL_JOBLY = "https://jobly.fi"
SEARCH_URL_BASE_JOBLY = "https://duunitori.fi/tyopaikat/search/{query_slug}?page={page}"
