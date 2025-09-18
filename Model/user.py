from flask_login import UserMixin  # Ajoutez cette importation
from extensions import db

class User(db.Model, UserMixin):  # Héritez de UserMixin
    __tablename__ = 'User'
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def get_id(self):
        return str(self.id_user)
    def serialize(self):
        return {
            'id_user': self.id_user,
            'username': self.username,
            'email': self.email,
           
        } 