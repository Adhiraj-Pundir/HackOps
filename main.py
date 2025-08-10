# import os
# from fastapi import FastAPI, HTTPException, Security
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from pydantic import BaseModel
# from typing import List

# # Import our helper functions
# from document_processor import process_pdf_from_url
# from vector_search import create_and_embed_index, get_relevant_chunks
# from llm_handler import get_answer_from_llm

# # --- API Setup ---
# app = FastAPI(title="Intelligent Query-Retrieval System")
# auth_scheme = HTTPBearer()

# # This is the bearer token from the problem description
# EXPECTED_BEARER_TOKEN = "9c4b4396f4a0f27d1e39a9302f4f93bff8336a872ce7213e4784de343aae8179"

# # --- Pydantic Models for Request/Response ---
# class QueryRequest(BaseModel):
#     documents: str
#     questions: List[str]

# class QueryResponse(BaseModel):
#     answers: List[str]

# # --- Authentication ---
# def validate_token(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)):
#     if credentials.scheme != "Bearer" or credentials.credentials != EXPECTED_BEARER_TOKEN:
#         raise HTTPException(status_code=403, detail="Invalid or missing bearer token")
#     return credentials

# # --- API Endpoint ---
# @app.post("/hackrx/run", response_model=QueryResponse)
# async def run_submission(request: QueryRequest, _=Security(validate_token)):
#     try:
#         # 1. Process Document
#         chunks = process_pdf_from_url(request.documents)
#         if not chunks:
#             raise HTTPException(status_code=400, detail="Could not extract text from document.")
        
#         # 2. Create Embeddings & Pinecone Index
#         # For a hackathon, we create a new index for each request.
#         # In a real app, you'd check if embeddings for this doc already exist.
#         index = create_and_embed_index(chunks)
        
#         # 3. Process each question
#         final_answers = []
#         for question in request.questions:
#             print(f"\nProcessing question: '{question}'")
            
#             # 4. Retrieve relevant chunks (clauses)
#             context = get_relevant_chunks(question, index)
            
#             # 5. Get final answer from LLM
#             answer = get_answer_from_llm(question, context)
#             final_answers.append(answer)
#             print(f"Generated answer: '{answer}'")
            
#         return QueryResponse(answers=final_answers)

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/")
# def root():
#     return {"message": "Query-Retrieval System is running."}

# file: main.py

from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import traceback

# Import helper functions from other modules
from document_processor import process_pdf_from_url
from vector_search import create_and_embed_index, get_relevant_chunks
from llm_handler import get_answer_from_llm

# --- API Setup ---
app = FastAPI(
    title="Intelligent Query-Retrieval System",
    description="A system to answer questions about documents using LLMs and Vector Search."
)
auth_scheme = HTTPBearer()

# The bearer token required for authorization
EXPECTED_BEARER_TOKEN = "9c4b4396f4a0f27d1e39a9302f4f93bff8336a872ce7213e4784de343aae8179"

# --- Pydantic Models for API Data Structure ---
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# --- Authentication Middleware ---
def validate_token(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != EXPECTED_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing bearer token"
        )
    return credentials

# --- API Endpoints ---
@app.post("/hackrx/run", response_model=QueryResponse, tags=["Core"])
async def run_submission(request: QueryRequest, _=Security(validate_token)):
    """
    Main endpoint to process a document and answer questions about it.
    """
    try:
        # Step 1: Download and process the document into text chunks
        print(f"Processing document from: {request.documents}")
        chunks = process_pdf_from_url(request.documents)
        if not chunks:
            raise HTTPException(status_code=400, detail="Could not extract text from the document.")

        # Step 2: Create embeddings and populate the vector store
        print("Populating vector store with document chunks...")
        create_and_embed_index(chunks)
        print("Vector store populated successfully.")

        # Step 3: Process each question
        final_answers = []
        for question in request.questions:
            print(f"\nProcessing question: '{question}'")
            
            # Step 4: Retrieve relevant context from the vector store
            context = get_relevant_chunks(question)
            
            # Step 5: Generate a final answer using the LLM and the context
            answer = get_answer_from_llm(question, context)
            final_answers.append(answer)
            print(f"Generated answer: '{answer}'")
            
        return QueryResponse(answers=final_answers)

    except Exception as e:
        # Log the full traceback for easier debugging on the server side
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@app.get("/", tags=["Health Check"])
def root():
    """
    Root endpoint to check if the service is running.
    """
    return {"message": "Intelligent Query-Retrieval System is running."}