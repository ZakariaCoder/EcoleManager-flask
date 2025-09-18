from extensions import db
from datetime import datetime
class Etudiant(db.Model):
    __tablename__ = 'Etudiant'
    id_etudiant = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    date_naissance = db.Column(db.Date)
    telephone = db.Column(db.String(100))
    class_ = db.Column('class', db.String(20))
    address = db.Column(db.Text)
    Photo = db.Column(db.String(255))
    annee_universitaire = db.Column(db.String(100))
    genre = db.Column(db.String(255))
    date_inscription = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def serialize(self):
        return {
            'id_etudiant': self.id_etudiant,
            'nom_complet': self.nom_complet,
            'Email': self.Email,
            'date_naissance': self.date_naissance,
            'telephone': self.telephone,
            'class': self.class_,
            'address': self.address,
            'Photo': self.Photo,
            'annee_universitaire': self.annee_universitaire,
            'genre': self.genre,
            'date_inscription': self.date_inscription,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 