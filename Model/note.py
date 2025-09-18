from extensions import db
from datetime import datetime

class Note(db.Model):
    __tablename__ = 'Note'
    
    id_note = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('Etudiant.id_etudiant'))
    matiere_id = db.Column(db.Integer, db.ForeignKey('Matiere.id_matiere'))
    note = db.Column(db.Float)
    coefficient = db.Column(db.Float, default=1.0)
    semester = db.Column(db.String(50))
    academic_year = db.Column(db.String(50))
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    matiere = db.relationship('Matiere', backref='notes')
    etudiant = db.relationship('Etudiant', backref='notes')
    
    def serialize(self):
        return {
            'id_note': self.id_note,
            'etudiant_id': self.etudiant_id,
            'matiere_id': self.matiere_id,
            'note': self.note,
            'coefficient': self.coefficient,
            'semester': self.semester,
            'academic_year': self.academic_year,
            'date': self.date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }