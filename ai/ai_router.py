from fastapi import APIRouter, HTTPException
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from .get_embeddings import get_embedding_function
from pydantic import BaseModel

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

class QueryRequest(BaseModel):
    query_text: str
    file_name: str

# Chroma database path
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an assistant specialized in retrieving information from specific documents.
Below is the content from documents with the name "{document_name}". Use this content to answer the question as accurately as possible.

Documents from Chroma:
{chroma_context}

Question: {question}

If the answer to the question is not explicitly stated in the documents, clearly indicate that the answer could not be found in the available documents.
"""

prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

@router.post("/query_db")
def query_chroma_db(request: QueryRequest):
    """Query the Chroma DB for a specific question and document name"""
    try:
        query_text = request.query_text
        document_name = request.file_name

        print(f"Received query: {query_text}, document name: {document_name}")

        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        all_results = db.similarity_search_with_score(query_text, k=5)

        print(f"Chroma returned {len(all_results)} results.")

        context_text = ""
        filtered_results = []
        if all_results:
            filtered_results = [
                (doc, score) for doc, score in all_results 
                if isinstance(doc.metadata, dict) and 
                doc.metadata.get("source", "").lower() == document_name.lower()
            ]

            if filtered_results:
                context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
                print(f"Filtered {len(filtered_results)} results.")
            else:
                print("No relevant documents found in Chroma.")
        else:
            print("No documents found in Chroma.")

        if not context_text:
            context_text = "No relevant data was found in the provided documents."

        print("Chroma context before formatting:", context_text)  # Debugging statement
        print("Query text before formatting:", query_text)  # Debugging statement
        print("Document name before formatting:", document_name)  # Debugging statement

        try:
            prompt = prompt_template.format(chroma_context=context_text, question=query_text, document_name=document_name)
            print(f"Final Prompt:\n{prompt}")
        except Exception as e:
            print(f"Error formatting the prompt: {e}")
            raise HTTPException(status_code=500, detail="Error formatting the prompt.")

        model = OllamaLLM(model="mistral")
        response_text = model.invoke(prompt)
        print(f"Model response: {response_text}")

        sources = [doc.metadata.get("id", None) for doc, _ in filtered_results if isinstance(doc.metadata, dict)] if filtered_results else ["No relevant documents found"]

        return {"response": response_text, "sources": sources}

    except Exception as e:
        print("Error in query_chroma_db:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
