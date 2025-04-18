from typing import Optional
from mcp.server.fastmcp import FastMCP
from app.pdf_qa.pdf_reader import extract_text_from_pdf
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document

# Initialize MCP server
mcp = FastMCP("pdf_qa")

# Load LLM for question answering
llm = OpenAI(temperature=0)

@mcp.tool()
async def load_pdf(pdf_path: str) -> str:
    """Load a PDF file and extract its text."""
    try:
        global pdf_text
        pdf_text = extract_text_from_pdf(pdf_path)
        return "PDF loaded successfully."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def ask_question(question: str) -> str:
    """Answer a question based on the loaded PDF content."""
    global pdf_text
    if not pdf_text:
        return "No PDF loaded. Please load a PDF first."
    
    # Prepare the document for the QA chain
    document = Document(page_content=pdf_text)
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    answer = qa_chain.run(input_documents=[document], question=question)
    return answer

if __name__ == "__main__":
    pdf_text: Optional[str] = None  # Global variable to store PDF text
    mcp.run()
```

# Requirements
PyPDF2>=3.0.0
langchain>=0.0.200
openai>=0.27.0