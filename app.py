from flask import Flask, request, jsonify
from my_RAG import function_upload_pdf, function_get_response
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload-pdf", method=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error" : "No file provided"}),400
    
    file = request.files["files"]

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}),400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    chunks = function_upload_pdf(file_path)
    return jsonify(
        {
            "message":"PDF indexed successfully",
            "chunk_added":chunks
        }
    )

def ask():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error":"Query is required"}),400
    
    result = function_get_response(data["query"])
    return jsonify(result);

if __name__ == "__main__":
    app.run(debug=True)

    