/**
 * SingleChoice Component
 *
 * Renders a group of radio buttons allowing only one selection.
 * Used for questions that require a single answer.
 *
 * @param {string} keyName - Unique identifier for the radio button group
 * @param {string} label - Display label for the question
 * @param {string[]} options - Array of option strings to display as radio buttons
 * @param {string} value - Currently selected option (single value, not array)
 * @param {function} onChange - Callback function called when radio button state changes
 *                              Receives (keyName, selectedValue) as parameters
 * @param {string} error - Optional error message to display
 * @param {boolean} required - Whether this field is required (default: false)
 * @param {number} splitAt - Optional index to split options into two columns (left and right)
 */
export default function SingleChoice({
  keyName,
  label,
  options,
  value,
  onChange,
  error,
  required = false,
  splitAt,
}) {
  /**
   * Renders label text with support for line breaks (\n) and italic text (*text*)
   */
  const renderLabel = (text) => {
    return text.split("\n").map((line, lineIndex, lineArray) => {
      // Split line by italic markers (*text*)
      const parts = line.split(/(\*[^*]+\*)/g);
      return (
        <span key={lineIndex}>
          {parts.map((part, partIndex) => {
            // Check if part is italic (starts and ends with *)
            if (part.startsWith("*") && part.endsWith("*") && part.length > 2) {
              return (
                <em key={partIndex} className="italic">
                  {part.slice(1, -1)}
                </em>
              );
            }
            return <span key={partIndex}>{part}</span>;
          })}
          {lineIndex < lineArray.length - 1 && <br />}
        </span>
      );
    });
  };

  return (
    <div className="flex flex-col w-full">
      <label className="mb-1">
        {renderLabel(label)}
        {required && <span className="text-red-400 ml-1">*</span>}
      </label>
      {error && (
        <p className="text-red-300 text-sm mb-2" role="alert">
          {error}
        </p>
      )}
      {splitAt !== undefined ? (
        // Two-column layout: split options at the specified index
        <div className="flex gap-8">
          <div className="flex-1">
            {options.slice(0, splitAt).map((option) => {
              const optionKey = option.toLowerCase().replace(/\s+/g, "-");
              const isChecked = value === option;
              return (
                <div key={option} className="flex items-center mb-2">
                  <input
                    className="radio-field accent-blue-500"
                    type="radio"
                    name={keyName}
                    checked={isChecked}
                    onChange={() => onChange(keyName, option)}
                    data-key={keyName}
                    data-value={option}
                    id={`${keyName}-${optionKey}`}
                  />
                  <label htmlFor={`${keyName}-${optionKey}`} className="ml-2">
                    {option}
                  </label>
                </div>
              );
            })}
          </div>
          <div className="flex-1">
            {options.slice(splitAt).map((option) => {
              const optionKey = option.toLowerCase().replace(/\s+/g, "-");
              const isChecked = value === option;
              return (
                <div key={option} className="flex items-center mb-2">
                  <input
                    className="radio-field accent-blue-500"
                    type="radio"
                    name={keyName}
                    checked={isChecked}
                    onChange={() => onChange(keyName, option)}
                    data-key={keyName}
                    data-value={option}
                    id={`${keyName}-${optionKey}`}
                  />
                  <label htmlFor={`${keyName}-${optionKey}`} className="ml-2">
                    {option}
                  </label>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        // Single-column layout (default)
        options.map((option) => {
          const optionKey = option.toLowerCase().replace(/\s+/g, "-");
          const isChecked = value === option;
          return (
            <div key={option} className="flex items-center mb-2">
              <input
                className="radio-field accent-blue-500"
                type="radio"
                name={keyName}
                checked={isChecked}
                onChange={() => onChange(keyName, option)}
                data-key={keyName}
                data-value={option}
                id={`${keyName}-${optionKey}`}
              />
              <label htmlFor={`${keyName}-${optionKey}`} className="ml-2">
                {option}
              </label>
            </div>
          );
        })
      )}
    </div>
  );
}
