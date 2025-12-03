"""
Form data extraction and transformation utilities.

Extracts and transforms frontend form submission data into structured format
for use by the JobsAI pipeline.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


def extract_form_data(form_submissions: Dict) -> Dict:
    """
    Extract and transform form submission data into structured format.

    Processes the frontend payload to extract:
    - General questions (job level, job boards, deep mode, cover letter settings)
    - Personal description
    - Converts and validates data types (e.g., cover_letter_num to int)
    - Handles array-to-string conversion for cover_letter_style

    Args:
        form_submissions (Dict): Form data from frontend containing:
            - "general": Array of 5 single-key objects with general questions
            - "additional-info": Array with personal description

    Returns:
        Dict: Structured dictionary with keys:
            - "job_level": List of selected job levels
            - "job_boards": List of selected job boards
            - "deep_mode": String ("Yes" or "No")
            - "cover_letter_num": Integer (number of cover letters to generate)
            - "cover_letter_style": String (style description, e.g., "Professional and Friendly")
            - "description": String (personal description)

    Raises:
        KeyError: If required form fields are missing
        ValueError: If cover_letter_num cannot be converted to int (defaults to 5)
    """
    # General questions
    job_level = form_submissions.get("general")[0].get("job-level")
    job_boards = form_submissions.get("general")[1].get("job-boards")
    deep_mode = form_submissions.get("general")[2].get("deep-mode")
    # Personal description
    description = form_submissions.get("additional-info")[0].get("additional-info")

    # Convert cover_letter_num to integer (comes from frontend as string)
    try:
        cover_letter_num = int(
            form_submissions.get("general")[3].get("cover-letter-num")
        )
    except (ValueError, TypeError) as e:
        logger.warning(f"Invalid cover_letter_num, defaulting to 5: {e}")
        cover_letter_num = 5

    # Handle cover_letter_style (can be string or array from frontend)
    cover_letter_style_raw = form_submissions.get("general")[4].get(
        "cover-letter-style"
    )
    if isinstance(cover_letter_style_raw, list):
        # If array, join with " and " (e.g., ["Professional", "Friendly"] -> "Professional and Friendly")
        cover_letter_style = " and ".join(cover_letter_style_raw)
    else:
        cover_letter_style = cover_letter_style_raw or "Professional"

    return {
        "job_level": job_level,
        "job_boards": job_boards,
        "deep_mode": deep_mode,
        "cover_letter_num": cover_letter_num,
        "cover_letter_style": cover_letter_style,
        "description": description,
    }
