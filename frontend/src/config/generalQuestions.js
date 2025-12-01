/**
 * General Questions Configuration
 *
 * Configuration for the General Questions set (question set index 0).
 * This set contains 5 questions:
 * - Questions 0-1: Multiple choice (checkboxes)
 * - Questions 2-4: Single choice (radio buttons)
 */

/** Index of the General Questions set in the questionnaire */
export const GENERAL_QUESTIONS_INDEX = 0;

/** Number of questions in the General Questions set */
export const GENERAL_QUESTIONS_COUNT = 5;

/**
 * Labels for each question in the General Questions set
 *
 * Index mapping:
 * 0: Job level (multiple choice - see NAME_OPTIONS)
 * 1: Job boards (multiple choice - see JOB_BOARD_OPTIONS)
 * 2: Deep mode (single choice - see DEEP_MODE_OPTIONS)
 * 3: Job count (single choice - see JOB_COUNT_OPTIONS)
 * 4: Cover letter style (single choice - see COVER_LETTER_STYLE_OPTIONS)
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
 * Single choice options for the third question (Deep mode)
 *
 * Users can select only one option (radio buttons).
 * These represent whether to use deep mode for job scraping.
 */
export const DEEP_MODE_OPTIONS = ["Yes", "No"];

/**
 * Single choice options for the fourth question (Job count)
 *
 * Users can select only one option (radio buttons).
 * These represent the number of jobs to include in the job report.
 */
export const JOB_COUNT_OPTIONS = ["1", "2", "3", "4", "5", "10"];

/**
 * Single choice options for the fifth question (Cover letter style)
 *
 * Users can select only one option (radio buttons).
 * These represent the desired style for the cover letter.
 */
export const COVER_LETTER_STYLE_OPTIONS = [
  "Professional",
  "Friendly",
  "Confident",
];
