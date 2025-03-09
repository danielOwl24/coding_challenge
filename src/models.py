from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def get_columns(cls):
        return [column.name for column in cls.__table__.columns]

class Departments(BaseModel):
    __table_name__ = 'departments'
    id = db.Column(db.Integer, primary_key = True)
    department = db.Column(db.String(255), nullable=False)

class Jobs(BaseModel):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job = db.Column(db.String(255), nullable=False)

class HiredEmployees(BaseModel):
    __tablename__ = 'hired_employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)





