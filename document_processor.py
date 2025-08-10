import requests
import pypdf
import io
import re

# A safe character limit to stay well under Pinecone's 40kb metadata limit
MAX_CHUNK_SIZE = 8000 

def _recursive_split(text: str, chunks: list):
    """Helper function to recursively split text."""
    if len(text) <= MAX_CHUNK_SIZE:
        chunks.append(text)
        return
    
    # Find the last sentence break before the max size limit
    split_pos = text.rfind(". ", 0, MAX_CHUNK_SIZE)
    # If no sentence break is found, split at the max size
    if split_pos == -1:
        split_pos = MAX_CHUNK_SIZE
            
    chunks.append(text[:split_pos])
    _recursive_split(text[split_pos:], chunks)

def process_pdf_from_url(url: str) -> list[str]:
    """Downloads a PDF, extracts text, and splits it into appropriately sized chunks."""
    print(f"Fetching PDF from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading PDF: {e}")
        return []

    pdf_file = io.BytesIO(response.content)
    reader = pypdf.PdfReader(pdf_file)

    full_text = ""
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text() + "\n"

    # Initial split by paragraphs
    initial_chunks = re.split(r'\n\s*\n', full_text)
    
    final_chunks = []
    for chunk in initial_chunks:
        stripped_chunk = chunk.strip()
        if len(stripped_chunk) > 100: # Filter out very small chunks
            # If a chunk is too large, split it further
            if len(stripped_chunk) > MAX_CHUNK_SIZE:
                _recursive_split(stripped_chunk, final_chunks)
            else:
                final_chunks.append(stripped_chunk)

    print(f"Extracted and chunked document into {len(final_chunks)} parts.")
    return final_chunks