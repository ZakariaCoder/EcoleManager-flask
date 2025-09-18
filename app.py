from flask import Flask, render_template, redirect, url_for
import datetime
from extensions import db
from Config import Config
from flask_migrate import Migrate

import os
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from Model.user import User  # Importez ici pour éviter les dépendances circulaires
    return User.query.get(int(user_id))
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
   
    
    # Initialisez login_manager avec l'app
    login_manager.init_app(app)
    # Initialisation des extensions
    db.init_app(app)
    migrate = Migrate()          
    migrate.init_app(app, db)
    
    # Import des modèles
    with app.app_context():
        from Model import etudiant, professeur, matiere, note, bulletin, importation, user
    
    # Enregistrement des blueprints
    register_blueprints(app)
    
    # Routes de base
    register_routes(app)
    
    # Context processor for templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.datetime.now()}
    
    return app

def register_blueprints(app):
    from controller.etudiant_controller import etudiant_bp
    app.register_blueprint(etudiant_bp, url_prefix='/etudiant')
    from controller.professeur_controller import professeur_bp
    app.register_blueprint(professeur_bp, url_prefix='/professeur')
    from controller.import_controller import import_bp
    app.register_blueprint(import_bp, url_prefix='/import')
    from controller.matiere_controller import matiere_bp
    app.register_blueprint(matiere_bp, url_prefix='/matiere')
    from controller.dashboard_controller import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    from controller.user_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Optionnel: ajoute un préfixe URL
    from controller.note_controller import note_bp
    app.register_blueprint(note_bp, url_prefix='/note')
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
    
#     # Configuration des uploads
#     app.config['UPLOAD_FOLDER'] = 'uploads/imports'
#     app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv'}
    
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])

#     # Initialisation des extensions
#     db.init_app(app)
#     migrate = Migrate(app, db)
    
#     # Import des modèles
#     with app.app_context():
#         from Model import etudiant, professeur, matiere, note, bulletin, importation, user
    
#     # Enregistrement des blueprints
#     register_blueprints(app)
    
#     # Routes de base
#     register_routes(app)
    
#     return app

# def register_blueprints(app):
#     from controller.etudiant_controller import etudiant_bp
#     from controller.import_controller import import_bp
    
#     app.register_blueprint(etudiant_bp, url_prefix='/etudiant')
#     app.register_blueprint(import_bp, url_prefix='/import')

def register_routes(app):
    # @app.route('/')
    # def home():
    #     return redirect(url_for('login'))

    # # Auth routes
    # @app.route('/register')
    # def register():
    #     return render_template('auth/register.html')

    # @app.route('/login')
    # def login():
    #     return render_template('auth/login.html')

    # Dashboard
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard/index.html')

    # Notes routes
    @app.route('/note')
    def note():
        return render_template('notes/note.html')

    @app.route('/ajouter_note')
    def ajouter_note():
        return render_template('notes/ajouter_note.html')

    @app.route('/afficher_note')
    def afficher_note():
        return render_template('notes/afficher_note.html')

    @app.route('/modifier_note')
    def modifier_note():
        return render_template('notes/modifier_note.html')

    # Professeur routes
    # @app.route('/professeur')
    # def professeur():
    #     return render_template('professeur/professeur.html')

      # @app.route('/ajouter_prof')
      # def ajouter_prof():
      #     return render_template('professeur/ajouter_prof.html')

    # @app.route('/modifier_prof')
    # def modifier_prof():
    #     return render_template('professeur/modifier_prof.html')

    # @app.route('/afficher_prof')
    # def afficher_prof():
    #     return render_template('professeur/afficher_prof.html')

    # # Matières routes
    # @app.route('/modifier_matiere')
    # def modifier_matiere():
    #     return render_template('matieres/modifier_matiere.html')

    # @app.route('/matiere')
    # def matiere():
    #     return render_template('matieres/matiere.html')
    # @app.route('/importation')
    # def importation():
    #     return render_template('document/importation.html')

    # Autres routes
    @app.route('/calendrier')
    def calendrier():
        return render_template('calendrier/calendrier.html')

    @app.route('/deconnexion')
    def deconnexion():
        return redirect(url_for('auth.login'))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

