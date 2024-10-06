# from fastapi import APIRouter, HTTPException
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.llms.ollama import Ollama
# from .get_embeddings import get_embedding_function
# from pydantic import BaseModel

# router = APIRouter(
#     prefix="/ai",
#     tags=["ai"]
# )

# class QueryRequest(BaseModel):
#     query_text: str

# CHROMA_PATH = "chroma"
# PROMPT_TEMPLATE = """
# Answer the question based only on the following context:

# {context}

# ---

# Answer the question based on the above context: {question}
# """


# @router.post("/query_db")
# def query_chroma_db(request: QueryRequest):
#     """Query the Chroma DB for a specific question"""
#     try:
#         query_text = request.query_text

#         # Prepare the DB and embedding function
#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
#         # Search for the most relevant documents
#         results = db.similarity_search_with_score(query_text, k=5)
#         if not results:
#             return {"response": "No relevant documents found", "sources": []}

#         context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

#         # Prepare the prompt
#         prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#         prompt = prompt_template.format(context=context_text, question=query_text)

#         # Get response from LLM
#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)

#         # Get the sources of the information
#         sources = [doc.metadata.get("id", None) for doc, _score in results]
#         formatted_response = f"Response: {response_text}\nSources: {sources}"

#         return {"response": response_text, "sources": sources}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# from fastapi import APIRouter, HTTPException
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.llms.ollama import Ollama
# from .get_embeddings import get_embedding_function
# from pydantic import BaseModel

# router = APIRouter(
#     prefix="/ai",
#     tags=["ai"]
# )

# class QueryRequest(BaseModel):
#     query_text: str
#     file_name: str  # Field for file name input

# CHROMA_PATH = "chroma"
# prompt_template = ChatPromptTemplate.from_template("""
#             You are an assistant specialized in retrieving information from specific documents.
#             Below is the content from documents with the name "{document_name}". Use this content to answer the question.

#             Documents:
#             {context}

#             Question: {question}

#             Please provide an accurate and detailed response.
# """)


# # @router.post("/query_db")
# # def query_chroma_db(request: QueryRequest):
# #     """Query the Chroma DB for a specific question and file"""
# #     try:
# #         query_text = request.query_text
# #         file_name = request.file_name  # Retrieve the file name from the request

# #         # Prepare the DB and embedding function
# #         embedding_function = get_embedding_function()
# #         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
# #         # Search for the most relevant documents in the file
# #         results = db.similarity_search_with_score(f"file:{file_name} {query_text}", k=5)
# #         if not results:
# #             return {"response": f"No relevant documents found in file {file_name}", "sources": []}

# #         context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

# #         # Prepare the prompt
# #         prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
# #         prompt = prompt_template.format(context=context_text, question=query_text, file_name=file_name)

# #         # Get response from LLM
# #         model = Ollama(model="mistral")
# #         response_text = model.invoke(prompt)

# #         # Get the sources of the information
# #         sources = [doc.metadata.get("id", None) for doc, _score in results]
# #         formatted_response = f"Response: {response_text}\nSources: {sources}"

# #         return {"response": response_text, "sources": sources}

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/query_db")
# def query_chroma_db(request: QueryRequest):
#     """Query the Chroma DB for a specific question and document name"""
#     try:
#         query_text = request.query_text
#         document_name = request.document_name  # Extract the document name from the request

#         # Prepare the DB and embedding function
#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

#         # Perform the similarity search across all documents
#         all_results = db.similarity_search_with_score(query_text, k=5)

#         if not all_results:
#             return {"response": "No documents found in search", "sources": []}

#         # Debug: Print all results metadata to ensure documents are being found
#         print("All Results Metadata:")
#         for doc, score in all_results:
#             print(doc.metadata)

#         # Filter results by document name manually using the source field
#         filtered_results = [
#             (doc, score) for doc, score in all_results 
#             if doc.metadata.get("source", "").lower() == document_name.lower()
#         ]

#         if not filtered_results:
#             return {"response": "No relevant documents found after filtering by source", "sources": []}

#         context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in filtered_results])

#         # Prepare the prompt
#         prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#         prompt = prompt_template.format(context=context_text, question=query_text)

#         # Get response from LLM
#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)

#         # Get the sources of the information
#         sources = [doc.metadata.get("id", None) for doc, _score in filtered_results]
#         formatted_response = f"Response: {response_text}\nSources: {sources}"

#         return {"response": response_text, "sources": sources}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# from fastapi import APIRouter, HTTPException
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.llms.ollama import Ollama
# from .get_embeddings import get_embedding_function
# from pydantic import BaseModel

# router = APIRouter(
#     prefix="/ai",
#     tags=["ai"]
# )

# class QueryRequest(BaseModel):
#     query_text: str
#     file_name: str  # Field for file name input

# CHROMA_PATH = "chroma"
# PROMPT_TEMPLATE = """
#             You are an assistant specialized in retrieving information from specific documents.
#             Below is the content from documents with the name "{document_name}". Use this content to answer the question.

#             Documents:
#             {context}

#             Question: {question}

#             Please provide an accurate and detailed response.
# """

# prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# @router.post("/query_db")
# def query_chroma_db(request: QueryRequest):
#     """Query the Chroma DB for a specific question and document name"""
#     try:
#         query_text = request.query_text
#         document_name = request.file_name  # Ensure consistency with the field name

