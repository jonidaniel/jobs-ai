# Frontend Documentation

## Overview

The JobsAI frontend is a React application built with Vite that provides a user-friendly interface for job seekers to input their skills and preferences. The application collects user data through a multi-step questionnaire, sends it to the backend API, and downloads generated cover letters.

## Technology Stack

- **Framework**: React 19.2.0
- **Build Tool**: Vite 7.2.4
- **Styling**:
  - Tailwind CSS 3.4.18 (utility-first CSS)
  - Custom CSS files for component-specific styles
- **Language**: JavaScript (ES6+)
- **Package Manager**: npm

## Project Structure

```
frontend/
├── dist/                    # Production build output
├── node_modules/            # Dependencies
├── public/                  # Static assets
│   └── vite.svg
├── src/
│   ├── assets/              # Images and icons
│   │   ├── icons/
│   │   │   └── favicon.ico
│   │   └── imgs/
│   │       └── face.png
│   ├── components/          # React components
│   │   ├── messages/        # Message/alert components
│   │   │   ├── ErrorMessage.jsx
│   │   │   └── SuccessMessage.jsx
│   │   ├── questions/       # Form input components
│   │   │   ├── MultipleChoice.jsx
│   │   │   ├── SingleChoice.jsx
│   │   │   ├── Slider.jsx
│   │   │   └── TextField.jsx
│   │   ├── Contact.jsx
│   │   ├── Hero.jsx
│   │   ├── NavBar.jsx
│   │   ├── QuestionSet.jsx
│   │   ├── QuestionSets.jsx
│   │   └── Search.jsx
│   ├── config/              # Configuration files
│   │   ├── api.js
│   │   ├── generalQuestions.js
│   │   ├── questionSet.js
│   │   └── sliders.js
│   ├── styles/              # CSS stylesheets
│   │   ├── App.css
│   │   ├── contact.css
│   │   ├── hero.css
│   │   ├── index.css
│   │   ├── nav.css
│   │   └── search.css
│   ├── utils/               # Utility functions
│   │   ├── errorMessages.js
│   │   ├── fileDownload.js
│   │   └── formDataTransform.js
│   ├── App.jsx              # Root component
│   └── main.jsx             # Application entry point
├── eslint.config.js         # ESLint configuration
├── index.html               # HTML template
├── package.json             # Dependencies and scripts
├── postcss.config.js        # PostCSS configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── vite.config.js           # Vite configuration
```

## Directory Organization

### `/src/components/`

React components organized by purpose:

#### Main Components
- **`App.jsx`**: Root component that orchestrates all page sections
- **`NavBar.jsx`**: Fixed navigation bar with links to page sections
- **`Hero.jsx`**: Landing section with main title and tagline
- **`Search.jsx`**: Main questionnaire component that handles form submission
- **`QuestionSets.jsx`**: Manages 10 question sets with navigation and form state
- **`QuestionSet.jsx`**: Renders a single question set (one of 10)
- **`Contact.jsx`**: Contact information section with links

#### `/src/components/questions/`

Reusable form input components:

- **`Slider.jsx`**: Range input for experience levels (0-7 years)
- **`TextField.jsx`**: Text input for user text responses
- **`MultipleChoice.jsx`**: Checkbox group for multiple selections
- **`SingleChoice.jsx`**: Radio button group for single selection

#### `/src/components/messages/`

User feedback components:

- **`ErrorMessage.jsx`**: Displays error messages in a red alert box
- **`SuccessMessage.jsx`**: Displays success messages in a green alert box

### `/src/config/`

Configuration files containing constants, data structures, and API endpoints:

- **`api.js`**: API endpoint configuration and base URL
- **`questionSet.js`**: Application-wide constants (question set structure, names, titles)
- **`generalQuestions.js`**: Configuration for the general questions set (labels, keys, options, constants)
- **`sliders.js`**: Technology data for slider-based question sets and slider configuration

### `/src/utils/`

Utility functions for common operations:

