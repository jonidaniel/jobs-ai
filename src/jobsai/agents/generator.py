"""JobsAI/src/jobsai/agents/generator.py

Acts as the GENERATOR AGENT.

CLASSES:
    GeneratorAgent

FUNCTIONS (in order of workflow):
    1. GeneratorAgent.generate_letters     (public use)
    2. GeneratorAgent._build_system_prompt (internal use)
    3. GeneratorAgent._build_user_prompt   (internal use)
    4. GeneratorAgent._write_letter        (internal use)"""

import os
import logging
from datetime import datetime
from typing import Dict

from docx import Document

from jobsai.config.paths import COVER_LETTER_PATH
from jobsai.config.prompts import (
    GENERATOR_SYSTEM_PROMPT as SYSTEM_PROMPT,
    GENERATOR_USER_PROMPT as USER_PROMPT,
)
from jobsai.config.schemas import SkillProfile

from jobsai.utils.llms import call_llm
from jobsai.utils.normalization import normalize_text

logger = logging.getLogger(__name__)


class GeneratorAgent:
    """Generates cover letters.

    Args:
        timestamp (str): The backend-wide timestamp of the moment when the main function was started.
    """

    def __init__(self, timestamp: str):
        self.timestamp = timestamp

    # ------------------------------
    # Public interface
    # ------------------------------
    def generate_letters(
        self,
        skill_profile: SkillProfile,
        job_report: str,
        letter_style: str,
        contact_info: Dict,
    ) -> Document:
        """Produce a tailored job-application message based on the candidate's skills and the job report.

        Args:
            skill_profile (SkillProfile): The candidate's skill profile.
            job_report (str): The job report that contains instructions for what kind of cover letter to write.
            letter_style (str): The intended style/tone of the cover letter.

        Returns:
            Document: The final cover letter.
        """

        system_prompt = self._build_system_prompt(letter_style)
        user_prompt = self._build_user_prompt(skill_profile, job_report)

        logger.info(" GENERATING COVER LETTER ...")

        cover_letter = self._write_letter(system_prompt, user_prompt, contact_info)

        logger.info(" COVER LETTER GENERATED\n")

        return cover_letter

    # ------------------------------
    # Internal functions
    # ------------------------------

    def _build_system_prompt(self, style: str) -> str:
        """Build the system prompt that is used to write the cover letter.

        Args:
            style (str): The intended style/tone of the cover letter.

        Returns:
            str: The system prompt that is used to write the cover letter.
        """

        tone_instructions = {
            "professional": (
                "Write in a clear, respectful, concise, professional tone. "
                "Use well-structured paragraphs. Avoid exaggerations."
            ),
            "friendly": ("Write in a warm, positive tone but keep it professional."),
            "confident": (
                "Write with a confident, proactive tone without sounding arrogant."
            ),
        }

        base_style = tone_instructions.get(style, tone_instructions["professional"])

        return SYSTEM_PROMPT.format(base_style=base_style)

    def _build_user_prompt(
        self,
        skill_profile: SkillProfile,
        job_report: str,
    ) -> str:
        """Build the user prompt that is used to write the cover letter.

        Args:
            skill_profile (SkillProfile): The candidate's skill profile.
            job_report (str): The job report that contains instructions for what kind of cover letter to write.

        Returns:
            str: The user prompt that is used to write the cover letter.
        """

        # KS:DJNÖJKSD
        json_profile = skill_profile.model_dump_json(indent=2)

        return USER_PROMPT.format(json_profile=json_profile, job_report=job_report)

    def _write_letter(
        self, system_prompt: str, user_prompt: str, contact_info: Dict
    ) -> Document:
        """Write the cover letter.

        Args:
            system_prompt (str): The system prompt that is used to write the cover letter.
            user_prompt (str): The user prompt that is used to write the cover letter.
            contact_info (Dict): The candidate's contact information.

        Returns:
            Document: The ready cover letter.
        """

        cover_letter = Document()

        # Contact information at the top
        p = cover_letter.add_paragraph()
        p.add_run(f'{contact_info.get("website")}\n')
        p.add_run(f'{contact_info.get("linkedin")}\n')
        p.add_run(f'{contact_info.get("github")}\n\n')
        p.add_run(f'{contact_info.get("email")}\n')
        p.add_run(f'{contact_info.get("phone")}\n\n')

        # Turn the timestamp into a 'pretty date'
        dt = datetime.strptime(self.timestamp, "%Y%m%d_%H%M%S")
        pretty_date = dt.strftime("%B %d, %Y")
        # Add the date
        cover_letter.add_paragraph(f"{pretty_date}\n")

        # Add the recipient
        cover_letter.add_paragraph("ADD RECRUITER/HIRING TEAM")
        cover_letter.add_paragraph("ADD HIRING COMPANY/GROUP\n\n")

        # Get the actual body/content of the cover letter
        raw = call_llm(system_prompt, user_prompt)
        normalized = normalize_text(raw)
        # Insert the body to the document
        cover_letter.add_paragraph(normalized)

        filename = f"{self.timestamp}_cover_letter.docx"
        # Save the cover letter to /src/jobsai/data/cover_letters/
        cover_letter.save(os.path.join(COVER_LETTER_PATH, filename))

        return cover_letter
