from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Departments(db.Model):
    __table_name__ = 'departments'
    id = db.Column(db.Integer, primary_key = True)
    department = db.Column(db.String(255), nullable=False)

class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job = db.Column(db.String(255), nullable=False)

class HiredEmployees(db.Model):
    __tablename__ = 'hired_employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)





