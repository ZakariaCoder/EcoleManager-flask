from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from Model.etudiant import Etudiant
import os

etudiant_bp = Blueprint('etudiant', __name__)


@etudiant_bp.route('/afficher_etud/<int:id>')
def afficher_etud(id):
    etudiant = Etudiant.query.get_or_404(id)
    return render_template('etudiants/afficher_etud.html', etudiant=etudiant) 

# Afficher le formulaire d'ajout
@etudiant_bp.route('/ajouter_etud', methods=['GET', 'POST'])
def ajouter_etud():
    if request.method == 'POST':
        try:
            # Gestion du fichier photo
            photo_filename = None
            if 'Photo' in request.files:
                photo = request.files['Photo']
                if photo.filename != '':
                    # Sécurisez le nom du fichier et enregistrez-le
                    from werkzeug.utils import secure_filename
                   
                    photo_filename = secure_filename(photo.filename)
                    photo.save(os.path.join('static/uploads', photo_filename))

            # Création de l'étudiant avec les données du formulaire
            etudiant = Etudiant(
                nom=request.form.get('nom'),
                prenom=request.form.get('prenom'),
                Email=request.form.get('Email'),  # Notez le changement de 'Email' à 'email'
                date_naissance=request.form.get('date_naissance'),
                telephone=request.form.get('telephone'),
                class_=request.form.get('class'),
                address=request.form.get('address'),
                Photo=photo_filename,
                annee_universitaire=request.form.get('annee_universitaire'),
                genre=request.form.get('genre'),
                date_inscription=request.form.get('date_inscription')
            )
            
            db.session.add(etudiant)
            db.session.commit()
            flash('Étudiant ajouté avec succès!', 'success')
            return redirect(url_for('etudiant.etudiant'))  # Assurez-vous que cette route existe
        
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout: {str(e)}", 'danger')
    
    return render_template('etudiants/ajouter_etud.html')

# Afficher le formulaire de modification
@etudiant_bp.route('/modifier_etud/<int:id>', methods=['GET', 'POST'])
def modifier_etud(id):
    etudiant = Etudiant.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Gestion du fichier photo
            if 'Photo' in request.files:
                photo = request.files['Photo']
                if photo.filename != '':
                    # Supprimer l'ancienne photo si elle existe
                    if etudiant.Photo:
                        try:
                            os.remove(os.path.join('static/uploads', etudiant.Photo))
                        except:
                            pass
                    
                    # Sauvegarder la nouvelle photo
                    from werkzeug.utils import secure_filename
                    photo_filename = secure_filename(photo.filename)
                    photo.save(os.path.join('static/uploads', photo_filename))
                    etudiant.Photo = photo_filename

            # Mise à jour des champs de l'étudiant
            etudiant.nom = request.form.get('nom')
            etudiant.prenom = request.form.get('prenom')
            etudiant.Email = request.form.get('Email')
            etudiant.date_naissance = request.form.get('date_naissance')
            etudiant.telephone = request.form.get('telephone')
            etudiant.class_ = request.form.get('class')
            etudiant.address = request.form.get('address')
            etudiant.annee_universitaire = request.form.get('annee_universitaire')
            etudiant.genre = request.form.get('genre')
            etudiant.date_inscription = request.form.get('date_inscription')
            
            db.session.commit()
            flash('Étudiant modifié avec succès!', 'success')
            return redirect(url_for('etudiant.etudiant'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la modification: {str(e)}", 'danger')
    
    return render_template('etudiants/modifier_etud.html', etudiant=etudiant)

# Supprimer un étudiant
@etudiant_bp.route('/supprimer_etud/<int:id>', methods=['POST'])
def supprimer_etud(id):
    etudiant = Etudiant.query.get_or_404(id)
    db.session.delete(etudiant)
    db.session.commit()
    flash('Étudiant supprimé avec succès!', 'success')
    return redirect(url_for('etudiant.etudiant'))


@etudiant_bp.route('/etudiant')

def etudiant():
    etudiants = Etudiant.query.all()
    return render_template('etudiants/etudiant.html', etudiants=etudiants)