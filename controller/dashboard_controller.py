from datetime import datetime, timedelta
from flask import render_template
from Model.etudiant import Etudiant
from Model.professeur import Professeur
from flask import Blueprint
dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/dashboard')
def dashboard():
    # Calcul des statistiques
    total_etudiants = Etudiant.query.count()
    total_professeurs = Professeur.query.count()
    
    # Vous devrez adapter ces parties selon vos autres modèles
    total_classes = 0  # À remplacer par votre modèle de classes
    total_notes = 0    # À remplacer par votre modèle de notes
    
    # Calcul des changements ce mois-ci
    last_month = datetime.now() - timedelta(days=30)
    
    etudiants_last_month = Etudiant.query.filter(
        Etudiant.date_inscription >= last_month
    ).count()
    etudiants_change = round(etudiants_last_month / (total_etudiants - etudiants_last_month)) * 100 if total_etudiants > etudiants_last_month else 0
    
    professeurs_last_month = Professeur.query.filter(
        Professeur.Date_embauche >= last_month
    ).count()
    professeurs_change = round(professeurs_last_month / (total_professeurs - professeurs_last_month)) * 100 if total_professeurs > professeurs_last_month else 0
    
    # Récupération des derniers étudiants
    derniers_etudiants = Etudiant.query.order_by(
        Etudiant.date_inscription.desc()
    ).limit(5).all()
    
    # Récupération des derniers professeurs
    derniers_professeurs = Professeur.query.order_by(
        Professeur.Date_embauche.desc()
    ).limit(5).all()
    
    return render_template('dashboard/index.html', 
        stats={
            'total_etudiants': total_etudiants,
            'total_professeurs': total_professeurs,
            'total_classes': total_classes,
            'total_notes': total_notes,
            'etudiants_change': etudiants_change,
            'professeurs_change': professeurs_change,
            'nouvelles_classes': 0,  # À adapter
            'nouvelles_notes': 0     # À adapter
        },
        derniers_etudiants=derniers_etudiants,
        derniers_professeurs=derniers_professeurs
    )