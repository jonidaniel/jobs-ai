import { useState } from "react";
import QuestionSets from "./QuestionSets";
import "../styles/search.css";

export default function Search() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    e.stopPropagation();

    // Prevent double submission
    if (isSubmitting) {
      return;
    }
    setIsSubmitting(true);

    // Collect form data
    const result = {};

    // Iterate over all slider questions
    document.querySelectorAll(".slider").forEach((slider) => {
      if (slider.value != 0) {
        const key = slider.dataset.key;
        result[key] = Number(slider.value);
      }
    });

    // Iterate over all checkbox questions (multiple choice)
    document.querySelectorAll(".checkbox-field").forEach((checkbox) => {
      if (checkbox.checked) {
        const key = checkbox.dataset.key;
        const value = checkbox.dataset.value;
        // Store as array if multiple selections, or as single value
        if (!result[key]) {
          result[key] = [];
        }
        result[key].push(value);
      }
    });

    // Iterate over all text field questions
    document.querySelectorAll(".text-field").forEach((textField) => {
      if (textField.value != "") {
        const key = textField.dataset.key;
        result[key] = textField.value.trim();
      }
    });

    // Send to backend and download document
    try {
      const response = await fetch("http://localhost:8000/api/endpoint", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(result),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      // Get the response as a blob (binary)
      const blob = await response.blob();

      // Get the filename from Content-Disposition header if available
      const contentDisposition = response.headers.get("Content-Disposition");
      let filename = "document.docx"; // default fallback
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="?(.+)"?/);
        if (match && match[1]) filename = match[1];
      }

      // Create a temporary URL for the blob
      const url = window.URL.createObjectURL(blob);

      // Create a temporary link element to trigger download
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();

      // Clean up the blob URL
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Download failed:", error);
    } finally {
      // Reset submission flag after request completes
      setIsSubmitting(false);
    }
  };

  return (
    <section id="search">
      <h2>Search</h2>
      <h3 className="text-3xl font-semibold text-white text-center">
        Answer questions in each category and we will find jobs relevant to you
      </h3>
      <QuestionSets />
      {/* Submit button */}
      <div className="flex justify-center">
        <button
          id="submit-btn"
          onClick={handleSubmit}
          disabled={isSubmitting}
          className="text-3xl mt-6 px-6 py-3 border border-white bg-transparent text-white font-semibold rounded-lg shadow disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? "Finding Jobs..." : "Find Jobs"}
        </button>
      </div>
    </section>
  );
}
