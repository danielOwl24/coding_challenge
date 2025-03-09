from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String, Float, DateTime

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
    def get_column_types_to_pandas(cls):
        PG_TO_PANDAS_TYPES = {
            Integer: "int",
            Float: "float",
            String: "string",
            DateTime: "datetime",
        }
        return {column.name: PG_TO_PANDAS_TYPES[type(column.type)] for column in cls.__table__.columns}
    
    @classmethod
    def get_column_types_to_avro(cls):
        PG_TO_AVRO_TYPES = {
            Integer: ["int", "null"],
            String: ["string", "null"],
            Float: ["float", "null"],
            DateTime: [{"type": "long", "logicalType": "timestamp-millis"}, "null"]
        }
        return {column.name: PG_TO_AVRO_TYPES[type(column.type)] for column in cls.__table__.columns}
    
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





