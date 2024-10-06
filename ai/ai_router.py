# from fastapi import APIRouter, HTTPException
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.llms.ollama import Ollama
# from .get_embeddings import get_embedding_function
# from pydantic import BaseModel
# import requests
# import os
# from dotenv import load_dotenv
# import traceback  # For stack trace debugging

# load_dotenv()

# router = APIRouter(
#     prefix="/ai",
#     tags=["ai"]
# )

# class QueryRequest(BaseModel):
#     query_text: str
#     file_name: str

# # Chroma database path
# CHROMA_PATH = "chroma"

# # Modified prompt template to handle both Chroma and Tavily data
# PROMPT_TEMPLATE = """
# You are an assistant specialized in retrieving information from specific documents.
# Below is the content from documents with the name "{document_name}". Use this content to answer the question as accurately as possible.

# Documents from Chroma:
# {chroma_context}

# External sources (Tavily):
# {tavily_context}

# Question: {question}

# If the answer to the question is not explicitly stated in the documents, use the external sources (Tavily) to provide additional information. Always prefer the latest information from external sources over any potentially outdated internal knowledge. Clearly indicate when information comes from the documents and when it comes from external sources.
# """

# prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# def tavily_search(query):
#     """Function to perform a Tavily search."""
#     try:
#         api_key = os.getenv("TAVILY_API_KEY")
#         if not api_key:
#             raise HTTPException(status_code=500, detail="Tavily API key is missing")

#         url = 'https://api.tavily.com/search'
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#             'Content-Type': 'application/json'
#         }

#         data = {
#             'api_key': api_key,
#             'query': query,
#         }

#         print(f"Sending request to Tavily with body: {data}")

#         response = requests.post(url, headers=headers, json=data)

#         print(f"Tavily API response status: {response.status_code}")
#         print(f"Tavily API response content: {response.text}")

#         if response.status_code == 200:
#             return response.json()
#         else:
#             try:
#                 error_response = response.json()
#                 error_detail = error_response.get('detail', 'No further information provided.')
#             except ValueError:
#                 error_detail = response.text

#             raise HTTPException(status_code=response.status_code, detail=f"Tavily search failed: {error_detail}")

#     except Exception as e:
#         print("Error in Tavily search:", str(e))
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/query_db")
# def query_chroma_db(request: QueryRequest):
#     """Query the Chroma DB for a specific question and document name"""
#     try:
#         query_text = request.query_text
#         document_name = request.file_name

#         print(f"Received query: {query_text}, document name: {document_name}")

#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
#         all_results = db.similarity_search_with_score(query_text, k=5)

#         print(f"Chroma returned {len(all_results)} results.")

#         context_text = ""
#         filtered_results = []
#         if all_results:
#             filtered_results = [
#                 (doc, score) for doc, score in all_results 
#                 if isinstance(doc.metadata, dict) and 
#                 doc.metadata.get("source", "").lower() == document_name.lower() and 
#                 "2024" in doc.page_content
#             ]

#             if filtered_results:
#                 context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
#                 print(f"Filtered {len(filtered_results)} results with the year 2024.")
#             else:
#                 print("No relevant 2024 documents found in Chroma.")
#         else:
#             print("No documents found in Chroma.")

#         if not context_text:
#             print("No 2024 results found in Chroma. Performing Tavily search...")
#             tavily_results = tavily_search(query_text)

#             print(f"Raw Tavily response: {tavily_results}")

#             if isinstance(tavily_results, list):
#                 context_text = "\n\n---\n\n".join([res.get('snippet', '') for res in tavily_results if isinstance(res, dict)])

#         if not context_text:
#             context_text = "No relevant data was found in the provided documents or external sources."

#         print("Chroma context before formatting:", context_text)  # Debugging statement
#         print("Query text before formatting:", query_text)  # Debugging statement
#         print("Document name before formatting:", document_name)  # Debugging statement

#         try:
#             prompt = prompt_template.format(chroma_context=context_text, question=query_text, document_name=document_name, tavily_context=tavily_results)
#             print(f"Final Prompt:\n{prompt}")
#         except Exception as e:
#             print(f"Error formatting the prompt: {e}")
#             raise HTTPException(status_code=500, detail="Error formatting the prompt.")

#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)
#         print(f"Model response: {response_text}")

#         sources = [doc.metadata.get("id", None) for doc, _ in filtered_results if isinstance(doc.metadata, dict)] if filtered_results else ["Tavily"]

#         return {"response": response_text, "sources": sources, "tavily_raw": tavily_results}

#     except Exception as e:
#         print("Error in query_chroma_db:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))


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