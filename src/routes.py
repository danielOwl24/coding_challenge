from flask import Blueprint, request, jsonify
from utils import load_csv_to_db, backup_table, get_all_models, restore_from_avro, load_queries
from models import db, Departments, Jobs, HiredEmployees
import traceback
from sqlalchemy.sql import text

SQL_QUERIES = load_queries()

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

@bp.route("/restore", methods=["POST"])
def restore_table():
    data = request.json
    table_name = data.get("table")

    if not table_name:
        return jsonify({"error": "Missing 'table' parameter in request body."}), 400

    TABLES = {
        "departments": Departments,
        "jobs": Jobs,
        "hired_employees": HiredEmployees,
    }

    model = TABLES.get(table_name.lower())
    if not model:
        return jsonify({"error": f"Unknown table: {table_name}"}), 400

    filename = f"data/backup/{table_name}.avro"
    response, status_code = restore_from_avro(model, filename)
    return jsonify(response), status_code

@bp.route("/req_1", methods=["GET"])
def req_1():
    query = text(SQL_QUERIES["req_1"])
    result = db.session.execute(query)
    data = [dict(row) for row in result.mappings()]
    #print(data)
    return jsonify(data), 200
