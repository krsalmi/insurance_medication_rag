# 'Grammarly for Doctors' backend

This is the backend server for an app we referred to as "Grammarly for Doctors", a hackathon project that helps physicians automatically adapt prescription texts so they meet insurance criteria.
The system suggests minimal edits to ensure prescriptions are valid for insurance reimbursement, while keeping the doctor’s intent intact.

## Features

* Flask API server with a `/api/generate` endpoint.
* Integrates with LlamaIndex and OpenAI GPT models.
* Uses PDF medical documents (insurance rules, drug approval criteria, etc.) as a knowledge base.
* Returns proposed edits to prescription text, with changes highlighted in square brackets `[like this]`.
* Supports document-level vector search + summarization tools for reasoning over multiple papers.

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Flask** (API server, CORS enabled)
* **LlamaIndex** (document indexing + agent framework)
* **OpenAI API** (LLM + embeddings)
* **PDF-based retrieval** (vector search + summarization over docs/)

---

## ⚡ Getting Started

### 1. Clone this repo

### 2. Set up a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root:

```
OPENAI_API_KEY=your_api_key_here
```

### 5. Add reference documents

Put any PDF files with insurance / prescription criteria into the `docs/` folder.
These will be indexed at startup.

### 6. Run the server

```bash
python app.py
```

The API will start on `http://localhost:3000`.

---

## 📡 API Usage

### Endpoint: `POST /api/generate`

**Request JSON**

```json
{
  "text": "Insurance: Anthem, Medication: Humira, Disease: Rheumatoid Arthritis, Prescription text: ..."
}
```

**Response JSON**

```json
{
  "output": "Modified prescription text with [necessary edits]"
}
```

If the input does not meet criteria, the agent proposes edits inside `[ ]` brackets.
