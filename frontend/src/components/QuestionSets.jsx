import { useEffect } from "react";
import builder from "../scripts/builder";
import navigatorScript from "../scripts/navigator";
import submitter from "../scripts/submitter";

export default function QuestionSets() {
  useEffect(() => {
    builder();
    navigatorScript();
    submitter();
  }, []);

  return (
    /*
     * Question set wrapper
     *
     * There are 8 question sets in total:
     *     1/8 'Programming, Scripting, and Markup Languages',
     *     2/8 'Databases',
     *     3/8 'Cloud Development',
     *     4/8 'Web Frameworks and Technologies',
     *     5/8 'Dev IDEs',
     *     6/8 'Large Language Models',
     *     7/8 'Code Documentation and Collaboration',
     *     8/8 'Computer Operating Systems'
     *
     *   Only one question set is shown on the webpage at a time
     */
    <div id="question-set-wrapper" className="relative" class="flex">
      <p>LEFT</p>
      {/* TailwindCSS form */}
      <div className="bg-gray-800 p-10 rounded-2xl shadow-lg">
        {/* General question set */}
        <section>
          <h3 class="text-3xl">1/8</h3>
          <h3 class="text-3xl">General Questions</h3>
          {/* Top left/right arrows */}
          <div className="flex justify-between items-center">
            <button className="prev-btn text-white text-2xl px-3 py-1">
              &larr;
            </button>
            <button className="next-btn text-white text-2xl px-3 py-1">
              &rarr;
            </button>
          </div>

          {/* Questions */}
          <div className="space-y-4">
            <div id="text-field0"></div>
          </div>

          {/* Bottom left/right arrows */}
          <div className="bottom-arrows flex justify-between items-center">
            <button className="prev-btn text-white text-2xl px-3 py-1">
              &larr;
            </button>
            <button className="next-btn text-white text-2xl px-3 py-1">
              &rarr;
            </button>
          </div>
        </section>

        {/* Create an array of 8 question sets */}
        {Array.from({ length: 8 }).map((_, i) => (
          /* Question set
           *
           * A single question set consists of:
           *     - Top left/right arrows
           *     - The actual questions
           *     - Bottom left/right arrows
           *
           * Left/right arrows change the question set
           */
          <section key={i}>
            <h3 class="text-3xl">{i + 2}/9</h3>
            <h3 class="text-3xl">{getTitle(i)}</h3>
            {/* Top left/right arrows */}
            <div className="flex justify-between items-center">
              <button className="prev-btn text-white text-2xl px-3 py-1">
                &larr;
              </button>
              <button className="next-btn text-white text-2xl px-3 py-1">
                &rarr;
              </button>
            </div>

            {/* Questions */}
            <div className="space-y-4">
              <div id={`sliders${i + 1}`}></div>
              <div id={`text-field${i + 1}`}></div>
            </div>

            {/* Bottom left/right arrows */}
            <div className="bottom-arrows flex justify-between items-center">
              <button className="prev-btn text-white text-2xl px-3 py-1">
                &larr;
              </button>
              <button className="next-btn text-white text-2xl px-3 py-1">
                &rarr;
              </button>
            </div>
          </section>
        ))}
      </div>
      <p>RIGHT</p>
    </div>
  );
}

function getTitle(i) {
  return [
    "Programming, Scripting, and Markup Languages Experience",
    "Databases Experience",
    "Cloud Development Experience",
    "Web Frameworks and Technologies Experience",
    "Dev IDEs Experience",
    "Large Language Models Experience",
    "Code Documentation and Collaboration Experience",
    "Computer Operating Systems Experience",
  ][i];
}