- **`formDataTransform.js`**: Transforms flat form data into grouped structure for backend API
- **`fileDownload.js`**: Handles programmatic file download from blob responses
- **`errorMessages.js`**: Converts technical error objects into user-friendly messages

### `/src/styles/`

Component-scoped CSS files:

- **`index.css`**: Global styles and Tailwind imports
- **`App.css`**: Application-level styles
- **`nav.css`**: Navigation bar styles
- **`hero.css`**: Hero section styles
- **`search.css`**: Search/questionnaire section styles
- **`contact.css`**: Contact section styles

### `/src/assets/`

Static assets (images, icons, fonts):

- **`icons/`**: Favicon and icon files
- **`imgs/`**: Image files used in components

## Component Architecture

### Component Hierarchy

```
App
├── NavBar
├── Hero
├── Search
│   ├── QuestionSets
│   │   ├── QuestionSet (rendered 10 times)
│   │   │   ├── Slider (for technology questions)
│   │   │   ├── TextField (for text inputs)
│   │   │   ├── MultipleChoice (for checkboxes)
│   │   │   └── SingleChoice (for radio buttons)
│   │   └── Navigation arrows
│   ├── SuccessMessage (conditional)
│   └── ErrorMessage (conditional)
└── Contact
```

### Key Components

#### `QuestionSets.jsx`

The main orchestrator for the questionnaire:

- **10 question sets** with navigation (prev/next buttons)
- **Form state management** for all inputs across all question sets
- **Synchronization** with parent `Search` component via callback
- **Smooth scrolling** to active question set

**Responsibilities:**
- Initializes form data with default values
- Manages current question set index (0-9)
- Handles navigation between question sets
- Updates form state on input changes
- Notifies parent component of form data changes

#### `QuestionSet.jsx`

Renders a single question set based on its index:

- **Index 0**: General questions (5 questions: 2 multiple choice, 3 single choice)
- **Indices 1-8**: Slider question sets (technology experience sliders + "Other" text field)
- **Index 9**: Text-only question set (single text input for additional information)

**Dynamic Rendering:**
- Conditionally renders different input types based on question set index
- Uses appropriate components (`MultipleChoice`, `SingleChoice`, `Slider`, `TextField`)
- Only the active question set is visible (others hidden via CSS)

#### `Search.jsx`

Orchestrates form submission and API communication:

1. Receives form data from `QuestionSets` via `onFormDataChange` callback
2. Transforms flat form data into grouped structure using `transformFormData()`
3. Sends POST request to backend API
4. Downloads returned `.docx` file using `downloadBlob()`
5. Displays success/error messages using `SuccessMessage`/`ErrorMessage` components
6. Manages submission state to prevent double-submission

**State Management:**
- `formData`: Complete form data from all question sets
- `isSubmitting`: Prevents double-submission
- `error`: Error message state
- `success`: Success message state
- `successTimeoutRef`: Ref for auto-dismissing success message

## Configuration Files

### `api.js`

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  SUBMIT_FORM: `${API_BASE_URL}/api/endpoint`,
};
```

- Configures API base URL (defaults to `http://localhost:8000`)
- Supports environment variable `VITE_API_BASE_URL`
- Centralizes all API endpoints

### `questionSet.js`

Application-wide constants for questionnaire structure:

- **`TOTAL_QUESTION_SETS`**: 10 (total number of question sets)
- **`QUESTION_SET_NAMES`**: Kebab-case names for each question set (e.g., "general", "languages", "databases")
- **`QUESTION_SET_TITLES`**: Display titles for each question set (shown as headings)

### `generalQuestions.js`

Configuration for the general questions set (index 0):

