"""
Form Data Extraction and Transformation Utilities.

This module provides utilities for extracting and transforming frontend form
submission data into a structured format suitable for the JobsAI pipeline.

The main function, extract_form_data(), processes the complex nested structure
from the frontend and extracts:
- The selected job boards
- The deep mode setting
- The number of cover letters to generate
- The style of the cover letters
- The technology stack organized by category
"""

from typing import Dict


def extract_form_data(form_submissions: Dict) -> Dict:
    """
    Extract and transform form submission data into structured format.

    Processes the frontend payload to extract:
    - The selected job boards
    - The deep mode setting
    - The number of cover letters to generate
    - The style of the cover letters
    - The technology stack

    Args:
        form_submissions (Dict): Form data from frontend containing:
            - "general": Array of 5 single-key objects with general questions (job level, job boards, deep mode, cover letter num, cover letter style)
            - "languages": Array of technology set items with programming, scripting, and markup languages
            - "databases": Array of technology set items with databases
            - "cloud-development": Array of technology set items with cloud development tools
            - "web-frameworks": Array of technology set items with web frameworks and technologies
            - "dev-ides": Array of technology set items with development IDEs
            - "llms": Array of technology set items with LLMs
            - "doc-and-collab": Array of technology set items with document and collaboration tools
            - "operating-systems": Array of technology set items with computer operating systems
            - "additional-info": Array with personal description

    Returns:
        Dict: Structured dictionary with keys:
            - "job_boards": Array of strings, contains one or more strings
            - "deep_mode": String, either "Yes" or "No"
            - "cover_letter_num": Integer, between 1 and 10
            - "cover_letter_style": Array of strings, contains one or more strings
            - "tech_stack": Array of arrays, contains one or more arrays of technology set items
    """

    # The selected job boards, deep mode setting, number of cover letters to generate, and style of the cover letters
    # Always an array, contains one or more strings
    job_boards = form_submissions.get("general")[1].get("job-boards")
    # Always a string, either "Yes" or "No"
    deep_mode = form_submissions.get("general")[2].get("deep-mode")
    # Always an integer, between 1 and 10
    cover_letter_num = form_submissions.get("general")[3].get("cover-letter-num")
    # Always an array of strings, contains one or more strings
    cover_letter_style = form_submissions.get("general")[4].get("cover-letter-style")

    # Extract technology categories into a tech stack list
    # Always an array of arrays, contains one or more arrays of technology set items
    tech_stack = [
        form_submissions.get("languages", []),
        form_submissions.get("databases", []),
        form_submissions.get("cloud-development", []),
        form_submissions.get("web-frameworks", []),
        form_submissions.get("dev-ides", []),
        form_submissions.get("llms", []),
        form_submissions.get("doc-and-collab", []),
        form_submissions.get("operating-systems", []),
    ]

    return {
        "job_boards": job_boards,
        "deep_mode": deep_mode,
        "cover_letter_num": cover_letter_num,
        "cover_letter_style": cover_letter_style,
        "tech_stack": tech_stack,
    }
