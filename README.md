# ghost

## Minimal RAG Example

This repository includes a tiny retrieval‑augmented generation (RAG) demo built with Flask. Documents located in `docs/` are loaded into a simple vector store on startup. The user can upload additional markdown or text files, query the collection, and receive a synthetic "Risk Reflection" report.

### Features
- Upload and parse markdown/text documents
- Simple vector store using token overlap
- Prompt input field and optional *Reflection Mode*
- Retrieval logic that surfaces relevant document chunks
- Mocked report generation summarizing content, risks, strategy, and contradiction notes

### Setup
1. Install dependencies
   ```bash
   pip install flask
   ```
2. Run the server
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser to test.

### Files
- `app.py` – basic Flask server
- `rag_logic.py` – retrieval and report generation logic
- `templates/index.html` – minimal HTML interface
- `docs/` – sample internal markdown documents

### RAG Concept
Retrieval‑augmented generation combines a search component with a language model. Queries first retrieve relevant text passages from a knowledge base. Those passages are then used to generate a response, providing fresher and more grounded answers than a model alone. This demo mocks the generation step but illustrates the flow of uploading, embedding, retrieving, and summarizing documents.
