from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from rag_utils.process_pdf import PDFProcessor
from rag_utils.vectorize import Vectorizer
from utils.validator import validate_pdf_file
from utils.logger import log
from rag_utils.pinecone_initializer import PineconeService

def upload_pdf():
    try:
        log("Handling file upload...")

        if 'file' not in request.files:
            return {"error": "No file provided"}

        file = request.files['file']
        if file.filename == '':
            return { "error": "No file selected" }

        if not validate_pdf_file(file):
            return { "error": "Invalid file. Please upload a PDF file" }

        doc_id = str(uuid.uuid4())
        filename = secure_filename(f"{doc_id}_{file.filename}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        pdf_processor = PDFProcessor()
        text_content = pdf_processor.extract_text(filepath)

        if not text_content.strip():
            os.remove(filepath)
            return {"error": "Could not extract text from PDF"}

        vectorizer = Vectorizer()
        chunks = vectorizer.create_chunks(text_content)
        embeddings = vectorizer.create_embeddings(chunks)

        pinecone_service = PineconeService()
        vectors_to_upsert = [
            (f"{doc_id}_{i}", embeddings[i], {"text": chunks[i], "doc_id": doc_id})
            for i in range(len(chunks))
        ]

        success = pinecone_service.upsert_vectors(vectors_to_upsert)

        os.remove(filepath)

        if success:
            return jsonify({
                "message": "PDF uploaded and processed successfully",
                "doc_id": doc_id,
                "filename": file.filename,
                "chunks_created": len(chunks)
            }), 200
        else:
            return jsonify({ "error": "Failed to store vectors in Pinecone" }), 500

    except Exception as e:
        log(f"Upload error: {str(e)}")
        return jsonify({ "error": "Internal server error" }), 500
