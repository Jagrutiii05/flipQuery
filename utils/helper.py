import hashlib
import time

def generate_doc_id(filename):
    """Generate unique document ID"""
    timestamp = str(int(time.time()))
    hash_input = f"{filename}_{timestamp}"
    return hashlib.md5(hash_input.encode()).hexdigest()

def clean_text(text):
    """Clean extracted text"""
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters if needed
    # You can add more cleaning logic here
    
    return text