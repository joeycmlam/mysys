import React, { useState } from "react";

const QuestionForm = ({ onSubmit }) => {
  const [tool, setTool] = useState("weather");
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(tool, question);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="tool">Select Tool:</label>
        <select
          id="tool"
          value={tool}
          onChange={(e) => setTool(e.target.value)}
        >
          <option value="weather">Weather</option>
          <option value="pdf_qa">PDF QA</option>
        </select>
      </div>
      <div>
        <label htmlFor="question">Your Question:</label>
        <input
          type="text"
          id="question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          required
        />
      </div>
      <button type="submit">Ask</button>
    </form>
  );
};

export default QuestionForm;