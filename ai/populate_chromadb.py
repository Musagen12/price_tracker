from fastapi import APIRouter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from .get_embeddings import get_embedding_function
from pathlib import Path
import os
import shutil

router = APIRouter()

CHROMA_PATH = "chroma"
COMMENTS_PATH = "/teamspace/studios/this_studio/price_tracker/amazon_comments"

@router.post("/populate_db", status_code=200)
def populate_chroma_db(reset: bool = False):
    """Endpoint to populate Chroma DB with .txt files from amazon_comments"""
    try:
        if reset:
            print("✨ Clearing Database")
            clear_database()

        # Load text documents and split them
        documents = load_text_documents(COMMENTS_PATH)
        if not documents:
            return {"message": "No documents found to load"}

        chunks = split_documents(documents)

        # Add to Chroma DB
        add_to_chroma(chunks)
        return {"message": "Database populated successfully."}

    except Exception as e:
        print(f"Error populating database: {e}")
        return {"message": f"Error populating database: {str(e)}"}

def load_text_documents(directory: str):
    """Load all .txt files from the specified directory."""
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                # Each text is stored as a Document object
                documents.append(Document(
                    page_content=text, 
                    metadata={"source": filename}
                ))
    return documents

def split_documents(documents: list):
    """Split documents into chunks using RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list):
    """Convert the chunks into embeddings then store them in chromadb a vector database."""
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    chunks_with_ids = calculate_chunk_ids(chunks)
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    
    print(f"Number of existing documents in DB: {len(existing_ids)}")  # Debug existing items

    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
    
    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")  # Debug added documents
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    """Assign unique IDs to each chunk based on source and chunk index."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        current_page_id = f"{source}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id
        last_page_id = current_page_id

    return chunks


def clear_database():
    """Clear the existing Chroma database."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    print("🧹 Chroma database cleared.")