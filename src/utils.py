import pandas as pd
from sqlalchemy.exc import IntegrityError
from models import db, HiredEmployees, Jobs, Departments 
from logging_config import logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text
import numpy as np
from fastavro import writer, parse_schema, reader
import os
import traceback
import flask_sqlalchemy
import yaml

def load_queries(file_path="src/queries.yaml"):
    with open(file_path, "r") as file:
        queries = yaml.safe_load(file)
    return queries

def cast_dataframe(df:pd.DataFrame, model:flask_sqlalchemy.model.DefaultMeta) -> pd.DataFrame:
    column_types = model.get_column_types_to_pandas()
    
    for col, dtype in column_types.items():
        if col in df.columns:
            if dtype == "int":
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
            elif dtype == "float":
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif dtype == "datetime":
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif dtype == "bool":
                df[col] = df[col].astype(bool)
            elif dtype == "string":
                df[col] = df[col].astype(object).where(df[col].notna(), None)
            df[col] = df[col].replace({np.nan: None})
    return df

def load_csv_to_db(file_path:str, file_name:str) -> tuple:
    model_mapping = {
        "departments.csv": Departments,
        "jobs.csv": Jobs,
        "hired_employees.csv": HiredEmployees
    }
    try: 
        if file_name in model_mapping:
            model_class = model_mapping[file_name]
            fields = model_class.get_columns()
            df = pd.read_csv(file_path, header=None, names=fields)
            df = cast_dataframe(df, model_class)
        else:
            logger.error("The file name is not mapped in our files dictionary.")
            return {"error": "File not mapped."}, 400
        
        stmt = insert(model_class).values(df.to_dict(orient="records"))
        stmt = stmt.on_conflict_do_update(
            index_elements = model_class.get_primary_key(),
            set_ = {c.name: c for c in stmt.excluded if c.name != model_class.get_primary_key()[0]}  # Evitar cambiar el ID
        )

        db.session.execute(stmt)
        db.session.commit()
        return {"message": f"The file {file_name} was loaded successfully."}, 200
    except pd.errors.EmptyDataError:
        return {"error": "The csv file is empty."}, 415
    except pd.errors.ParserError:
        return {"error:" "Error parsing the csv file."}, 422
    except IntegrityError:
        db.session.rollback()
        return {"error": "Integrity Database error."}, 409
    except Exception as e:
        return {"error": f"Unexpected error -> {str(e)}"}, 500
    
def get_table_schema(model:flask_sqlalchemy.model.DefaultMeta):
    columns = model.get_columns()
    column_types = model.get_column_types_to_avro()
    schema = {
        "type": "record",
        "name": model.__tablename__,
        "fields": [{"name": col, "type":column_types[col]} for col in columns]
    }
    return parse_schema(schema)

def get_all_models() -> list:
    return [
        model for model in db.Model.registry._class_registry.values()
        if isinstance(model, type) and issubclass(model, db.Model) and not model.__dict__.get('__abstract__', False)
    ]

def backup_table(model:flask_sqlalchemy.model.DefaultMeta) -> None:
    BACKUP_DIR = "data/backup/"

    schema = get_table_schema(model)
    filename = os.path.join(BACKUP_DIR, f"{model.__tablename__}.avro")
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "wb") as out_file:
        writer(out_file, schema, [row.__dict__ for row in model.query.all()])

def restore_from_avro(model:flask_sqlalchemy.model.DefaultMeta, filename:str) -> tuple:
    if not os.path.exists(filename):
        return {"error": f"Backup file not found: {filename}"}, 404

    with open(filename, "rb") as in_file:
        file = reader(in_file)
        records = [record for record in file]

    if not records:
        return {"warning": "No data found in backup file."}, 200

    restored_objects = []
    for record in records:
        restored_objects.append(record)

    df = pd.DataFrame(restored_objects)
    df = cast_dataframe(df, model)

    try:
        db.session.execute(text(f"TRUNCATE TABLE {model.__tablename__} RESTART IDENTITY CASCADE"))
        stmt = insert(model).values(df.to_dict(orient="records"))
        stmt = stmt.on_conflict_do_update(
            index_elements = model.get_primary_key(),
            set_ = {c.name: c for c in stmt.excluded if c.name != model.get_primary_key()[0]}  # Evitar cambiar el ID
        )
        db.session.execute(stmt)
        db.session.commit()
        return {"message": f"Successfully restored {len(restored_objects)} records into {model.__tablename__}."}, 200
    except IntegrityError:
        traceback.print_exc(IntegrityError)
        db.session.rollback()
        return {"error": f"Integrity Database error"}, 409
    except Exception as e:
        traceback.print_exc(e)
        db.session.rollback()
        return {"error": f"Unexpected error -> {str(e)}"}, 500
