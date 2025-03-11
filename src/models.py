from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy import Integer, String, Float, DateTime


db = SQLAlchemy()


class BaseModel(db.Model):
    """
    Abstract base model that provides utility methods for SQLAlchemy models.
    """
    __abstract__ = True


    @classmethod
    def get_columns(cls) -> list:
        """
        Retrieves a list of column names for the model.

        Returns:
            list: A list of column names.
        """
        return [column.name for column in cls.__table__.columns]
    
    
    @classmethod
    def get_primary_key(cls) -> list:
        """
        Retrieves the primary key column(s) for the model.

        Returns:
            list: A list containing the primary key column names.
        """
        mapper = inspect(cls)
        return [column.name for column in mapper.primary_key]
    
    
    @classmethod
    def get_foreign_keys(cls) -> list:
        """
        Retrieves the foreign key columns for the model.

        Returns:
            list: A list of column names that are foreign keys.
        """
        return [fk.column.name for fk in cls.__table__.foreign_keys]
    
    
    @classmethod
    def get_column_types_to_pandas(cls) -> dict:
        """
        Maps the model's column types to equivalent Pandas data types.

        Returns:
            dict: A dictionary where keys are column names and values are Pandas-compatible types.
        """
        PG_TO_PANDAS_TYPES = {
            Integer: "int",
            Float: "float",
            String: "string",
            DateTime: "datetime",
        }
        return {column.name: PG_TO_PANDAS_TYPES[type(column.type)] for column in cls.__table__.columns}
    
    
    @classmethod
    def get_column_types_to_avro(cls) -> dict:
        """
        Maps the model's column types to Avro-compatible data types.

        Returns:
            dict: A dictionary where keys are column names and values are Avro-compatible types.
        """
        PG_TO_AVRO_TYPES = {
            Integer: ["int", "null"],
            String: ["string", "null"],
            Float: ["float", "null"],
            DateTime: [{"type": "long", "logicalType": "timestamp-millis"}, "null"]
        }
        return {column.name: PG_TO_AVRO_TYPES[type(column.type)] for column in cls.__table__.columns}
    
    
class Departments(BaseModel):
    """
    Model representing the 'departments' table.
    """
    __table_name__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255), nullable=False)


class Jobs(BaseModel):
    """
    Model representing the 'jobs' table.
    """
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=False)


class HiredEmployees(BaseModel):
    """
    Model representing the 'hired_employees' table.
    Stores employee details, including their hiring date, department, and job.
    """
    __tablename__ = 'hired_employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)