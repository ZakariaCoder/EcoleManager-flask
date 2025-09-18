import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/gestion_etudiant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-secrete'