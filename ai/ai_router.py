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

# CHROMA_PATH = "chroma"
# PROMPT_TEMPLATE = """
#     You are an assistant specialized in retrieving information from specific documents.
#     Below is the content from documents with the name "{document_name}". Use this content to answer the question as accurately as possible.

#     Documents:
#     {context}

#     Question: {question}

#     If the answer to the question is not explicitly stated in the documents, use external sources, such as Tavily, to provide additional information.
#     Clearly indicate when information comes from the documents and when it comes from external sources.
#     """


# prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# def tavily_search(query):
#     """Function to perform a Tavily search."""
#     try:
#         api_key = os.getenv("TAVILY_API_KEY")
#         if not api_key:
#             raise HTTPException(status_code=500, detail="Tavily API key is missing")

#         url = f'https://api.tavily.com/search?query={query}'
#         headers = {
#             'Authorization': f'Bearer {api_key}'
#         }

#         response = requests.get(url, headers=headers)
#         print(f"Tavily API response status: {response.status_code}")
#         print(f"Tavily API response content: {response.text}")  # For debugging

#         if response.status_code == 200:
#             return response.json()
#         else:
#             raise HTTPException(status_code=response.status_code, detail="Tavily search failed")
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
#         if all_results:
#             filtered_results = [
#                 (doc, score) for doc, score in all_results 
#                 if doc.metadata.get("source", "").lower() == document_name.lower()
#             ]

#             if filtered_results:
#                 context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
#                 print(f"Filtered {len(filtered_results)} results by document name.")
#             else:
#                 print("No relevant documents found in Chroma.")
#         else:
#             print("No documents found in Chroma.")

#         # Check if Chroma results are empty and call Tavily
#         if not context_text:
#             print("No Chroma results found. Performing Tavily search...")
#             tavily_results = tavily_search(query_text)  # Call Tavily API
#             print(f"Tavily returned {len(tavily_results)} results.")
#             context_text = "\n\n---\n\n".join([res.get('snippet', '') for res in tavily_results])

#         # Now pass Chroma and/or Tavily results to LLM
#         prompt = prompt_template.format(context=context_text, question=query_text, document_name=document_name)
#         print(f"Final Prompt:\n{prompt}")

#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)
#         print(f"Model response: {response_text}")

#         sources = [doc.metadata.get("id", None) for doc, _ in filtered_results] if filtered_results else ["Tavily"]

#         return {"response": response_text, "sources": sources}

#     except Exception as e:
#         print("Error in query_chroma_db:", str(e))
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
# import traceback  # For stack trace debugging

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
#     You are an assistant specialized in retrieving information from specific documents.
#     Below is the content from documents with the name "{document_name}". Use this content to answer the question as accurately as possible.

#     Documents:
#     {context}

#     Question: {question}

#     If the answer to the question is not explicitly stated in the documents, use external sources, such as Tavily, to provide additional information.
#     Clearly indicate when information comes from the documents and when it comes from external sources.
# """

# prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# def tavily_search(query):
#     """Function to perform a Tavily search."""
#     try:
#         api_key = os.getenv("TAVILY_API_KEY")
#         if not api_key:
#             raise HTTPException(status_code=500, detail="Tavily API key is missing")

#         url = f'https://api.tavily.com/search?query={query}'
#         headers = {
#             'Authorization': f'Bearer {api_key}'
#         }

#         response = requests.get(url, headers=headers)
#         print(f"Tavily API response status: {response.status_code}")
#         print(f"Tavily API response content: {response.text}")  # For debugging

#         if response.status_code == 200:
#             return response.json()
#         else:
#             raise HTTPException(status_code=response.status_code, detail="Tavily search failed")
#     except Exception as e:
#         print("Error in Tavily search:", str(e))
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Tavily search failed: {str(e)}")

# @router.post("/query_db")
# def query_chroma_db(request: QueryRequest):
#     """Query the Chroma DB for a specific question and document name"""
#     try:
#         query_text = request.query_text
#         document_name = request.file_name

#         print(f"Received query: {query_text}, document name: {document_name}")

#         # Fetch embeddings and query Chroma DB
#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
#         all_results = db.similarity_search_with_score(query_text, k=5)

#         print(f"Chroma returned {len(all_results)} results.")

