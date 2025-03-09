import pandas as pd
from sqlalchemy.exc import IntegrityError
from models import db, HiredEmployees, Jobs, Departments 


def load_csv_to_db(file_path, file_name):
    model_mapping = {
        "departments": Departments,
        "jobs": Jobs,
        "hired_employees": HiredEmployees
    }

    df = pd.read_csv(file_path)

    if file_name in model_mapping:
        model_class = model_mapping[file_name]
        fields = model_class.get_columns()
        table_items = [model_class(**{field: row[field] for field in fields}) for _, row in df.iterrows()]
        print(table_items)
    
    try:
        db.session.bulk_save_objects(table_items)
        db.session.commit()
        return {"message": "Data loaded successfully"}, 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Database error"}, 500