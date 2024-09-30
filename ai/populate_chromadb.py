# populate_chromadb.py
from fastapi import APIRouter
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from get_embedding import get_embedding_function
from pathlib import Path
import os
import shutil

router = APIRouter()

CHROMA_PATH = "chroma"
COMMENTS_PATH = "amazon_comments"

@router.post("/populate_db", status_code=200)
def populate_chroma_db(reset: bool = False):
    """Endpoint to populate Chroma DB with PDFs from amazon_comments"""
    
    if reset:
        print("✨ Clearing Database")
        clear_database()

    # Load documents and split them
    documents = load_documents(COMMENTS_PATH)
    chunks = split_documents(documents)

    # Add to Chroma DB
    add_to_chroma(chunks)
    return {"message": "Database populated successfully."}


def load_documents(directory: str):
    document_loader = PyPDFDirectoryLoader(directory)
    return document_loader.load()


def split_documents(documents: list):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
    
    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id
        last_page_id = current_page_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
