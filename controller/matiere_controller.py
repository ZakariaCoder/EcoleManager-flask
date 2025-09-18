from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from Model.matiere import Matiere
from Model.professeur import Professeur
import os

matiere_bp = Blueprint('matiere', __name__)

@matiere_bp.route('/afficher_mat/<int:id>')
def afficher_mat(id):
    matiere = db.session.query(
        Matiere,
        Professeur.nom.label('prof_nom'),
        Professeur.prenom.label('prof_prenom')
    ).join(
        Professeur, 
        Matiere.id_prof == Professeur.id_prof,
        isouter=True
    ).filter(Matiere.id_matiere == id).first_or_404()
    
    return render_template('matieres/afficher_mat.html', matiere=matiere)

@matiere_bp.route('/ajouter_mat', methods=['GET', 'POST'])
def ajouter_mat():
    if request.method == 'POST':
        try:
            # Gestion correcte de l'ID professeur
            professeur_id = request.form.get('professeur_id')
            id_prof = int(professeur_id) if professeur_id else None  # None si vide
            
            nouvelle_matiere = Matiere(
                nom_matiere=request.form['nom_matiere'],
                coefficient=float(request.form['coefficient']),
                volume_horaire=int(request.form['volume_horaire']),
                semestre=request.form['semestre'],
                classe=request.form['classe'],
                annee_universitaire=request.form['annee_universitaire'],
                id_prof=id_prof  # Utilisation de la variable correctement gérée
            )
            
            db.session.add(nouvelle_matiere)
            db.session.commit()
            flash('Matière ajoutée avec succès!', 'success')
            return redirect(url_for('matiere.matiere'))
            
        except ValueError as e:
            db.session.rollback()
            flash("Veuillez entrer des valeurs valides pour les champs numériques", 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout: {str(e)}", 'danger')
            print(f"Erreur détaillée: {str(e)}")  # Pour le débogage
    
    professeurs = Professeur.query.all()
    return render_template('matieres/ajouter_mat.html', professeurs=professeurs)

@matiere_bp.route('/modifier_mat/<int:id>', methods=['GET', 'POST'])
def modifier_mat(id):
    matiere = Matiere.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Gestion de l'ID professeur
            professeur_id = request.form.get('professeur_id')
            id_prof = int(professeur_id) if professeur_id else None
            
            # Mise à jour des champs
            matiere.nom_matiere = request.form['nom_matiere']
            matiere.coefficient = float(request.form['coefficient'])
            matiere.volume_horaire = int(request.form['volume_horaire'])
            matiere.semestre = request.form['semestre']
            matiere.classe = request.form['classe']
            matiere.annee_universitaire = request.form['annee_universitaire']
            matiere.id_prof = id_prof
            
            db.session.commit()
            flash('Matière modifiée avec succès!', 'success')
            return redirect(url_for('matiere.matiere'))
            
        except ValueError as e:
            db.session.rollback()
            flash("Veuillez entrer des valeurs valides pour les champs numériques", 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la modification: {str(e)}", 'danger')
    
    # Récupérer la liste des professeurs pour le select
    professeurs = Professeur.query.all()
    
    return render_template('matieres/modifier_mat.html',
                         matiere=matiere,
                         professeurs=professeurs)

@matiere_bp.route('/supprimer_mat/<int:id>', methods=['POST'])
def supprimer_mat(id):
    matiere = Matiere.query.get_or_404(id)
    
    try:
        db.session.delete(matiere)
        db.session.commit()
        flash('Matière supprimée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression: {str(e)}", 'danger')
    
    return redirect(url_for('matiere.matiere'))

@matiere_bp.route('/matiere')
def matiere():
    # Récupérer toutes les matières avec les noms des professeurs
    matieres = db.session.query(
        Matiere,
        Professeur.nom.label('prof_nom'),
        Professeur.prenom.label('prof_prenom')
    ).join(
        Professeur, 
        Matiere.id_prof == Professeur.id_prof,
        isouter=True
    ).all()
    
    return render_template('matieres/matiere.html', matieres=matieres)