- **`GENERAL_QUESTIONS_INDEX`**: 0
- **`GENERAL_QUESTIONS_COUNT`**: 5
- **`GENERAL_QUESTION_LABELS`**: Display labels for 5 questions
- **`GENERAL_QUESTION_KEYS`**: Form data keys (e.g., "job-level", "job-boards", "deep-mode")
- **Option arrays**:
  - `NAME_OPTIONS`: Job level options (Expert, Intermediate, Entry, Intern)
  - `JOB_BOARD_OPTIONS`: Job board options (Duunitori, Jobly)
  - `DEEP_MODE_OPTIONS`: Deep mode options (Yes, No)
  - `JOB_COUNT_OPTIONS`: Job count options (1, 2, 3, 4, 5, 10)
  - `COVER_LETTER_STYLE_OPTIONS`: Style options (Professional, Friendly, Confident)

### `sliders.js`

Technology data and slider configuration:

- **`SLIDER_MIN`**: 0 (minimum slider value)
- **`SLIDER_MAX`**: 7 (maximum slider value)
- **`SLIDER_DEFAULT`**: 0 (default slider value)
- **`SLIDER_DATA`**: Array of 8 objects, each containing technology key-value pairs for one question set
  - Languages, databases, cloud development, web frameworks, dev IDEs, LLMs, documentation tools, operating systems

## Styling Approach

### Tailwind CSS

Utility-first CSS framework used for:

- Layout (flexbox, grid)
- Spacing (padding, margin)
- Colors and typography
- Responsive design
- Component styling (buttons, inputs, etc.)

### Custom CSS

Component-specific styles in separate files:

- Scoped to component IDs (e.g., `#search`, `#hero`, `#contact`)
- Handles complex styling not easily achieved with Tailwind
- Maintains separation of concerns
- Each component imports its own CSS file

### CSS Organization

- **Global styles**: `index.css` (Tailwind imports, root variables, base styles)
- **Component styles**: Individual files per component (imported in component files)
- **App-level styles**: `App.css` for application-wide rules

## Data Flow

### Form Data Collection

1. **User Input**: User fills out questions across 10 question sets
2. **State Management**: `QuestionSets` component manages form state locally
3. **Callback**: `onFormDataChange` callback updates `Search` component state
4. **Submission**: User clicks "Find Jobs" button
5. **Processing**: `Search.handleSubmit()`:
   - Calls `transformFormData()` to filter empty values and group by question set
   - Transforms flat data structure to grouped backend format
6. **API Request**: POST to `/api/endpoint` with grouped data
7. **Response**: Backend returns `.docx` file as blob
8. **Download**: `downloadBlob()` programmatically triggers file download
9. **Feedback**: Success or error message displayed to user

### Data Structure

**Frontend Form Data** (flat structure):

```javascript
{
  "job-level": ["Expert", "Intermediate"],
  "job-boards": ["Duunitori", "Jobly"],
  "deep-mode": "Yes",
  "cover-letter-num": "5",
  "cover-letter-style": "Professional",
  "javascript": 5,
  "python": 3,
  "text-field1": "Additional languages...",
  "additional-info": "Additional information...",
  ...
}
```

**Backend Payload** (grouped by question set):

```javascript
{
  "general": [
    {"job-level": ["Expert", "Intermediate"]},
    {"job-boards": ["Duunitori", "Jobly"]},
    {"deep-mode": "Yes"},
    {"cover-letter-num": "5"},
    {"cover-letter-style": "Professional"}
  ],
  "languages": [
    {"javascript": 5},
    {"python": 3},
    {"text-field1": "Additional languages..."}
  ],
  "databases": [...],
  "cloud-development": [...],
  "web-frameworks": [...],
  "dev-ides": [...],
  "llms": [...],
  "doc-and-collab": [...],
  "operating-systems": [...],
  "additional-info": [
    {"additional-info": "Additional information..."}
  ]
}
```

## Utility Functions

### `formDataTransform.js`

**`transformFormData(formData)`**

Transforms flat form data into grouped structure for backend API:

- Filters out empty values (empty strings, 0 numbers, empty arrays)
- Groups data by question set using `QUESTION_SET_NAMES`
- Returns structured object matching backend expectations

### `fileDownload.js`

**`downloadBlob(blob, headers, defaultFilename)`**

Handles programmatic file download:

- Extracts filename from `Content-Disposition` header
- Creates temporary download link
- Programmatically triggers download
- Cleans up blob URL and DOM elements

