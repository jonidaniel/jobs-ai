// Gather all experience-category-container div's child sections (experience categories) to an array when the DOM content is loaded
document.addEventListener("DOMContentLoaded", () => {
  const sections = Array.from(
    document.querySelectorAll("#experience-categories-container section")
  );
  let currentIndex = 0;

  // Toggle a section's (an experience category's) state
  function showSection(index) {
    sections.forEach((section, i) => {
      section.classList.toggle("active", i === index);
    });
  }

  // On click listener for left arrow
  document.getElementById("prevBtn").onclick = () => {
    currentIndex = currentIndex === 0 ? sections.length - 1 : currentIndex - 1;
    showSection(currentIndex);
  };

  // On click listener for right arrow
  document.getElementById("nextBtn").onclick = () => {
    currentIndex = (currentIndex + 1) % sections.length;
    showSection(currentIndex);
  };

  // Show the first section
  showSection(currentIndex);
});
