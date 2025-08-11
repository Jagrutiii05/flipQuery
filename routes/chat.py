from flask import Blueprint, request, jsonify, current_app
from rag_utils.vectorize import Vectorizer
from rag_utils.pinecone_initializer import PineconeService
from rag_utils.ai_agent import generate_answer
from utils.validator import validate_query

def query_rag():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Query text is required"}), 400
        
        query_text = data['query']
        doc_id = data.get('doc_id')
        
        if not validate_query(query_text):
            return jsonify({"error": "Invalid query"}), 400
        
        # Create query embedding
        vectorizer = Vectorizer()
        query_embedding = vectorizer.create_query_embedding(query_text)
        
        # Search similar vectors
        pinecone_service = PineconeService()
        similar_chunks = pinecone_service.similarity_search(
            query_embedding, 
            top_k=5,
            filter_doc_id=doc_id
        )
        
        if not similar_chunks:
            return jsonify({
                "answer": "I couldn't find relevant information to answer your question.",
                "query": query_text
            }), 200
        
        # Generate response using LLM
        answer = generate_answer(query_text, similar_chunks)
        
        return jsonify({
            "answer": answer,
            "query": query_text,
            "sources": len(similar_chunks)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Query error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500