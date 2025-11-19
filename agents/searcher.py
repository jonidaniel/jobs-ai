# ---------- SEARCHER AGENT ----------

# 1. Takes the skill profile produced by the Skill Assessment agent
# 2. Converts it into search queries
# 3. Scrapes Finnish job sites
# 4. Parses the results into a normalized job listing schema
# 5. Saves listings under /data/job_listings/raw/ and /processed/
# 6. Returns structured listings to the Planner / Scorer agent

# This is the LLM-based orchestrator for job search:
# 1. Receives:
# • Skills profile (JSON)
# • Search settings (max listings, max sites, etc.)
# 2. Decides:
# • Which keywords to search
# • Which sites to use
# • How many results to fetch
# • Whether narrowing or expanding queries is needed
# 3. Instructs scraper functions to run
# 4. Returns:
# • Normalized list of job postings
# • Saved raw job JSON under /data/job_listings/
# • Metadata about the search (query coverage, failure logs)