from flask import make_response
from fpdf import FPDF

    #  @app.route('/download_bulletin')
    #  def download_bulletin():
    # pdf = FPDF()
    # pdf.add_page()
    
    # # --- EN-TÊTE AVEC LOGO ET TITRE ---
    # # Ajoute le logo (remplace le chemin par le tien)
    # pdf.image("static/img/logo.png", x=10, y=8, w=25)
    # pdf.set_xy(40, 10)
    # pdf.set_font("Arial", 'B', 16)
    # pdf.cell(0, 10, "Établissement Scolaire XYZ", ln=1, align='C')
    # pdf.set_xy(10, 25)
    # pdf.set_font("Arial", 'B', 14)
    # pdf.cell(0, 10, "Bulletin de Notes", ln=1, align='C')
    # pdf.set_font("Arial", '', 12)
    # pdf.cell(0, 8, "Année universitaire : 2023-2024", ln=1, align='C')
    # pdf.ln(5)
    
    # # --- INFOS ÉTUDIANT ---
    # pdf.set_font("Arial", 'B', 12)
    # pdf.set_fill_color(230, 230, 250)
    # pdf.cell(0, 8, "Informations de l'étudiant", ln=1, fill=True)
    # pdf.set_font("Arial", '', 12)
    # student_info = [
    #     "Nom: Jean Dupont",
    #     "ID Étudiant: #1001",
    #     "Classe: L2",
    #     "Année: 2023-2024",
    #     "Semestre: S3"
    # ]
    # for info in student_info:
    #     pdf.cell(0, 8, info, ln=1)
    # pdf.ln(3)
    
    # # --- TABLEAU DES NOTES ---
    # pdf.set_font("Arial", 'B', 12)
    # pdf.set_fill_color(200, 220, 255)
    # pdf.cell(80, 10, "Matière", 1, 0, 'C', 1)
    # pdf.cell(30, 10, "Coefficient", 1, 0, 'C', 1)
    # pdf.cell(30, 10, "Note", 1, 0, 'C', 1)
    # pdf.cell(30, 10, "Points", 1, 1, 'C', 1)
    
    # subjects = [
    #     {"name": "Mathématiques", "coef": 4, "grade": 16.5, "points": 66.0},
    #     {"name": "Français", "coef": 3, "grade": 15.0, "points": 45.0},
    #     {"name": "Anglais", "coef": 2, "grade": 14.0, "points": 28.0},
    #     {"name": "Informatique", "coef": 5, "grade": 17.0, "points": 85.0},
    #     {"name": "Physique", "coef": 4, "grade": 15.5, "points": 62.0}
    # ]
    # pdf.set_font("Arial", '', 12)
    # fill = False
    # for subject in subjects:
    #     pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
    #     pdf.cell(80, 10, subject["name"], 1, 0, 'L', fill)
    #     pdf.cell(30, 10, str(subject["coef"]), 1, 0, 'C', fill)
    #     pdf.cell(30, 10, str(subject["grade"]), 1, 0, 'C', fill)
    #     pdf.cell(30, 10, str(subject["points"]), 1, 1, 'C', fill)
    #     fill = not fill
    # pdf.ln(3)
    
    # # --- MOYENNE ET MENTION ---
    # pdf.set_font("Arial", 'B', 12)
    # pdf.set_fill_color(230, 230, 250)
    # pdf.cell(0, 8, f"Moyenne Générale: 15.75    Mention: Bien", ln=1, fill=True)
    # pdf.ln(5)
    
    # # --- PIED DE PAGE ---
    # pdf.set_y(-40)
    # pdf.set_font("Arial", '', 11)
    # pdf.cell(0, 8, f"Date d'édition : {datetime.date.today().strftime('%d/%m/%Y')}", ln=1)
    # pdf.cell(0, 8, "Signature du responsable : ____________________", ln=1)
    # pdf.ln(5)
    # pdf.set_font("Arial", 'I', 10)
    # pdf.set_text_color(120, 120, 120)
    # pdf.cell(0, 8, "Document généré automatiquement - Ne pas signer à la main", ln=1, align='C')
    
    # # --- ENVOI DU PDF ---
    # response = make_response(pdf.output(dest='S').encode('latin1'))
    # response.headers.set('Content-Disposition', 'attachment', filename='bulletin_notes.pdf')
    # response.headers.set('Content-Type', 'application/pdf')
    # return response

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)