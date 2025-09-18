from extensions import db
from datetime import datetime

class Bulletin(db.Model):
    __tablename__ = 'Bulletin'
    id_bulletin = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('Etudiant.id_etudiant'))
    note_id = db.Column(db.Integer, db.ForeignKey('Note.id_note'))
    moyenne = db.Column(db.Float)
    Etat = db.Column(db.String(50))
    mention = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def serialize(self):
        return {
            'id_bulletin': self.id_bulletin,
            'etudiant_id': self.etudiant_id,
            'note_id': self.note_id,
            'moyenne': self.moyenne,
            'Etat': self.Etat,
            'mention': self.mention,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 