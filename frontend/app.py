import streamlit as st
import sys
import os
import tempfile
from pathlib import Path
from langgraph.errors import GraphRecursionError

# Add project root to the system path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.main import app as graph_app
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

# --- Page Configuration ---
st.set_page_config(page_title="UAE Legal Assistant", page_icon="⚖️", layout="centered")
st.title("⚖️ UAE Legal Assistant")
st.markdown("Ask questions about UAE Federal Labor Law and Data Protection Law, or upload your own documents.")

# --- Sidebar Components ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("This assistant uses a Multi-Agent RAG pipeline with local Hugging Face embeddings and free OpenRouter LLMs.")
    
    st.divider()
    
    # --- NEW: PDF Uploader ---
    st.subheader("📄 Upload New Document")
    uploaded_file = st.file_uploader("Add a PDF to the knowledge base", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Process & Ingest PDF", use_container_width=True):
            with st.spinner("Embedding and uploading to Pinecone..."):
                try:
                    # 1. Save uploaded file temporarily to disk
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # 2. Load, extract, and split the PDF
                    loader = PyPDFLoader(tmp_file_path)
                    documents = loader.load()
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                    chunks = text_splitter.split_documents(documents)
                    
                    # 3. Embed and push to your existing Pinecone index
                    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                    PineconeVectorStore.from_documents(
                        chunks, 
                        embeddings, 
                        index_name="uae-legal-assistant-free"
                    )
                    
                    st.success(f"✅ Successfully added {len(chunks)} text chunks to the database!")
                except Exception as e:
                    st.error(f"Error during ingestion: {str(e)}")
                finally:
                    # 4. Clean up the temporary file to prevent storage bloat
                    if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                        os.remove(tmp_file_path)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Chat Interface ---
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages and their retrieved sources
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📄 View Referenced Legal Text"):
                for idx, doc in enumerate(message["sources"]):
                    st.info(f"**Chunk {idx+1}:**\n\n{doc}")

# Accept user input
if prompt := st.chat_input("E.g., What are the rules for annual leave?"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching legal documents and checking facts..."):
            initial_state = {
                "query": prompt,
                "messages": [],
                "retrieved_documents": [],
                "synthesis": "",
                "is_factually_correct": False
            }
            
            try:
                final_state = graph_app.invoke(initial_state, config={"recursion_limit": 5})
                answer = final_state["synthesis"]
                sources = final_state.get("retrieved_documents", [])
                
                st.markdown(answer)
                
                if sources:
                    with st.expander("📄 View Referenced Legal Text"):
                        for idx, doc in enumerate(sources):
                            st.info(f"**Chunk {idx+1}:**\n\n{doc}")
                            
            except Exception as e:
                error_msg = str(e)
                if "Recursion limit" in error_msg:
                    answer = "⚠️ **Verification Failed:** The AI models could not synthesize a strictly verified answer within the retry limit. This occasionally happens with free routing models. Please try rephrasing your question."
                else:
                    answer = f"⚠️ **System Error:** {error_msg}"
                
                sources = []
                st.error(answer)
            
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})