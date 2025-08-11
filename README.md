## FlipQuery — PDF RAG Chatbot

Upload a PDF and chat with its contents. This app performs Retrieval-Augmented Generation (RAG) using sentence-transformers for embeddings, Pinecone for vector search, and Google Gemini for answer generation. A simple Flask UI is included.

### Features
- **PDF upload**: Extracts text with PyPDF2 and splits into chunks
- **Embeddings**: `all-MiniLM-L6-v2` via sentence-transformers
- **Vector DB**: Pinecone for similarity search
- **LLM**: Gemini 2.5 Flash (`google-genai`)
- **UI**: Clean web UI at `/` with drag-and-drop upload and chat

### Tech Stack
- Backend: Flask (Python)
- Embeddings: sentence-transformers (`all-MiniLM-L6-v2`, 384-dim)
- Vector DB: Pinecone
- LLM: Google Gemini (via `google-genai`)
- PDF: PyPDF2

### Project Structure
```
basic_context_chatbot/
  app.py
  routes/          # API endpoints: upload, query
  rag_utils/       # PDF processing, vectorization, Pinecone, LLM
  utils/           # logging, validation, helpers
  templates/       # UI (index.html)
  static/          # CSS
  uploads/         # temp storage (auto-created)
```

### Prerequisites
- Python 3.10+
- Pinecone account and an index (recommended dimension: 384)
- Google AI Studio API key (Gemini)

### Setup
1) Clone and install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2) Configure environment variables (create a `.env` in the project root)
```env
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=your_index_name
GEMINI_API_KEY=your_gemini_key
```

Notes:
- The app will query Pinecone to detect the index dimension. If it can’t, it defaults to 384 and pads vectors to match the index dimension.
- Ensure your Pinecone index exists and is compatible with 384-d embeddings (recommended).

3) Run the app
```bash
python app.py
```
Open `http://localhost:5000` and use the UI to upload a PDF and start chatting.

### API
- Health
```bash
curl http://localhost:5000/health
```

- Upload PDF
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@/path/to/document.pdf"
```
Response:
```json
{ "message": "PDF uploaded and processed successfully", "doc_id": "...", "filename": "...", "chunks_created": 12 }
```

- Query
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main conclusion?", "doc_id": "<doc_id from upload>"}'
```
Response:
```json
{ "answer": "...", "query": "...", "sources": 5 }
```

### Troubleshooting
- Missing or invalid keys: verify `.env` values (`PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `GEMINI_API_KEY`).
- Pinecone errors (index not found/unauthorized): ensure the index exists and your key has access.
- First run is slow: the `sentence-transformers` model download can take a minute.

---


