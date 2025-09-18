from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from extensions import db
from Model.user import User

# Création du Blueprint avec le dossier de templates spécifié
auth_bp = Blueprint('auth', __name__)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user
from Model.user import User  # Importez votre modèle User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email').strip()  # Nettoyage de l'email
        password = request.form.get('password')
        
        # Validation basique
        if not email or not password:
            flash('Tous les champs sont obligatoires', 'error')
            return redirect(url_for('auth.login'))

        # Recherche de l'utilisateur
        user = User.query.filter_by(email=email).first()
        
        # Vérification
        if not user or not check_password_hash(user.password, password):
            flash('Identifiants incorrects', 'error')  # Message générique pour la sécurité
            return redirect(url_for('auth.login'))
        
        # Connexion (avec vérification implicite de is_active via UserMixin)
        login_user(user)
        flash('Connexion réussie', 'success')
        
        # Redirection sécurisée (évite les open redirects)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    try:
        # Récupération des données du formulaire
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation des données
        if not all([username, email, password, confirm_password]):
            flash('Tous les champs sont obligatoires', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'error')
            return redirect(url_for('auth.register'))

        # Création de l'utilisateur
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
         
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Compte créé avec succès! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('auth.login'))

    except Exception as e:
        db.session.rollback()  # Annulation des changements en cas d'erreur
        flash(f"Une erreur est survenue: {str(e)}", 'error')
        return redirect(url_for('auth.register'))
   

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('auth.login'))  # Préfix 'auth.'