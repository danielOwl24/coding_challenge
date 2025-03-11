from flask import Blueprint, request, jsonify
from utils import load_csv_to_db, backup_table, get_all_models, restore_from_avro, load_queries, execute_query
from models import Departments, Jobs, HiredEmployees
import traceback
from sqlalchemy.sql import text

SQL_QUERIES = load_queries()
bp = Blueprint("api", __name__)

@bp.route("/upload-csv", methods=["POST"])
def upload_csv():
    """
    Handles CSV file uploads and processes them into the database.

    This endpoint receives a CSV file via a POST request, saves it to a local directory, 
    and then inserts the data into the corresponding database table.

    Returns:
        JSON response with a success message if the file is processed correctly, 
        or an error message if no file is uploaded or an issue occurs.
    """
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = f"data/{file.filename}"
    file.save(file_path)
    response, status_code = load_csv_to_db(file_path, file.filename)
    return jsonify(response), status_code


@bp.route("/backup", methods=["GET"])
def backup_all():
    """
    Creates a backup of all database tables in AVRO format.

    This endpoint iterates over all SQLAlchemy models in the application and generates 
    a backup file for each table. If an error occurs during the process, it logs the 
    error and returns a failure response.

    Returns:
        JSON response with a success message if the backup was successful, 
        or an error message if the backup was not completed or an issue occurs.
    """
    try:
        for model in get_all_models():
            backup_table(model)
        return jsonify({"message": "Backup completed successfully"}), 200
    except Exception as e:
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 500

@bp.route("/restore/<string:table_name>", methods=["POST"])
def restore_table(table_name):
    """
    Restores a specified database table from its backup file.

    Args:
        table_name (str): The name of the table to restore, passed as a URL parameter.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    if not table_name:
        return jsonify({"error": "Missing table name in the route."}), 400

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
    """
    Retrieves the number of employees hired for each job and department in 2021, divided by quarter.
    The results are sorted alphabetically by department and job.

    Returns:
        Response: A JSON response containing the aggregated hiring data or error information.
    """
    return execute_query("req_1", SQL_QUERIES)


@bp.route("/req_2", methods=["GET"])
def req_2():
    """
    Retrieves a list of department IDs, names, and the number of employees hired in 2021 
    for departments that hired more employees than the average across all departments.

    The results are sorted in descending order by the number of employees hired.

    Returns:
        Response: A JSON response containing the filtered hiring data or error information. 
    """
    return execute_query("req_2", SQL_QUERIES)