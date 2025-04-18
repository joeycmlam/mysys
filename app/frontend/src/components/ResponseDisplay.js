import React from "react";

const ResponseDisplay = ({ response }) => {
  if (!response) return null;

  return (
    <div>
      <h3>Response:</h3>
      <pre>{response.error || response}</pre>
    </div>
  );
};

export default ResponseDisplay;