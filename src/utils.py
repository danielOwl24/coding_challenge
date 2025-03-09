import pandas as pd
from sqlalchemy.exc import IntegrityError
from models import db, HiredEmployees, Jobs, Departments 
from logging_config import logger
from sqlalchemy.dialects.postgresql import insert

def load_csv_to_db(file_path, file_name):
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
        else:
            logger.error("The file name is not mapped in our files dictionary.")
            return {"error": "File not mapped."}, 500
        
        stmt = insert(model_class).values(df.to_dict(orient="records"))
        stmt = stmt.on_conflict_do_update(
            index_elements = model_class.get_primary_key(),
            set_ = {c.name: c for c in stmt.excluded if c.name != model_class.get_primary_key()[0]}  # Evitar cambiar el ID
        )
        db.session.execute(stmt)
        db.session.commit()
        return {"message": "Data loaded successfully."}, 200
    except pd.errors.EmptyDataError:
        return {"error": "The csv file is empty."}, 400
    except pd.errors.ParserError:
        return {"error:" "Error parsing the csv file."}, 400
    except IntegrityError:
        db.session.rollback()
        return {"error": "Database error."}, 500
    except Exception as e:
        return {"error": str(e)}, 500