### `errorMessages.js`

**`getErrorMessage(error)`**

Converts technical error objects into user-friendly messages:

- Maps network errors to connection failure messages
- Maps HTTP status codes (400, 404, 500) to user-friendly messages
- Provides fallback for unexpected errors

## Development Setup

### Prerequisites

- Node.js (v18 or higher recommended)
- npm

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

Starts Vite dev server at `http://localhost:5173` (default port).

**Features:**
- Hot Module Replacement (HMR)
- Fast refresh
- Source maps
- Optimized development builds

### Linting

```bash
npm run lint
```

Runs ESLint to check code quality and catch errors.

### Building for Production

```bash
npm run build
```

Creates optimized production build in `dist/` directory:

- Minified JavaScript
- Optimized CSS
- Asset optimization
- Tree-shaking
- Code splitting

### Preview Production Build

```bash
npm run preview
```

Serves the production build locally for testing.

## Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

For production:

```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

**Note**: Vite requires the `VITE_` prefix for environment variables to be exposed to the client.

## Adding New Features

### Adding a New Question Set

1. **Update `config/questionSet.js`**:
   - Increment `TOTAL_QUESTION_SETS`
   - Add name to `QUESTION_SET_NAMES` array
   - Add title to `QUESTION_SET_TITLES` array

2. **Add data to `config/sliders.js`** (if slider-based):
   - Add new object to `SLIDER_DATA` array with technology key-value pairs

3. **Update `components/QuestionSets.jsx`**:
   - Add initialization logic for new question set in `formData` state (if needed)

4. **Update `components/QuestionSet.jsx`**:
   - Add rendering logic for new question set type (if different from existing types)

### Adding a New General Question

1. **Update `config/generalQuestions.js`**:
   - Add label to `GENERAL_QUESTION_LABELS` array
   - Add key to `GENERAL_QUESTION_KEYS` array
   - Add options array (e.g., `NEW_QUESTION_OPTIONS`)
   - Increment `GENERAL_QUESTIONS_COUNT`

2. **Update `components/QuestionSet.jsx`**:
   - Add rendering logic in general questions section (determine if multiple or single choice)

### Adding a New Component

1. Create component file in appropriate `src/components/` subdirectory:
   - Main components: `src/components/`
   - Form inputs: `src/components/questions/`
   - Messages: `src/components/messages/`

2. Import and use in parent component

3. Add component-specific CSS in `src/styles/` (if needed)

4. Import CSS in component file

### Adding a New Utility Function

1. Create function in appropriate `src/utils/` file or create new file
2. Export the function
3. Import and use in components that need it

### Adding a New API Endpoint

1. **Update `config/api.js`**:

   ```javascript
   export const API_ENDPOINTS = {
     SUBMIT_FORM: `${API_BASE_URL}/api/endpoint`,
     NEW_ENDPOINT: `${API_BASE_URL}/api/new-endpoint`,
   };
   ```

2. **Use in component**:

   ```javascript
   import { API_ENDPOINTS } from "../config/api";

   const response = await fetch(API_ENDPOINTS.NEW_ENDPOINT, {...});
   ```

## API Integration

### Backend Communication

The frontend communicates with the FastAPI backend:

- **Endpoint**: `/api/endpoint` (configurable via `VITE_API_BASE_URL`)
- **Method**: POST
- **Content-Type**: `application/json`
- **Request Body**: Grouped form data (see Data Flow section)
- **Response**: `.docx` file as blob with `Content-Disposition` header

### Error Handling

The `Search` component includes comprehensive error handling:

- **Network errors**: Connection failures (handled by `getErrorMessage()`)
- **HTTP errors**: 400, 404, 500 status codes (mapped to user-friendly messages)
- **User-friendly messages**: Technical errors converted to readable messages
- **Success feedback**: Auto-dismissing success message after 5 seconds
- **Error display**: `ErrorMessage` component shows errors in red alert box

### File Download

The application automatically downloads the generated cover letter:

1. Receives blob from API response
2. Calls `downloadBlob()` utility function
3. Extracts filename from `Content-Disposition` header (or uses default)
4. Creates temporary download link
5. Programmatically triggers download
6. Cleans up blob URL and DOM elements

## Code Style

### Naming Conventions

- **Components**: PascalCase (e.g., `QuestionSets.jsx`, `ErrorMessage.jsx`)
- **Files**: PascalCase for components, camelCase for config/utils
- **CSS files**: kebab-case (e.g., `search.css`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `TOTAL_QUESTION_SETS`)
- **Functions/Variables**: camelCase
- **Directories**: kebab-case (e.g., `questions/`, `messages/`)

### Component Structure

```javascript
/**
 * Component Description
 *
 * Detailed explanation of component purpose and usage.
 *
 * @param {type} propName - Description
 */
