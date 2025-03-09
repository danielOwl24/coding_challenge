from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String, Float, DateTime, Boolean

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def get_columns(cls):
        return [column.name for column in cls.__table__.columns]
    
    @classmethod
    def get_primary_key(cls):
        mapper = inspect(cls)
        return [column.name for column in mapper.primary_key]
    
    @classmethod
    def get_foreign_keys(cls):
        return [fk.column.name for fk in cls.__table__.foreign_keys]
    
    @classmethod
    def get_column_types(cls):
        column_types = {}
        for column in cls.__table__.columns:
            if isinstance(column.type, Integer):
                column_types[column.name] = "int"
            elif isinstance(column.type, Float):
                column_types[column.name] = "float"
            elif isinstance(column.type, String):
                column_types[column.name] = "string"
            elif isinstance(column.type, DateTime):
                column_types[column.name] = "datetime"
            elif isinstance(column.type, Boolean):
                column_types[column.name] = "bool"
        return column_types
    
class Departments(BaseModel):
    __table_name__ = 'departments'
    id = db.Column(db.Integer, primary_key = True)
    department = db.Column(db.String(255), nullable=False)

class Jobs(BaseModel):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=False)

class HiredEmployees(BaseModel):
    __tablename__ = 'hired_employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)





