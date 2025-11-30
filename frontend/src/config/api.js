// API configuration
// Supports environment variables via Vite's import.meta.env
// Falls back to default development values if not set

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  SUBMIT_FORM: `${API_BASE_URL}/api/endpoint`,
};

// Export base URL for other uses if needed
export { API_BASE_URL };
