from flask import Blueprint, request, flash, redirect, url_for, render_template, send_file
from extensions import db
from Model.importation import Importation
from Model.etudiant import Etudiant
from Model.professeur import Professeur
from Model.matiere import Matiere
from Model.note import Note
import pandas as pd
import io
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import json

# Configuration
UPLOAD_FOLDER = 'static/uploads/imports'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

import_bp = Blueprint('import', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@import_bp.route('/', methods=['GET'])
def import_page():
    imports = Importation.query.order_by(Importation.date_import.desc()).all()
    stats = {
        'etudiants': Etudiant.query.count(),
        'professeurs': Professeur.query.count(),
        'matieres': Matiere.query.count(),
        'notes': Note.query.count()
    }
    return render_template('document/importation.html', imports=imports, stats=stats)

@import_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(url_for('import.import_page'))
    
    file = request.files['file']
    import_type = request.form.get('import_type')
    
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'danger')
        return redirect(url_for('import.import_page'))
    
    if not import_type:
        flash('Veuillez sélectionner un type d\'importation', 'danger')
        return redirect(url_for('import.import_page'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Lire le fichier
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            
            # Convertir les dates
            for col in df.columns:
                if 'date' in col.lower():
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
            
            # Traitement selon le type (mode création seulement)
            if import_type == 'etudiants':
                result = process_etudiants(df)
            elif import_type == 'professeurs':
                result = process_professeurs(df)
            elif import_type == 'matieres':
                result = process_matieres(df)
            elif import_type == 'notes':
                result = process_notes(df)
            else:
                flash('Type d\'importation non valide', 'danger')
                return redirect(url_for('import.import_page'))
            
            # Enregistrer l'historique
            import_record = Importation(
                nom_fichier=filename,
                type_import=import_type,
                taille_fichier=os.path.getsize(filepath),
                nombre_lignes=result['total'],
                nombre_traitees=result['success'],
                lignes_erreur=result['errors'],
                status='completed' if result['errors'] == 0 else 'completed_with_errors',
                rapport_erreurs=json.dumps(result['error_details']),
                date_import=datetime.utcnow()
            )
            db.session.add(import_record)
            db.session.commit()
            
            if result['errors'] > 0:
                flash(f"Import terminé avec {result['errors']} erreur(s)", 'warning')
            else:
                flash('Import terminé avec succès', 'success')
            
            return redirect(url_for('import.import_page'))
            
        except Exception as e:
            flash(f'Erreur lors de l\'importation: {str(e)}', 'danger')
            return redirect(url_for('import.import_page'))
    
    flash('Type de fichier non autorisé', 'danger')
    return redirect(url_for('import.import_page'))

@import_bp.route('/template/<import_type>')
def download_template(import_type):
    if import_type == 'etudiants':
        columns = ['nom', 'prenom', 'Email', 'date_naissance', 'telephone', 
                 'class', 'address', 'Photo', 'annee_universitaire', 
                 'genre', 'date_inscription']
    elif import_type == 'professeurs':
        columns = ['nom', 'prenom', 'Email', 'date_naissance', 'Telephone', 
                 'address', 'Photo', 'genre', 'Departement', 'Specialite', 
                 'siteWeb', 'annee_universitaire', 'Date_embauche', 
                 'LinkedIn', 'Biographie', 'status']
    elif import_type == 'matieres':
        columns = ['nom_matiere', 'coefficient', 'volume_horaire', 'semestre', 
                 'classe', 'annee_universitaire', 'id_prof']
    elif import_type == 'notes':
        columns = ['etudiant_id', 'matiere_id', 'note', 'date']
    else:
        flash('Type d\'importation non valide', 'danger')
        return redirect(url_for('import.import_page'))
    
    df = pd.DataFrame(columns=columns)
    
    # Ajouter des exemples de données
    # if import_type == 'etudiants':
    #     df.loc[0] = ['Doe', 'John', 'john.doe@email.com', '2000-01-15', 
    #                 '0612345678', 'L3', '123 Rue Exemple', '', '2023-2024', 
    #                 'M', '2023-09-01']
    # elif import_type == 'professeurs':
    #     df.loc[0] = ['Smith', 'Jane', 'jane.smith@email.com', '1980-05-20',
    #                 '0698765432', '456 Avenue Test', '', 'F', 'Informatique',
    #                 'IA', 'www.janesmith.com', '2023-2024', '2015-09-01',
    #                 'linkedin.com/janesmith', 'Bio...', 'active']
    # elif import_type == 'matieres':
    #     df.loc[0] = ['Mathématiques', 4, 60, 'S1', 'L3', '2023-2024', 1]
    # elif import_type == 'notes':
    #     df.loc[0] = [1, 1, 15.5, '2023-12-15']
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Donnees', index=False)
        worksheet = writer.sheets['Donnees']
        
        # Ajouter des commentaires/instructions
        if import_type == 'notes':
            worksheet.write('G1', 'ID étudiant doit exister dans la base')
            worksheet.write('G2', 'ID matière doit exister dans la base')
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name=f'modele_import_{import_type}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Fonctions de traitement simplifiées (création seulement)
def process_etudiants(df):
    required_columns = ['nom', 'prenom', 'Email', 'class']
    if not all(col in df.columns for col in required_columns):
        return {
            'total': len(df),
            'success': 0,
            'errors': len(df),
            'error_details': ['Colonnes requises manquantes: nom, prenom, Email, class']
        }
    
    results = {'total': len(df), 'success': 0, 'errors': 0, 'error_details': []}
    
    for index, row in df.iterrows():
        try:
            etudiant_data = {
                'nom': str(row['nom']),
                'prenom': str(row['prenom']),
                'Email': str(row['Email']),
                'date_naissance': row.get('date_naissance'),
                'telephone': str(row.get('telephone', '')),
                'class_': str(row['class']),
                'address': str(row.get('address', '')),
                'Photo': str(row.get('Photo', '')),
                'annee_universitaire': str(row.get('annee_universitaire', '')),
                'genre': str(row.get('genre', '')),
                'date_inscription': row.get('date_inscription')
            }
            
            # Vérifier si l'étudiant existe déjà
            if Etudiant.query.filter_by(Email=etudiant_data['Email']).first():
                raise Exception("Un étudiant avec cet email existe déjà")
            
            new_etudiant = Etudiant(**etudiant_data)
            db.session.add(new_etudiant)
            db.session.commit()
            results['success'] += 1
            
        except Exception as e:
            db.session.rollback()
            results['errors'] += 1
            results['error_details'].append(f"Ligne {index+1}: {str(e)}")
    
    return results

def process_professeurs(df):
    required_columns = ['nom', 'prenom', 'Email']
    if not all(col in df.columns for col in required_columns):
        return {
            'total': len(df),
            'success': 0,
            'errors': len(df),
            'error_details': ['Colonnes requises manquantes: nom, prenom, Email']
        }
    
    results = {'total': len(df), 'success': 0, 'errors': 0, 'error_details': []}
    
    for index, row in df.iterrows():
        try:
            prof_data = {
                'nom': str(row['nom']),
                'prenom': str(row['prenom']),
                'Email': str(row['Email']),
                'date_naissance': row.get('date_naissance'),
                'Telephone': str(row.get('Telephone', '')),
                'address': str(row.get('address', '')),
                'Photo': str(row.get('Photo', '')),
                'genre': str(row.get('genre', '')),
                'Departement': str(row.get('Departement', '')),
                'Specialite': str(row.get('Specialite', '')),
                'siteWeb': str(row.get('siteWeb', '')),
                'annee_universitaire': str(row.get('annee_universitaire', '')),
                'Date_embauche': row.get('Date_embauche'),
                'LinkedIn': str(row.get('LinkedIn', '')),
                'Biographie': str(row.get('Biographie', '')),
                'status': str(row.get('status', 'active'))
            }
            
            if Professeur.query.filter_by(Email=prof_data['Email']).first():
                raise Exception("Un professeur avec cet email existe déjà")
            
            new_prof = Professeur(**prof_data)
            db.session.add(new_prof)
            db.session.commit()
            results['success'] += 1
            
        except Exception as e:
            db.session.rollback()
            results['errors'] += 1
            results['error_details'].append(f"Ligne {index+1}: {str(e)}")
    
    return results

def process_matieres(df):
    required_columns = ['nom_matiere', 'coefficient', 'semestre', 'classe']
    if not all(col in df.columns for col in required_columns):
        return {
            'total': len(df),
            'success': 0,
            'errors': len(df),
            'error_details': ['Colonnes requises manquantes: nom_matiere, coefficient, semestre, classe']
        }
    
    results = {'total': len(df), 'success': 0, 'errors': 0, 'error_details': []}
    
    for index, row in df.iterrows():
        try:
            matiere_data = {
                'nom_matiere': str(row['nom_matiere']),
                'coefficient': float(row['coefficient']),
                'volume_horaire': int(row.get('volume_horaire', 0)),
                'semestre': str(row['semestre']),
                'classe': str(row['classe']),
                'annee_universitaire': str(row.get('annee_universitaire', '')),
                'id_prof': int(row.get('id_prof', 0)) if pd.notna(row.get('id_prof')) else None
            }
            
            # Vérifier si le professeur existe si id_prof est fourni
            if matiere_data['id_prof'] and not Professeur.query.get(matiere_data['id_prof']):
                raise Exception(f"Professeur ID {matiere_data['id_prof']} introuvable")
            
            # Vérifier si la matière existe déjà
            if Matiere.query.filter_by(
                nom_matiere=matiere_data['nom_matiere'],
                semestre=matiere_data['semestre'],
                classe=matiere_data['classe']
            ).first():
                raise Exception("Cette matière existe déjà pour ce semestre et cette classe")
            
            new_matiere = Matiere(**matiere_data)
            db.session.add(new_matiere)
            db.session.commit()
            results['success'] += 1
            
        except Exception as e:
            db.session.rollback()
            results['errors'] += 1
            results['error_details'].append(f"Ligne {index+1}: {str(e)}")
    
    return results

def process_notes(df):
    required_columns = ['etudiant_id', 'matiere_id', 'note']
    if not all(col in df.columns for col in required_columns):
        return {
            'total': len(df),
            'success': 0,
            'errors': len(df),
            'error_details': ['Colonnes requises manquantes: etudiant_id, matiere_id, note']
        }
    
    results = {'total': len(df), 'success': 0, 'errors': 0, 'error_details': []}
    
    for index, row in df.iterrows():
        try:
            # Vérifier que l'étudiant et la matière existent
            etudiant = Etudiant.query.get(int(row['etudiant_id']))
            matiere = Matiere.query.get(int(row['matiere_id']))
            
            if not etudiant:
                raise Exception(f"Étudiant ID {row['etudiant_id']} introuvable")
            if not matiere:
                raise Exception(f"Matière ID {row['matiere_id']} introuvable")
            
            note_data = {
                'etudiant_id': int(row['etudiant_id']),
                'matiere_id': int(row['matiere_id']),
                'note': float(row['note']),
                'date': row.get('date')
            }
            
            # Vérifier si la note existe déjà
            if Note.query.filter_by(
                etudiant_id=note_data['etudiant_id'],
                matiere_id=note_data['matiere_id']
            ).first():
                raise Exception("Une note existe déjà pour cet étudiant et cette matière")
            
            new_note = Note(**note_data)
            db.session.add(new_note)
            db.session.commit()
            results['success'] += 1
            
        except Exception as e:
            db.session.rollback()
            results['errors'] += 1
            results['error_details'].append(f"Ligne {index+1}: {str(e)}")
    
    return results