# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def get_answer_from_llm(query: str, context: str) -> str:
#     """Generates an answer using GPT-4 based on the query and retrieved context."""
    
#     system_prompt = """
#     You are an expert Q&A system for insurance policies.
#     Your task is to answer the user's question based *only* on the provided text context.
#     - If the context contains the answer, provide a clear and concise answer.
#     - If the context does not contain enough information to answer the question, state that clearly.
#     - Do not use any external knowledge or make assumptions.
#     - Cite the specific information from the context that supports your answer.
#     """

#     user_prompt = f"""
#     CONTEXT:
#     ---
#     {context}
#     ---
#     QUESTION: {query}
    
#     ANSWER:
#     """

#     response = client.chat.completions.create(
#         model="gpt-4", # Or "gpt-3.5-turbo" for better latency/cost
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ],
#         temperature=0.0, # Low temperature for factual answers
#         max_tokens=300
#     )
#     return response.choices[0].message.content.strip()

# file: llm_handler.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_answer_from_llm(query: str, context: str) -> str:
    """Generates an answer using Gemini based on the query and retrieved context."""

    system_prompt = """
    You are an expert Q&A system for insurance policies.
    Your task is to answer the user's question based ONLY on the provided text context.
    - If the context contains the answer, provide a clear and concise answer.
    - If the context does not contain enough information, state that clearly.
    - Do not use any external knowledge or make assumptions.
    """

    # Create the model and generate the response
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(system_prompt + "\n\n" + f"CONTEXT: {context}\n\nQUESTION: {query}")

    return response.text.strip()