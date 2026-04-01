from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv('.env')
    env = os.environ
    password = env.get('DB_PASSWORD')
    dbname = env.get('DB_NAME')
    host = env.get('HOST')
    user = env.get('USER')

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}/{dbname}"

    db.init_app(app)

    return app