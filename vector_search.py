# # # import os
# # # import pinecone
# # # from openai import OpenAI
# # # from dotenv import load_dotenv

# # # load_dotenv()
# # # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # # # Initialize Pinecone
# # # pinecone.init(
# # #     api_key=os.getenv("PINECONE_API_KEY"),
# # #     environment=os.getenv("PINECONE_ENVIRONMENT")
# # # )

# # # # Use a consistent embedding model
# # # EMBEDDING_MODEL = "text-embedding-3-small"
# # # INDEX_NAME = "hackrx-retrieval" # Choose an index name

# # # def create_and_embed_index(chunks: list[str]):
# # #     """Creates a Pinecone index and populates it with document chunks."""
# # #     if INDEX_NAME in pinecone.list_indexes():
# # #         print(f"Index '{INDEX_NAME}' already exists. Deleting it.")
# # #         pinecone.delete_index(INDEX_NAME)

# # #     print(f"Creating new index '{INDEX_NAME}'...")
# # #     pinecone.create_index(
# # #         name=INDEX_NAME,
# # #         dimension=1536, # Dimension for text-embedding-3-small
# # #         metric='cosine'
# # #     )
# # #     index = pinecone.Index(INDEX_NAME)

# # #     # Embed and upsert chunks in batches
# # #     batch_size = 100
# # #     for i in range(0, len(chunks), batch_size):
# # #         batch_chunks = chunks[i:i + batch_size]
# # #         response = client.embeddings.create(input=batch_chunks, model=EMBEDDING_MODEL)
# # #         embeddings = [item.embedding for item in response.data]
        
# # #         vectors_to_upsert = []
# # #         for j, chunk in enumerate(batch_chunks):
# # #             # Create a unique ID for each chunk
# # #             vector_id = f"chunk-{i+j}"
# # #             vectors_to_upsert.append((vector_id, embeddings[j], {"text": chunk}))

# # #         index.upsert(vectors=vectors_to_upsert)
# # #     print("Finished embedding and uploading all chunks to Pinecone.")
# # #     return index

# # # def get_relevant_chunks(query: str, index) -> str:
# # #     """Embeds a query and retrieves the top 3 most relevant text chunks."""
# # #     response = client.embeddings.create(input=[query], model=EMBEDDING_MODEL)
# # #     query_embedding = response.data[0].embedding

# # #     results = index.query(
# # #         vector=query_embedding,
# # #         top_k=3, # Retrieve top 3 relevant chunks
# # #         include_metadata=True
# # #     )

# # #     context = "\n---\n".join([match['metadata']['text'] for match in results['matches']])
# # #     return context
# # # file: vector_search.py
# # import os
# # from openai import OpenAI
# # from dotenv import load_dotenv
# # # IMPORTANT: Import ServerlessSpec
# # from pinecone import Pinecone, ServerlessSpec

# # # Load environment variables from .env file
# # load_dotenv()

# # # --- Initialize Clients ---
# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# # pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # # --- Define Constants ---
# # EMBEDDING_MODEL = "text-embedding-3-small"
# # INDEX_NAME = "hackrx-retrieval"

# # def create_and_embed_index(chunks: list[str]):
# #     """Creates a Pinecone index and populates it with document chunks."""

# #     # Delete index if it already exists
# #     if INDEX_NAME in [index.name for index in pc.list_indexes()]:
# #         print(f"Index '{INDEX_NAME}' already exists. Deleting it for a fresh start.")
# #         pc.delete_index(INDEX_NAME)

# #     # Create new index using ServerlessSpec (THIS IS THE FIX)
# #     print(f"Creating new serverless index '{INDEX_NAME}'...")
# #     pc.create_index(
# #         name=INDEX_NAME,
# #         dimension=1536,
# #         metric='cosine',
# #         # Use ServerlessSpec with the cloud and region you selected earlier
# #         spec=ServerlessSpec(
# #             cloud='aws',
# #             region='us-east-1'
# #         )
# #     )
# #     # Get the index object from the Pinecone instance
# #     index = pc.Index(INDEX_NAME)

# #     # Embed and upsert chunks in batches
# #     batch_size = 100
# #     for i in range(0, len(chunks), batch_size):
# #         batch_chunks = chunks[i:i + batch_size]
# #         response = client.embeddings.create(input=batch_chunks, model=EMBEDDING_MODEL)
# #         embeddings = [item.embedding for item in response.data]
        
# #         vectors_to_upsert = []
# #         for j, chunk in enumerate(batch_chunks):
# #             vector_id = f"chunk-{i+j}"
# #             vectors_to_upsert.append((vector_id, embeddings[j], {"text": chunk}))

# #         index.upsert(vectors=vectors_to_upsert)
# #     print(f"Finished embedding and uploading all {len(chunks)} chunks to Pinecone.")
# #     return index

