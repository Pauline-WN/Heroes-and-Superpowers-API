import os

class Config:
    # Using os.path.join to construct the path to the database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of this config.py
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'heroes.db')  # Point to heroes.db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
