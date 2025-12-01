/**
 * Converts technical error objects into user-friendly error messages
 *
 * Provides centralized error message handling for the application.
 * Maps various error types (network errors, HTTP status codes) to
 * user-friendly messages.
 *
 * @param {Error} error - The error object from fetch or other operations
 * @returns {string} User-friendly error message
 */
export function getErrorMessage(error) {
  if (error instanceof TypeError && error.message.includes("fetch")) {
    return "Unable to connect to the server. Please check your internet connection and try again.";
  }
  if (error.message.includes("Server error: 404")) {
    return "The requested endpoint was not found. Please contact support.";
  }
  if (error.message.includes("Server error: 500")) {
    return "The server encountered an error. Please try again later.";
  }
  if (error.message.includes("Server error: 400")) {
    return "Invalid request. Please check your answers and try again.";
  }
  if (error.message.includes("Server error")) {
    return `Server error occurred. Please try again later. (${error.message})`;
  }
  return "An unexpected error occurred. Please try again.";
}
