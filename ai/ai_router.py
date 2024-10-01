# query.py
from fastapi import APIRouter, HTTPException
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from .get_embeddings import get_embedding_function
from pydantic import BaseModel

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

class QueryRequest(BaseModel):
    query_text: str

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


@router.post("/query_db")
def query_chroma_db(request: QueryRequest):
    """Query the Chroma DB for a specific question"""
    try:
        query_text = request.query_text

        # Prepare the DB and embedding function
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Search for the most relevant documents
        results = db.similarity_search_with_score(query_text, k=5)
        if not results:
            return {"response": "No relevant documents found", "sources": []}

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        # Prepare the prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        # Get response from LLM
        model = Ollama(model="mistral")
        response_text = model.invoke(prompt)

        # Get the sources of the information
        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"

        return {"response": response_text, "sources": sources}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
