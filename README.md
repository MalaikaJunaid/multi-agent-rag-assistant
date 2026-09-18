# ⚖️ UAE Legal Assistant: Multi-Agent RAG System

A portfolio-grade, cross-platform Multi-Agent Retrieval-Augmented Generation (RAG) system built to query and synthesize United Arab Emirates (UAE) Federal Labor Law and Data Protection Law. 

This project utilizes a cyclic LangGraph architecture with a built-in strict fact-checking node to detect and mitigate LLM hallucinations autonomously. It is optimized for zero-cost operation using local Hugging Face embeddings and OpenRouter's free tier dynamic routing.

## 🏗️ System Architecture

The pipeline is built using **LangGraph** to manage the state and routing between three specialized AI agents. If the Fact-Checker detects unsupported claims, a conditional edge loops the process back to the Synthesizer for correction before delivering the final answer to the user.

1. **Retriever Node:** Converts the user query into vector embeddings and retrieves the top-K relevant chunks from a Pinecone vector database.
2. **Synthesizer Node:** Takes the retrieved context and user query to draft a comprehensive, legally grounded answer.
3. **Fact-Checker Node:** Acts as a strict boolean gatekeeper. It evaluates the Synthesizer's draft against the raw retrieved context. If hallucinations or contradictions are detected, it forces a retry loop (capped at 5 recursions).

## 🛠️ Tech Stack

* **Framework:** LangGraph, LangChain
* **Frontend:** Streamlit
* **Vector Database:** Pinecone (Serverless)
* **Embeddings:** Hugging Face `all-MiniLM-L6-v2` (Local, 384-dimensions)
* **LLM Engine:** OpenRouter (`openrouter/free` dynamic auto-routing)
* **Environment:** Python 3.10+

## 🚀 Installation & Setup

### 1. Clone the Repository
```powershell
git clone [https://github.com/MalaikaJunaid/multi-agent-rag-assistant.git](https://github.com/MalaikaJunaid/multi-agent-rag-assistant.git)
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
HF_TOKEN="your_huggingface_token_here" # Optional, removes download warnings

```

### 4. Ingest Legal Data

Before running the application, you must embed the PDF documents in the `data/` folder and upload them to your Pinecone index.

```powershell
python notebooks/ingest.py

```

### 5. Launch the Application

Start the Streamlit frontend interface to interact with the multi-agent pipeline.

```powershell
streamlit run frontend/app.py

```

## 💡 Key Features

* **Zero-Cost Scalability:** By swapping OpenAI embeddings for local Hugging Face models and utilizing OpenRouter's dynamic free tier, the entire ingestion and inference pipeline costs $0 to operate.
* **Hallucination Mitigation:** The autonomous Fact-Checker node ensures that only verifiable information extracted directly from the UAE legal text is presented to the user.
* **Source Transparency:** The frontend UI includes interactive expanders allowing users to view the exact legal text chunks the AI referenced to generate its answer.
* **Modular Backend:** The architecture is decoupled into a dedicated `backend/` module, making it trivial to expose via FastAPI endpoints in the future for mobile or enterprise platform integration.
