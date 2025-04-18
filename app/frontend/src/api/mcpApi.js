import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Replace with your MCP server URL

export const askQuestion = async (tool, question) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/tools/${tool}`, {
      question,
    });
    return response.data;
  } catch (error) {
    console.error("Error calling MCP server:", error);
    return { error: "Failed to get a response from the server." };
  }
};