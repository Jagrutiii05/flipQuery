from flask import Flask, request, jsonify, render_template

from routes.chat import query_rag
from routes.upload import upload_pdf
import os
from utils.logger import log

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def home():
    log("Serving index.html")
    return render_template("index.html")

@app.route("/api/upload", methods=["POST"])
def upload():
    log("Upload route hit.")
    return upload_pdf()

@app.route("/api/query", methods=["POST"])
def query():
    log("Query route hit.")
    return query_rag()

@app.route("/health")
def health_check():
    log("Health check requested.")
    return {"status": "healthy", "message": "RAG Backend is running"}

if __name__ == "__main__":
    log("Starting Flask server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
