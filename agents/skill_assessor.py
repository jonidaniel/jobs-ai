# ---------- SKILLASSESSOR ----------

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

import os
import json
import logging

from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import ValidationError
from openai import OpenAI

from agents.prompts.skill_assessor_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, OUTPUT_SCHEMA_INSTRUCTION

from agents.schemas.skill_profile import SkillProfile

from utils.normalization import normalize_list

# Load environment variables
load_dotenv()

# Init OpenAI client
client = OpenAI()

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI model configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
if not OPENAI_MODEL:
    logger.warning("OPENAI_MODEL not found in environment. OpenAI calls will fail without it.")

# OpenAI API key configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not found in environment. OpenAI calls will fail without it.")
client.api_key = OPENAI_API_KEY

# Path for the structured skill profile
MEMORY_PATH = Path("memory/vector_db/skills.json")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

class SkillAssessor:
    def __init__(self, model: str = OPENAI_MODEL, memory_path: Path = MEMORY_PATH):
        self.model = model
        self.memory_path = memory_path

    def _call_llm(self, prompt: str, max_tokens: int = 800) -> str:
        #if not openai.api_key:
        if not client.api_key:
            raise RuntimeError("OpenAI API key not configured. Set OPENAI_API_KEY env var.")
        logger.info("Calling LLM...")
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        text = resp.choices[0].message.content
        logger.debug("LLM response: %s", text[:500])
        return text

    def assess(self, input_text: str, name_hint: str = "") -> SkillProfile:
        user_prompt = USER_PROMPT_TEMPLATE.format(input_text=input_text)
        raw = self._call_llm(user_prompt)
        # Ensure we get JSON: try to extract JSON substring
        json_text = self._extract_json(raw)
        if json_text is None:
            raise ValueError("LLM did not return parseable JSON.")
        parsed = json.loads(json_text)
        # Normalize lists and keys
        parsed = self._normalize_parsed(parsed)
        # Validate with pydantic
        try:
            profile = SkillProfile(**parsed)
        except ValidationError as e:
            logger.error("Validation error: %s", e)
            raise
        # If name empty, fill from hint
        if not profile.name and name_hint:
            profile.name = name_hint
        return profile

    def _extract_json(self, text: str) -> Optional[str]:
        # crude extraction: find first { and the matching }
        start = text.find("{")
        if start == -1:
            return None
        # attempt to balance braces
        brace = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                brace += 1
            elif text[i] == "}":
                brace -= 1
                if brace == 0:
                    return text[start:i+1]
        # fallback: try direct load
        try:
            json.loads(text)
            return text
        except Exception:
            return None

    def _normalize_parsed(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        # Ensure keys exist
        keys = [
            "name", "core_languages", "frameworks_and_libraries", "tools_and_platforms",
            "agentic_ai_experience", "ai_ml_experience", "soft_skills", "projects_mentioned",
            "experience_level", "job_search_keywords"
        ]
        for k in keys:
            if k not in parsed:
                parsed[k] = [] if k != "experience_level" else {"Python": 0, "JavaScript": 0, "Agentic AI": 0, "AI/ML": 0}
        # Normalize lists
        for list_key in ["core_languages", "frameworks_and_libraries", "tools_and_platforms",
                         "agentic_ai_experience", "ai_ml_experience", "soft_skills", "projects_mentioned", "job_search_keywords"]:
            if isinstance(parsed.get(list_key), list):
                parsed[list_key] = normalize_list(parsed[list_key])
            else:
                parsed[list_key] = []
        # Normalize experience_level keys and values
        el = parsed.get("experience_level", {})
        norm_el = {
            "Python": int(el.get("Python") or 0),
            "JavaScript": int(el.get("JavaScript") or 0),
            "Agentic AI": int(el.get("Agentic AI") or el.get("Agentic_Ai") or 0),
            "AI/ML": int(el.get("AI/ML") or el.get("AI_ML") or 0)
        }
        parsed["experience_level"] = norm_el
        # Name normalization
        if not parsed.get("name") or not isinstance(parsed["name"], str):
            parsed["name"] = ""
        else:
            parsed["name"] = parsed["name"].strip()
        return parsed

    def save(self, profile: SkillProfile):
        # Write JSON to memory path
        out = json.loads(profile.json(by_alias=True))
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        logger.info("Saved skill profile to %s", self.memory_path)

    def load_existing(self) -> Optional[SkillProfile]:
        if not self.memory_path.exists():
            return None
        with open(self.memory_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        try:
            return SkillProfile(**data)
        except ValidationError:
            return None

    def merge_update(self, new_profile: SkillProfile) -> SkillProfile:
        """Merge new_profile into existing profile (union lists, max experience levels)."""
        existing = self.load_existing()
        if not existing:
            self.save(new_profile)
            return new_profile
        # merge lists
        merged = existing.dict()
        for list_key in ["core_languages", "frameworks_and_libraries", "tools_and_platforms",
                         "agentic_ai_experience", "ai_ml_experience", "soft_skills", "projects_mentioned", "job_search_keywords"]:
            merged[list_key] = list(dict.fromkeys(existing.dict()[list_key] + new_profile.dict()[list_key]))
        # merge experience levels (take max)
        el_existing = existing.experience_level.dict(by_alias=True)
        el_new = new_profile.experience_level.dict(by_alias=True)
        merged_el = {}
        for k in ["Python", "JavaScript", "Agentic AI", "AI/ML"]:
            merged_el[k] = max(int(el_existing.get(k, 0) or 0), int(el_new.get(k, 0) or 0))
        merged["experience_level"] = merged_el
        merged["name"] = new_profile.name or existing.name
        merged_profile = SkillProfile(**merged)
        self.save(merged_profile)
        return merged_profile

# ---------- SIMPLE CLI USAGE ----------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run SkillAssessor on a resume text file.")
    parser.add_argument("file", help="Path to a plain-text resume or profile file.")
    parser.add_argument("--name", help="Candidate name hint", default="")
    parser.add_argument("--merge", action="store_true", help="Merge with existing profile instead of overwriting.")
    args = parser.parse_args()

    if not Path(args.file).exists():
        logger.error("Input file not found: %s", args.file)
        raise SystemExit(1)

    text = Path(args.file).read_text(encoding="utf-8")
    assessor = SkillAssessor()
    try:
        profile = assessor.assess(text, name_hint=args.name)
    except Exception as e:
        logger.exception("Assessment failed: %s", e)
        raise

    if args.merge:
        merged = assessor.merge_update(profile)
        logger.info("Merged profile saved. Summary: %s", merged.json(indent=2))
    else:
        assessor.save(profile)
        logger.info("Profile saved. Summary: %s", profile.json(indent=2))
