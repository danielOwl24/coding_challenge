from flask import Blueprint, request, jsonify
from utils import load_csv_to_db

bp = Blueprint("api", __name__)

@bp.route("/upload-csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = f"data/{file.filename}"
    file.save(file_path)

    return jsonify(*load_csv_to_db(file_path, file.filename))