#         # Filter Chroma results by document name and prepare the context
#         context_text = ""
#         if all_results:
#             filtered_results = [
#                 (doc, score) for doc, score in all_results 
#                 if doc.metadata.get("source", "").lower() == document_name.lower()
#             ]

#             if filtered_results:
#                 context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
#                 print(f"Filtered {len(filtered_results)} results by document name.")
#             else:
#                 print("No relevant documents found in Chroma.")
#         else:
#             print("No documents found in Chroma.")

#         # If no Chroma results, perform Tavily search
#         if not context_text:
#             print("No Chroma results found. Performing Tavily search...")
#             tavily_results = tavily_search(query_text)  # Call Tavily API
#             if tavily_results:
#                 print(f"Tavily returned {len(tavily_results)} results.")
#                 context_text = "\n\n---\n\n".join([res.get('snippet', '') for res in tavily_results])

#         # Check if no content from Chroma or Tavily
#         if not context_text:
#             return {"response": "No relevant information found in either Chroma or Tavily.", "sources": []}

#         # Now pass Chroma and/or Tavily results to LLM
#         prompt = prompt_template.format(context=context_text, question=query_text, document_name=document_name)
#         print(f"Final Prompt:\n{prompt}")

#         # Query LLM with prompt
#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)
#         print(f"Model response: {response_text}")

#         # Collect sources
#         sources = [doc.metadata.get("id", None) for doc, _ in filtered_results] if filtered_results else ["Tavily"]

#         return {"response": response_text, "sources": sources}

#     except Exception as e:
#         print("Error in query_chroma_db:", str(e))
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

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

# # Prompt template for the LLM
# PROMPT_TEMPLATE = """
# You are an assistant specialized in retrieving information from specific documents.
# Below is the content from documents with the name "{document_name}". Use this content to answer the question as accurately as possible.

# Documents:
# {context}

# Question: {question}

# If the answer to the question is not explicitly stated in the documents, use external sources, such as Tavily, to provide additional information.
# Clearly indicate when information comes from the documents and when it comes from external sources.
# """

# # Create the prompt template instance
# prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# def tavily_search(query):
#     """Function to perform a Tavily search."""
#     try:
#         api_key = os.getenv("TAVILY_API_KEY")
#         if not api_key:
#             raise HTTPException(status_code=500, detail="Tavily API key is missing")

#         # Tavily API URL
#         url = 'https://api.tavily.com/search'

#         headers = {
#             'Authorization': f'Bearer {api_key}',  # This may still be needed for other parts of the API
#             'Content-Type': 'application/json'
#         }

#         # Prepare the request body with required parameters
#         data = {
#             'api_key': api_key,  # Include api_key in the body
#             'query': query,
#         }

#         print(f"Sending request to Tavily with body: {data}")

#         # Make a POST request with JSON data
#         response = requests.post(url, headers=headers, json=data)

#         print(f"Tavily API response status: {response.status_code}")
#         print(f"Tavily API response content: {response.text}")  # Log response for debugging

#         if response.status_code == 200:
#             return response.json()  # Ensure this returns a JSON object
#         else:
#             # Try to parse the response as JSON, and handle it accordingly
#             try:
#                 error_response = response.json()  # Attempt to parse JSON
#                 error_detail = error_response.get('detail', 'No further information provided.')
#             except ValueError:  # Catch if the response is not valid JSON
#                 error_detail = response.text  # Fallback to raw response text

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

#         # Retrieve the embedding function and connect to Chroma DB
#         embedding_function = get_embedding_function()
#         db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
#         all_results = db.similarity_search_with_score(query_text, k=5)

#         print(f"Chroma returned {len(all_results)} results.")

#         context_text = ""
#         if all_results:
#             # Filter results by document name and check if the document mentions 2024
#             filtered_results = [
#                 (doc, score) for doc, score in all_results 
#                 if doc.metadata.get("source", "").lower() == document_name.lower() and "2024" in doc.page_content
#             ]

#             if filtered_results:
#                 context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
#                 print(f"Filtered {len(filtered_results)} results with the year 2024.")
#             else:
#                 print("No relevant 2024 documents found in Chroma.")
#         else:
#             print("No documents found in Chroma.")

#         # If no relevant 2024 context was found in Chroma, perform a Tavily search
#         if not context_text:
#             print("No 2024 results found in Chroma. Performing Tavily search...")
#             tavily_results = tavily_search(query_text)  # Call Tavily API
#             print(f"Tavily returned {len(tavily_results)} results.")
#             context_text = "\n\n---\n\n".join([res.get('snippet', '') for res in tavily_results])

