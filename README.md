# ⚖️ UAE Legal Assistant: Multi-Agent RAG System

A portfolio-grade, cross-platform Multi-Agent Retrieval-Augmented Generation (RAG) system built to query and synthesize United Arab Emirates (UAE) Federal Labor Law and Data Protection Law.

This project utilizes a cyclic LangGraph architecture with a built-in strict fact-checking node to detect and mitigate LLM hallucinations autonomously. It is optimized for zero-cost operation using local Hugging Face embeddings and OpenRouter's free tier dynamic routing.

## 🏗️ System Architecture

The pipeline is built using **LangGraph** to manage the state and routing between three specialized AI agents. If the Fact-Checker detects unsupported claims, a conditional edge loops the process back to the Synthesizer for correction before delivering the final answer to the user.

### Backend Pipeline (LangGraph)

1. **Retriever Node:** Converts the user query into vector embeddings and retrieves the top-K relevant chunks from a Pinecone vector database.
2. **Synthesizer Node:** Takes the retrieved context and user query to draft a comprehensive, legally grounded answer.
3. **Fact-Checker Node:** Acts as a strict boolean gatekeeper. It evaluates the Synthesizer's draft against the raw retrieved context. If hallucinations or contradictions are detected, it forces a retry loop (capped at 5 recursions).

### Frontend Architecture

The frontend is built with **Streamlit** using a **modular component-based structure** for maintainability and scalability:

- **`styling.py`** – Custom CSS theming, page configuration, and header rendering
- **`chat_history.py`** – Conversation persistence with save/load functionality and session state management
- **`sidebar.py`** – Sidebar UI with FAQ, settings, conversation management, and about section
- **`utils.py`** – Shared utility functions for API calls and message formatting
- **`__init__.py`** – Clean exports for all components

This modular approach keeps `app.py` clean (~100 lines) and makes the codebase easy to extend.

## 🛠️ Tech Stack

* **Framework:** LangGraph, LangChain
* **Frontend:** Streamlit (with modular components)
* **Vector Database:** Pinecone (Serverless)
* **Embeddings:** Hugging Face `all-MiniLM-L6-v2` (Local, 384-dimensions)
* **LLM Engine:** OpenRouter (`openrouter/free` dynamic auto-routing via Mistral-7B)
* **Document Processing:** PyPDF, RecursiveCharacterTextSplitter
* **Environment:** Python 3.10+

## 🚀 Installation & Setup

### 1. Clone the Repository
```powershell
git clone https://github.com/MalaikaJunaid/multi-agent-rag-assistant.git
cd multi-agent-rag-assistant
```

### 2. Set Up the Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory and add your API keys:

```text
OPENROUTER_API_KEY="your_openrouter_key_here"
PINECONE_API_KEY="your_pinecone_key_here"
PINECONE_INDEX_NAME="uae-legal-assistant-free"
HF_TOKEN="your_huggingface_token_here" # Optional, removes download warnings
```

### 4. Ingest Legal Data

Before running the application, embed the PDF documents and upload them to your Pinecone index:

```powershell
python notebooks/ingest.py
```

Or use the **in-app PDF uploader** in the sidebar to add documents on-the-fly.

### 5. Launch the Application

Start the Streamlit frontend interface to interact with the multi-agent pipeline:

```powershell
streamlit run frontend/app.py
```

The app will be available at `http://localhost:8501`

## 💡 Key Features

### Core Features
* **Zero-Cost Scalability:** By swapping OpenAI embeddings for local Hugging Face models and utilizing OpenRouter's dynamic free tier, the entire ingestion and inference pipeline costs $0 to operate.
* **Hallucination Mitigation:** The autonomous Fact-Checker node ensures that only verifiable information extracted directly from the UAE legal text is presented to the user.
* **Source Transparency:** The frontend UI includes interactive expanders allowing users to view the exact legal text chunks the AI referenced to generate its answer.

