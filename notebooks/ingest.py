import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env in project root
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

# New index name because the vector dimensions are different
INDEX_NAME = "uae-legal-assistant-free" 

def ingest_pdfs():
    data_folder = str(project_root / "data")
    print(f"Loading PDFs from: {data_folder}...")
    
    loader = PyPDFDirectoryLoader(data_folder)
    documents = loader.load()
    
    if not documents:
        print("No PDFs found. Check the folder path and try again.")
        return

    print(f"Loaded {len(documents)} document pages. Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    print(f"Created {len(chunks)} text chunks. Connecting to Pinecone...")
    
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index: {INDEX_NAME}...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,  # Matches all-MiniLM-L6-v2 dimensions
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("Index created successfully.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

    print("Downloading local embedding model (this only happens once)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Embedding and uploading chunks to Pinecone...")
    PineconeVectorStore.from_documents(chunks, embeddings, index_name=INDEX_NAME)
    print("Ingestion complete. The vector database is live!")

if __name__ == "__main__":
    ingest_pdfs()