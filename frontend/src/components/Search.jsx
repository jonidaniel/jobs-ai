import QuestionSets from "./QuestionSets";

import "../styles/search.css";

export default function Search() {
  return (
    <section id="search">
      <h2>Search</h2>
      <h3 className="text-3xl font-semibold text-white text-center">
        Fill in questions in each category and we will find jobs relevant to you
      </h3>
      <QuestionSets />
    </section>
  );
}
