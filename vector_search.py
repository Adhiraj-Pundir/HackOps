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