### Frontend Features
* **📄 PDF Upload:** Users can upload their own legal documents directly from the sidebar for real-time knowledge base expansion
* **💬 Chat History:** Persistent conversation storage with the ability to load, export, and manage previous chats
* **⚙️ Configurable Settings:** Adjust LLM temperature and verification retry limits from the sidebar
* **📋 Pre-loaded FAQs:** Quick-select buttons for common legal questions with category filtering
* **🎨 Professional UI/UX:** Dark-themed sidebar, custom CSS styling, and responsive layout
* **📥 Conversation Export:** Download chat history as markdown files
* **⚠️ Graceful Error Handling:** User-friendly error messages instead of technical backend traces

### Backend Features
* **Modular Architecture:** Decoupled `backend/` module makes it trivial to expose via FastAPI endpoints for mobile or enterprise platform integration
* **Cyclic Fact-Checking Loop:** Autonomous retry mechanism (up to 5 cycles) ensures answer accuracy
* **LangGraph State Management:** Robust handling of query, documents, synthesis, and fact-checking states

## 📊 Project Structure

```
multi-agent-rag-assistant/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create locally)
│
├── backend/
│   ├── main.py               # LangGraph application entry point
│   ├── agents/
│   │   ├── state.py          # Shared AgentState schema
│   │   ├── retriever.py      # Vector retrieval node
│   │   ├── synthesizer.py    # LLM synthesis node
│   │   └── fact_checker.py   # Fact-checking node with Pydantic output
│   ├── api/                  # FastAPI routes (future expansion)
│   └── core/                 # Core utilities (future expansion)
│
├── frontend/
│   ├── app.py                # Streamlit main app (clean orchestration)
│   └── components/
│       ├── __init__.py       # Component exports
│       ├── styling.py        # CSS and page configuration
│       ├── chat_history.py   # Conversation persistence
│       ├── sidebar.py        # Sidebar UI and settings
│       └── utils.py          # Shared utility functions
│
├── notebooks/
│   └── ingest.py             # PDF embedding and Pinecone ingestion script
│
└── data/
    └── (PDF legal documents stored here)
```

## 🔄 How It Works

### User Query Flow

1. **User Input** → Chat input in Streamlit frontend
2. **Query Routing** → Sent to LangGraph application
3. **Retrieval** → Vector embedding lookup in Pinecone
4. **Synthesis** → LLM generates answer based on retrieved context
5. **Fact-Checking** → Strict validation against source documents
6. **Retry Loop** → If hallucination detected, loop back to Synthesizer (max 5 times)
7. **Final Answer** → Delivered to user with source transparency

### PDF Upload Flow

1. **User Upload** → PDF file selected in sidebar
2. **Text Extraction** → PyPDF extracts pages
3. **Chunking** → RecursiveCharacterTextSplitter creates overlapping chunks
4. **Embedding** → HuggingFace `all-MiniLM-L6-v2` generates embeddings
5. **Storage** → Chunks stored in Pinecone vector database
6. **Success Confirmation** → User sees success message with chunk count

## 🧪 Testing

To test a single query without the full UI:

```powershell
python -m backend.main
```

This runs the test query defined in `backend/main.py`:
```
"What is the maximum probation period for an employee under UAE law?"
```

## 🤝 Contributing

Contributions are welcome! Areas for expansion:

- [ ] FastAPI backend for REST endpoints
- [ ] Mobile-friendly React frontend
- [ ] Multi-language support
- [ ] Document export functionality
- [ ] User authentication and role-based access
- [ ] Advanced analytics and usage tracking

## ⚖️ Legal Disclaimer

This tool is designed for **informational purposes only**. It does not constitute legal advice. Users should consult official UAE government resources or qualified legal professionals for critical decisions related to labor law or data protection.

## 📝 License

This project is open-source. Please refer to the LICENSE file for details.

## 👤 Author

**Malaika Junaid** – Portfolio project demonstrating enterprise-grade RAG architecture.

---

**Last Updated:** September 2026