export default function ComponentName({ prop1, prop2 }) {
  // State declarations
  const [state, setState] = useState(initial);

  // Refs
  const ref = useRef(null);

  // Effects
  useEffect(() => {
    // Effect logic
  }, [dependencies]);

  // Event handlers
  const handleEvent = () => {
    // Handler logic
  };

  // Render
  return (
    // JSX
  );
}
```

### File Organization

- **Imports**: Grouped by type (React, components, config, utils, styles)
- **Comments**: JSDoc-style comments for components and functions
- **Structure**: Logical ordering (state, effects, handlers, render)

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Consider code-splitting for large components
2. **Memoization**: Use `React.memo()` for expensive components if needed
3. **State Management**: Minimize unnecessary re-renders
4. **Asset Optimization**: Images optimized during build
5. **Bundle Size**: Tree-shaking removes unused code
6. **Efficient State Updates**: Use functional updates for state

### Current Performance

- **Initial Load**: Fast due to Vite's optimized build
- **HMR**: Near-instant updates during development
- **Form State**: Efficient state management with React hooks
- **File Download**: Streamed blob download for large files
- **Component Rendering**: Only active question set rendered (others hidden via CSS)

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ features required
- No IE11 support

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check `VITE_API_BASE_URL` in `.env`
   - Verify backend server is running
   - Check CORS settings on backend
   - Check browser console for network errors

2. **Styles Not Loading**
   - Verify CSS imports in components
   - Check Tailwind configuration
   - Ensure PostCSS is configured correctly
   - Verify `index.css` imports Tailwind directives

3. **Form Data Not Submitting**
   - Check browser console for errors
   - Verify API endpoint is correct
   - Check network tab for request details
   - Verify form data transformation is working

4. **Build Errors**
   - Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
   - Check for syntax errors
   - Verify all imports are correct
   - Check for unused variables or imports

5. **Question Sets Not Displaying**
   - Verify `TOTAL_QUESTION_SETS` matches actual number of sets
   - Check `QUESTION_SET_NAMES` and `QUESTION_SET_TITLES` arrays
   - Verify question set rendering logic in `QuestionSet.jsx`

## Future Improvements

Potential enhancements:

1. **TypeScript**: Add type safety for better developer experience
2. **State Management**: Consider Redux/Zustand for complex state if needed
3. **Testing**: Add unit and integration tests (Jest, React Testing Library)
4. **Accessibility**: Improve ARIA labels and keyboard navigation
5. **Internationalization**: Add i18n support for multiple languages
6. **Progressive Web App**: Add PWA capabilities for offline support
7. **Error Boundaries**: Add React error boundaries for better error handling
8. **Loading States**: Improve loading indicators during API calls
9. **Form Validation**: Client-side validation before submission
10. **Responsive Design**: Enhanced mobile experience
11. **Animation**: Add smooth transitions between question sets
12. **Progress Indicator**: Show progress through question sets

## Related Documentation

- [API Documentation](./api.md) - Backend API endpoints
- [Architecture](./architecture.md) - Overall system architecture
- [User Guide](./user-guide.md) - End-user documentation
- [Project Structure](./project-structure.md) - Full project organization