# # def get_relevant_chunks(query: str, index) -> str:
# #     """Embeds a query and retrieves the top 3 most relevant text chunks."""
# #     response = client.embeddings.create(input=[query], model=EMBEDDING_MODEL)
# #     query_embedding = response.data[0].embedding

# #     results = index.query(
# #         vector=query_embedding,
# #         top_k=3,
# #         include_metadata=True
# #     )

# #     context = "\n---\n".join([match['metadata']['text'] for match in results['matches']])
# #     return context

# # file: vector_search.py
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# from pinecone import Pinecone, ServerlessSpec

# load_dotenv()

# # --- Initialize Clients ---
# # Configure Gemini API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# # Initialize Pinecone
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # --- Define Constants ---
# # Use Google's new embedding model
# EMBEDDING_MODEL = "models/embedding-001"
# INDEX_NAME = "hackrx-retrieval"

# def create_and_embed_index(chunks: list[str]):
#     """Creates a Pinecone index and populates it with document chunks."""

#     if INDEX_NAME in [index.name for index in pc.list_indexes()]:
#         print(f"Index '{INDEX_NAME}' already exists. Deleting it.")
#         pc.delete_index(INDEX_NAME)

#     # Create new index with the correct dimension for Google's model (768)
#     print(f"Creating new serverless index '{INDEX_NAME}'...")
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536, # <-- IMPORTANT: Dimension changed from 1536 to 768
#         metric='cosine',
#         spec=ServerlessSpec(
#             cloud='aws',
#             region='us-east-1'
#         )
#     )
#     index = pc.Index(INDEX_NAME)

#     # Embed and upsert chunks in batches
#     batch_size = 50 # Google's API has a lower batch limit
#     for i in range(0, len(chunks), batch_size):
#         batch_chunks = chunks[i:i + batch_size]
#         # Create embeddings using the Google Gemini API
#         result = genai.embed_content(
#             model=EMBEDDING_MODEL,
#             content=batch_chunks,
#             task_type="retrieval_document"
#         )
#         embeddings = result['embedding']
        
#         vectors_to_upsert = []
#         for j, chunk in enumerate(batch_chunks):
#             vector_id = f"chunk-{i+j}"
#             vectors_to_upsert.append((vector_id, embeddings[j], {"text": chunk}))

#         index.upsert(vectors=vectors_to_upsert)
#     print(f"Finished embedding and uploading all {len(chunks)} chunks to Pinecone.")
#     return index

# def get_relevant_chunks(query: str, index) -> str:
#     """Embeds a query and retrieves the top 3 most relevant text chunks."""
#     # Create query embedding
#     result = genai.embed_content(
#         model=EMBEDDING_MODEL,
#         content=query,
#         task_type="retrieval_query"
#     )
#     query_embedding = result['embedding']

#     results = index.query(
#         vector=query_embedding,
#         top_k=3,
#         include_metadata=True
#     )

#     context = "\n---\n".join([match['metadata']['text'] for match in results['matches']])
#     return context

# file: vector_search.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

# --- Initialize Clients ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# --- Define Constants and Index ---
EMBEDDING_MODEL = "models/embedding-001"
INDEX_NAME = "hackrx-retrieval"

# Get the index object from Pinecone
index = pc.Index(INDEX_NAME)

def create_and_embed_index(chunks: list[str]):
    """Populates the Pinecone index with document chunks."""
    
    # --- THIS IS THE FIX ---
    # First, check index stats. Only try to delete if it's not empty.
    index_stats = index.describe_index_stats()
    if index_stats.total_vector_count > 0:
        print(f"Clearing the '{INDEX_NAME}' index in Pinecone...")
        index.delete(delete_all=True)
    else:
        print(f"Index is already empty. Skipping delete step.")
    # --- END OF FIX ---

    print(f"Embedding and adding {len(chunks)} chunks to Pinecone...")
    batch_size = 50 
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=batch_chunks,
            task_type="retrieval_document"
        )
        embeddings = result['embedding']
        
        vectors_to_upsert = []
        for j, chunk in enumerate(batch_chunks):
            vector_id = f"chunk-{i+j}"
            vectors_to_upsert.append({
                "id": vector_id,
                "values": embeddings[j],
                "metadata": {"text": chunk}
            })

        index.upsert(vectors=vectors_to_upsert)
        
    print(f"Finished adding all chunks to Pinecone.")
    return

def get_relevant_chunks(query: str) -> str:
    """Embeds a query and retrieves relevant text chunks from Pinecone."""
    
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=query,
        task_type="retrieval_query"
    )
    query_embedding = result['embedding']
    
    results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True
    )

    context = "\n---\n".join([match['metadata']['text'] for match in results['matches']])
    return context