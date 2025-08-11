import os

def validate_pdf_file(file):
    """Validate uploaded file is a PDF"""
    if not file:
        return False
    
    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        return False
    
    # Check file size (optional)
    # You can add file size validation here
    
    return True

def validate_query(query_text):
    """Validate query text"""
    if not query_text or not isinstance(query_text, str):
        return False
    
    if len(query_text.strip()) < 3:
        return False
    
    if len(query_text) > 5000:  # Max query length
        return False
    
    return True
