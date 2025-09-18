from extensions import db
from datetime import datetime
class Importation(db.Model):
    __tablename__ = 'Importation'
    id_import = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(255))
    type_import = db.Column(db.String(50))
    taille_fichier = db.Column(db.BigInteger)
    nombre_lignes = db.Column(db.Integer)
    nombre_traitees = db.Column(db.Integer)
    lignes_erreur = db.Column(db.Integer)
    status = db.Column(db.String(20))
    rapport_erreurs = db.Column(db.Text)
    date_import = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def serialize(self):
        return {
            'id_import': self.id_import,
            'nom_fichier': self.nom_fichier,
            'type_import': self.type_import,
            'taille_fichier': self.taille_fichier,
            'nombre_lignes': self.nombre_lignes,
            'nombre_traitees': self.nombre_traitees,
            'lignes_erreur': self.lignes_erreur,
            'status': self.status,
            'rapport_erreurs': self.rapport_erreurs,
            'date_import': self.date_import,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 