#         # Prepare the DB and embedding function
#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

#         # Perform the similarity search across all documents
#         all_results = db.similarity_search_with_score(query_text, k=5)

#         if not all_results:
#             return {"response": "No documents found in search", "sources": []}

#         # Filter results by document name
#         filtered_results = [
#             (doc, score) for doc, score in all_results 
#             if doc.metadata.get("source", "").lower() == document_name.lower()
#         ]

#         if not filtered_results:
#             return {"response": "No relevant documents found after filtering by source", "sources": []}

#         context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])

#         # Prepare the prompt
#         prompt = prompt_template.format(context=context_text, question=query_text)

#         # Get response from LLM
#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)

#         # Get the sources of the information
#         sources = [doc.metadata.get("id", None) for doc, _ in filtered_results]

#         return {"response": response_text, "sources": sources}

#     except Exception as e:
#         # You can log the error here for debugging purposes
#         raise HTTPException(status_code=500, detail=str(e))



# from fastapi import APIRouter, HTTPException
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_community.llms.ollama import Ollama
# from .get_embeddings import get_embedding_function
# from pydantic import BaseModel
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# router = APIRouter(
#     prefix="/ai",
#     tags=["ai"]
# )

# class QueryRequest(BaseModel):
#     query_text: str
#     file_name: str

# CHROMA_PATH = "chroma"
# PROMPT_TEMPLATE = """
#             You are an assistant specialized in retrieving information from specific documents.
#             Below is the content from documents with the name "{document_name}". Use this content to answer the question.

#             Documents:
#             {context}

#             Question: {question}

#             Please provide an accurate and detailed response.
# """

# prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# def tavily_search(query):
#     """Function to perform a Tavily search."""
#     api_key = redis_url = os.getenv("TAVILY_API_KEY")
#     url = f'https://api.tavily.com/search?query={query}'
    
#     headers = {
#         'Authorization': f'Bearer {api_key}'
#     }
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()  # Return the JSON response containing search results
#     else:
#         raise HTTPException(status_code=response.status_code, detail="Tavily search failed")

# @router.post("/query_db")
# def query_chroma_db(request: QueryRequest):
#     """Query the Chroma DB for a specific question and document name"""
#     try:
#         query_text = request.query_text
#         document_name = request.file_name

#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

#         all_results = db.similarity_search_with_score(query_text, k=5)

#         if not all_results:
#             return {"response": "No documents found in search", "sources": []}

#         # Filter results by document name
#         filtered_results = [
#             (doc, score) for doc, score in all_results 
#             if doc.metadata.get("source", "").lower() == document_name.lower()
#         ]

#         if not filtered_results:
#             # No relevant documents found; use Tavily to search the internet
#             tavily_results = tavily_search(query_text)
#             return {"response": "No relevant documents found. Here's what I found online.", "sources": tavily_results}

#         context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
#         prompt = prompt_template.format(context=context_text, question=query_text, document_name=document_name)

#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)

#         sources = [doc.metadata.get("id", None) for doc, _ in filtered_results]

#         return {"response": response_text, "sources": sources}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from .get_embeddings import get_embedding_function
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import traceback  # For stack trace debugging

load_dotenv()

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

class QueryRequest(BaseModel):
    query_text: str
    file_name: str

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
    You are an assistant specialized in retrieving information from specific documents.
    Below is the content from documents with the name "{document_name}". Use this content to answer the question as accurately as possible.

    Documents:
    {context}

    Question: {question}

    If the answer to the question is not explicitly stated in the documents, use external sources, such as Tavily, to provide additional information.
    Clearly indicate when information comes from the documents and when it comes from external sources.
    """


prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

def tavily_search(query):
    """Function to perform a Tavily search."""
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Tavily API key is missing")

        url = f'https://api.tavily.com/search?query={query}'
        headers = {
            'Authorization': f'Bearer {api_key}'
        }

        response = requests.get(url, headers=headers)
        print(f"Tavily API response status: {response.status_code}")
        print(f"Tavily API response content: {response.text}")  # For debugging

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Tavily search failed")
    except Exception as e:
        print("Error in Tavily search:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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
        if all_results:
            filtered_results = [
                (doc, score) for doc, score in all_results 
                if doc.metadata.get("source", "").lower() == document_name.lower()
            ]

            if filtered_results:
                context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
                print(f"Filtered {len(filtered_results)} results by document name.")
            else:
                print("No relevant documents found in Chroma.")
        else:
            print("No documents found in Chroma.")

        # Check if Chroma results are empty and call Tavily
        if not context_text:
            print("No Chroma results found. Performing Tavily search...")
            tavily_results = tavily_search(query_text)  # Call Tavily API
            print(f"Tavily returned {len(tavily_results)} results.")
            context_text = "\n\n---\n\n".join([res.get('snippet', '') for res in tavily_results])

        # Now pass Chroma and/or Tavily results to LLM
        prompt = prompt_template.format(context=context_text, question=query_text, document_name=document_name)
        print(f"Final Prompt:\n{prompt}")

        model = Ollama(model="mistral")
        response_text = model.invoke(prompt)
        print(f"Model response: {response_text}")

        sources = [doc.metadata.get("id", None) for doc, _ in filtered_results] if filtered_results else ["Tavily"]

        return {"response": response_text, "sources": sources}

    except Exception as e:
        print("Error in query_chroma_db:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
