from extensions import db
from datetime import datetime

class Professeur(db.Model):
    __tablename__ = 'Professeur'
    id_prof = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    date_naissance = db.Column(db.Date)
    Telephone = db.Column(db.String(100))
    address = db.Column(db.Text)
    Photo = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    Departement = db.Column(db.String(255))
    Specialite = db.Column('Specialité', db.String(255))
    siteWeb = db.Column(db.String(255))
    annee_universitaire = db.Column(db.String(100))
    Date_embauche = db.Column(db.Date)
    LinkedIn = db.Column(db.String(255))
    Biographie = db.Column(db.String(255))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id_prof': self.id_prof,
            'nom': self.nom,
            'prenom': self.prenom,
            'Email': self.Email,
            'date_naissance': self.date_naissance,
            'Telephone': self.Telephone,
            'address': self.address,
            'Photo': self.Photo,
            'genre': self.genre,
            'Departement': self.Departement,
            'Specialite': self.Specialite,
            'siteWeb': self.siteWeb,
            'annee_universitaire': self.annee_universitaire,
            'Date_embauche': self.Date_embauche,
            'LinkedIn': self.LinkedIn,
            'Biographie': self.Biographie,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 