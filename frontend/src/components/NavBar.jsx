import "../styles/nav.css";

/**
 * NavBar Component
 *
 * Renders the main navigation bar with links to different sections.
 * Provides smooth scrolling navigation to Hero, Search, and Contact sections.
 */
export default function NavBar() {
  return (
    <nav>
      <a href="#hero">Home</a>
      <a href="#search">Search</a>
      <a href="#contact">Contact</a>
    </nav>
  );
}
