from flask import Blueprint, request, jsonify
from utils import load_csv_to_db, backup_table, get_all_models
from models import db
import traceback

bp = Blueprint("api", __name__)

@bp.route("/upload-csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = f"data/{file.filename}"
    file.save(file_path)

    return jsonify(*load_csv_to_db(file_path, file.filename))

@bp.route("/backup", methods=["GET"])
def backup_all():
    try:
        for model in get_all_models():
            backup_table(model)
        return jsonify({"message": "Backup completed successfully"}), 200
    except Exception as e:
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 500