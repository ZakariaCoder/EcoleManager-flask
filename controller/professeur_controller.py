from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from Model.professeur import Professeur
import os
from werkzeug.utils import secure_filename
from datetime import datetime

professeur_bp = Blueprint('professeur', __name__)

@professeur_bp.route('/professeur')
def professeur():
    professeurs = Professeur.query.all()
    return render_template('professeur/professeur.html', professeurs=professeurs)

@professeur_bp.route('/ajouter_prof', methods=['GET', 'POST'])
def ajouter_prof():
    if request.method == 'POST':
        try:
            # Gestion du fichier photo
            photo_filename = None
            if 'Photo' in request.files:
                photo = request.files['Photo']
                if photo.filename != '':
                    if not os.path.exists('static/uploads'):
                        os.makedirs('static/uploads')
                    photo_filename = secure_filename(photo.filename)
                    photo.save(os.path.join('static/uploads', photo_filename))

            # Convertir les dates
            date_naissance = datetime.strptime(request.form['date_naissance'], '%Y-%m-%d') if request.form['date_naissance'] else None
            date_embauche = datetime.strptime(request.form['Date_embauche'], '%Y-%m-%d') if request.form['Date_embauche'] else None

            # Création du professeur
            professeur = Professeur(
                nom=request.form['nom'],
                prenom=request.form['prenom'],
                Email=request.form['Email'],
                Telephone=request.form['Telephone'],  # Notez la majuscule pour correspondre au modèle
                date_naissance=date_naissance,
                genre=request.form['genre'],
                Departement=request.form['Departement'],
                Specialite=request.form['Specialite'],
                Date_embauche=date_embauche,
                status=request.form['status'],
                address=request.form['address'],
                siteWeb=request.form.get('siteWeb'),  # Champ optionnel
                LinkedIn=request.form.get('LinkedIn'),  # Champ optionnel
                Biographie=request.form.get('Biographie'),  # Champ optionnel
                Photo=photo_filename  # Correspond au nom dans le modèle
            )
            
            db.session.add(professeur)
            db.session.commit()
            flash('Professeur ajouté avec succès!', 'success')
            return redirect(url_for('professeur.professeur'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout: {str(e)}", 'danger')
            # Pour débogage, vous pouvez imprimer l'erreur
            print(f"Erreur: {str(e)}")
            return render_template('professeur/ajouter_prof.html')  # Restez sur la même page avec les données
    
    return render_template('professeur/ajouter_prof.html')

@professeur_bp.route('/modifier_prof/<int:id>', methods=['GET', 'POST'])
def modifier_prof(id):
    professeur = Professeur.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Gestion du fichier photo
            if 'Photo' in request.files:
                photo = request.files['Photo']
                if photo.filename != '':
                    # Supprimer l'ancienne photo si elle existe
                    if professeur.Photo:
                        try:
                            os.remove(os.path.join('static/uploads', professeur.Photo))
                        except:
                            pass
                    
                    # Sauvegarder la nouvelle photo
                    photo_filename = secure_filename(photo.filename)
                    photo.save(os.path.join('static/uploads', photo_filename))
                    professeur.Photo = photo_filename

            # Mise à jour des champs
            professeur.nom = request.form.get('nom')
            professeur.prenom = request.form.get('prenom')
            professeur.Email = request.form.get('Email')
            professeur.Telephone = request.form.get('Telephone')
            professeur.date_naissance = request.form.get('date_naissance')
            professeur.genre = request.form.get('genre')
            professeur.Departement = request.form.get('Departement')
            professeur.Specialite = request.form.get('Specialite')
            professeur.Date_embauche = request.form.get('Date_embauche')
            professeur.status = request.form.get('status')
            professeur.address = request.form.get('address')
            professeur.siteWeb = request.form.get('siteWeb')
            professeur.LinkedIn = request.form.get('LinkedIn')
            professeur.Biographie = request.form.get('Biographie')
            
            db.session.commit()
            flash('Professeur modifié avec succès!', 'success')
            return redirect(url_for('professeur.professeur'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la modification: {str(e)}", 'danger')
    
    return render_template('professeur/modifier_prof.html', professeur=professeur)

@professeur_bp.route('/afficher_prof/<int:id>')
def afficher_prof(id):
    professeur = Professeur.query.get_or_404(id)
    return render_template('professeur/afficher_prof.html', professeur=professeur)

@professeur_bp.route('/supprimer_prof/<int:id>', methods=['POST'])
def supprimer_prof(id):
    professeur = Professeur.query.get_or_404(id)
    
    # Suppression de la photo si elle existe
    if professeur.Photo:
        try:
            os.remove(os.path.join('static/uploads', professeur.Photo))
        except:
            pass
    
    db.session.delete(professeur)
    db.session.commit()
    flash('Professeur supprimé avec succès!', 'success')
    return redirect(url_for('professeur.professeur'))