from extensions import db
from datetime import datetime
class Matiere(db.Model):
    __tablename__ = 'Matiere'
    id_matiere = db.Column(db.Integer, primary_key=True)
    nom_matiere = db.Column(db.String(255), nullable=False)
    coefficient = db.Column(db.Float)
    volume_horaire = db.Column(db.Integer)
    semestre = db.Column(db.String(25))
    classe = db.Column(db.String(25))
    annee_universitaire = db.Column(db.String(100))
    id_prof = db.Column(db.Integer, db.ForeignKey('Professeur.id_prof'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def serialize(self):
        return {
            'id_matiere': self.id_matiere,
            'nom_matiere': self.nom_matiere,
            'coefficient': self.coefficient,
            'volume_horaire': self.volume_horaire,
            'semestre': self.semestre,
            'classe': self.classe,
            'annee_universitaire': self.annee_universitaire,
            'id_prof': self.id_prof,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 