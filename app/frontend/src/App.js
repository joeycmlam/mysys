import React, { useState } from "react";
import QuestionForm from "./components/QuestionForm";
import ResponseDisplay from "./components/ResponseDisplay";
import { askQuestion } from "./api/mcpApi";

const App = () => {
  const [response, setResponse] = useState(null);

  const handleQuestionSubmit = async (tool, question) => {
    const result = await askQuestion(tool, question);
    setResponse(result);
  };

  return (
    <div>
      <h1>MCP Question Answering</h1>
      <QuestionForm onSubmit={handleQuestionSubmit} />
      <ResponseDisplay response={response} />
    </div>
  );
};

export default App;