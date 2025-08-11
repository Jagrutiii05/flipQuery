import os

import openai
from utils.logger import log
from google import genai

# client = genai.Client()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_answer(query, context_chunks):
    """Generate answer using Gemini"""
    try:
        # Prepare context from retrieved chunks with better formatting
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            text = chunk.get('metadata', {}).get('text', '').strip()
            if text:
                context_parts.append(f"Context {i}:\n{text}")
        
        context = "\n\n".join(context_parts)
            
        # Create prompt with better formatting
        system_prompt = f"""Based on the following context, please answer the question. If the answer cannot be found in the context, please say so.

Context:
{context}

Question: {query}

Instructions:
- Provide a clear, well-formatted answer
- Use bullet points or numbered lists when appropriate
- If citing specific information, mention which context section it comes from
- Keep the response concise but comprehensive
- Format the response in a readable way with proper spacing and structure"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[f"{system_prompt}\n\nQuestion: {query}"]
        )
            
        answer = response.text.strip()

        # Clean up any formatting issues
        if answer:
            # Ensure proper spacing
            answer = answer.replace('\n\n\n', '\n\n')  # Remove excessive line breaks
            answer = answer.replace('  ', ' ')  # Remove double spaces
            
        log("Generated answer successfully")
        return answer
            
    except Exception as e:
        log(f"Error generating answer: {str(e)}")
        return "I'm sorry, I encountered an error while generating the answer."