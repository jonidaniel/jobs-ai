# ---------- SEARCHER AGENT ----------

# 1. Takes the skill profile produced by the Skill Assessment agent
# 2. Converts it into search queries
# 3. Scrapes Finnish job sites
# 4. Parses the results into a normalized job listing schema
# 5. Saves listings under /data/job_listings/raw/ and /processed/
# 6. Returns structured listings to the Planner / Scorer agent
