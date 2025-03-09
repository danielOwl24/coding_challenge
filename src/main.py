from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import POSTGRES_PORT, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER, DATABASE_NAME
from models import db
from logging_config import logger

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}'
logger.info(f'Connecting to the database {DATABASE_NAME} at port {POSTGRES_PORT}')

db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)