/**
 * General Questions Configuration
 *
 * Configuration for the General Questions set (question set index 0).
 * This set contains 5 questions, all of which are multiple choice.
 */

/**
 * Labels for each question in the General Questions set
 *
 * Index mapping:
 * 0: Job level (multiple choice - see NAME_OPTIONS)
 * 1: Job boards (multiple choice - see JOB_BOARD_OPTIONS)
 * 2: Deep mode (multiple choice - see DEEP_MODE_OPTIONS)
 * 3: Job count (multiple choice - see JOB_COUNT_OPTIONS)
 * 4: Cover letter style (multiple choice - see COVER_LETTER_STYLE_OPTIONS)
 */
export const GENERAL_QUESTION_LABELS = [
  "1. What level of job are you looking for?",
  "2. What job boards you want to include in the search?",
  "3. Do you want to use 'deep mode' when searching?",
  "4. For how many top jobs you want cover letters?",
  "5. What kind of style you want the letters to be?",
];

/**
 * Key names for each question in the General Questions set
 *
 * These are the keys used in the form data object sent to the backend.
 * Index mapping:
 * 0: "job-level"
 * 1: "job-boards"
 * 2: "deep-mode"
 * 3: "cover-letter-num"
 * 4: "cover-letter-style"
 */
export const GENERAL_QUESTION_KEYS = [
  "job-level",
  "job-boards",
  "deep-mode",
  "cover-letter-num",
  "cover-letter-style",
];

/**
 * Multiple choice options for the first question (Job level)
 *
 * Users can select multiple options (checkboxes).
 * These represent experience levels that can be combined.
 */
export const NAME_OPTIONS = ["Expert", "Intermediate", "Entry", "Intern"];

/**
 * Multiple choice options for the second question (Job boards)
 *
 * Users can select multiple options (checkboxes).
 * These represent job boards to scrape.
 */
export const JOB_BOARD_OPTIONS = ["Duunitori", "Jobly"];

/**
 * Multiple choice options for the third question (Deep mode)
 *
 * Users can select multiple options (checkboxes).
 * These represent whether to use deep mode for job scraping.
 */
export const DEEP_MODE_OPTIONS = ["Yes", "No"];

/**
 * Multiple choice options for the fourth question (Job count)
 *
 * Users can select multiple options (checkboxes).
 * These represent the number of jobs to include in the job report.
 */
export const JOB_COUNT_OPTIONS = ["1", "2", "3", "4", "5", "10"];

/**
 * Multiple choice options for the fifth question (Cover letter style)
 *
 * Users can select multiple options (checkboxes).
 * These represent the desired style for the cover letter.
 */
export const COVER_LETTER_STYLE_OPTIONS = [
  "Professional",
  "Friendly",
  "Confident",
];