#         # Prepare the final prompt for the LLM
#         prompt = prompt_template.format(context=context_text, question=query_text, document_name=document_name)
#         print(f"Final Prompt:\n{prompt}")

#         # Invoke the local LLM
#         model = Ollama(model="mistral")
#         response_text = model.invoke(prompt)
#         print(f"Model response: {response_text}")

#         # Determine sources for the response
#         sources = [doc.metadata.get("id", None) for doc, _ in filtered_results] if filtered_results else ["Tavily"]

#         return {"response": response_text, "sources": sources}

#     except Exception as e:
#         print("Error in query_chroma_db:", str(e))
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

# Chroma database path
CHROMA_PATH = "chroma"

# Prompt template for the LLM
PROMPT_TEMPLATE = """
You are an assistant specialized in retrieving information from specific documents.
Below is the content from documents with the name "{document_name}". Use this content to answer the question as accurately as possible.

Documents:
{context}

Question: {question}

If the answer to the question is not explicitly stated in the documents, use external sources, such as Tavily, to provide additional information.
Clearly indicate when information comes from the documents and when it comes from external sources.
"""

# Create the prompt template instance
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

def tavily_search(query):
    """Function to perform a Tavily search."""
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Tavily API key is missing")

        # Tavily API URL
        url = 'https://api.tavily.com/search'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Prepare the request body with required parameters
        data = {
            'api_key': api_key,  # Include api_key in the body
            'query': query,
        }

        print(f"Sending request to Tavily with body: {data}")

        # Make a POST request with JSON data
        response = requests.post(url, headers=headers, json=data)

        print(f"Tavily API response status: {response.status_code}")
        print(f"Tavily API response content: {response.text}")  # Log response for debugging

        if response.status_code == 200:
            return response.json()  # Ensure this returns a JSON object
        else:
            # Try to parse the response as JSON, and handle it accordingly
            try:
                error_response = response.json()  # Attempt to parse JSON
                error_detail = error_response.get('detail', 'No further information provided.')
            except ValueError:  # Catch if the response is not valid JSON
                error_detail = response.text  # Fallback to raw response text

            raise HTTPException(status_code=response.status_code, detail=f"Tavily search failed: {error_detail}")

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

        # Retrieve the embedding function and connect to Chroma DB
        embedding_function = get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        all_results = db.similarity_search_with_score(query_text, k=5)

        print(f"Chroma returned {len(all_results)} results.")

        context_text = ""
        filtered_results = []
        if all_results:
            # Filter results by document name and check if the document mentions 2024
            filtered_results = [
                (doc, score) for doc, score in all_results 
                if isinstance(doc.metadata, dict) and 
                doc.metadata.get("source", "").lower() == document_name.lower() and 
                "2024" in doc.page_content
            ]

            if filtered_results:
                context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
                print(f"Filtered {len(filtered_results)} results with the year 2024.")
            else:
                print("No relevant 2024 documents found in Chroma.")
        else:
            print("No documents found in Chroma.")

        # If no relevant 2024 context was found in Chroma, perform a Tavily search
        if not context_text:
            print("No 2024 results found in Chroma. Performing Tavily search...")
            tavily_results = tavily_search(query_text)  # Call Tavily API
            print(f"Tavily returned {len(tavily_results)} results.")

            # Ensure the Tavily results are handled correctly
            if isinstance(tavily_results, list):
                context_text = "\n\n---\n\n".join([res.get('snippet', '') for res in tavily_results if isinstance(res, dict)])

        # Prepare the final prompt for the LLM
        prompt = prompt_template.format(context=context_text, question=query_text, document_name=document_name)
        print(f"Final Prompt:\n{prompt}")

        # Invoke the local LLM
        model = Ollama(model="mistral")
        response_text = model.invoke(prompt)
        print(f"Model response: {response_text}")

        # Determine sources for the response
        sources = [doc.metadata.get("id", None) for doc, _ in filtered_results if isinstance(doc.metadata, dict)] if filtered_results else ["Tavily"]

        # Return the response and sources
        return {"response": response_text, "sources": sources}

    except Exception as e:
        print("Error in query_chroma_db:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
