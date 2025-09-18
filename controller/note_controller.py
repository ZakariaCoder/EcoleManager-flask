from Model.etudiant import Etudiant
from Model.note import Note
from Model.bulletin import Bulletin
from Model.matiere import Matiere
from flask import Blueprint, render_template, request, flash, redirect, url_for
from extensions import db
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from flask import make_response

note_bp = Blueprint('note', __name__)

@note_bp.route('/note')
def note():
    # Get all students with their notes and bulletin information
    etudiants = Etudiant.query.all()
    
    # Prepare the student data with their averages and status
    student_data = []
    for etudiant in etudiants:
        # Get all notes for this student
        notes = Note.query.filter_by(etudiant_id=etudiant.id_etudiant).all()
        
        # Calculate average if notes exist
        moyenne = None
        if notes:
            moyenne = sum(note.note for note in notes) / len(notes)
        
        # Get bulletin information if exists
        bulletin = Bulletin.query.filter_by(etudiant_id=etudiant.id_etudiant).first()
        
        # Determine status and mention
        etat = "Non noté"
        mention = "Non applicable"
        
        if moyenne is not None:
            if moyenne >= 10:
                etat = "Admis"
                if moyenne >= 18:
                    mention = "Excellent"
                elif moyenne >= 16:
                    mention = "Très Bien"
                elif moyenne >= 14:
                    mention = "Bien"
                elif moyenne >= 12:
                    mention = "Assez Bien"
                elif moyenne >= 10:
                    mention = "Passable"
            elif moyenne >= 8:
                etat = "Rattrapage"
                mention = "Insuffisant"
            else:
                etat = "Ajourné"
                mention = "Insuffisant"
        
        # If bulletin exists, use its data
        if bulletin:
            etat = bulletin.Etat
            mention = bulletin.mention
            moyenne = bulletin.moyenne
        
        student_data.append({
            'id_etudiant': etudiant.id_etudiant,
            'prenom': etudiant.prenom,
            'nom': etudiant.nom,
            'Email': etudiant.Email,
            'class_': etudiant.class_,
            'Photo': etudiant.Photo,
            'moyenne': moyenne,
            'Etat': etat,
            'mention': mention
        })
    
    # Calculate statistics
    total_students = len(student_data)
    admitted_count = len([s for s in student_data if s['Etat'] == "Admis"])
    retake_count = len([s for s in student_data if s['Etat'] == "Rattrapage"])
    failed_count = len([s for s in student_data if s['Etat'] == "Ajourné"])
    
    return render_template('notes/note.html',
                         students=student_data,
                         total_students=total_students,
                         admitted_count=admitted_count,
                         retake_count=retake_count,
                         failed_count=failed_count)

@note_bp.route('/afficher_note/<int:id>')
def afficher_note(id):
    # Récupérer l'étudiant
    etudiant = Etudiant.query.get_or_404(id)
    
    # Récupérer toutes les notes avec les matières associées
    notes = db.session.query(Note, Matiere)\
        .join(Matiere, Note.matiere_id == Matiere.id_matiere)\
        .filter(Note.etudiant_id == id)\
        .all()
    
    # Calculer la moyenne générale et coefficients
    total_points = 0
    total_coefficients = 0
    notes_data = []
    
    for note, matiere in notes:
        total_points += note.note * note.coefficient
        total_coefficients += note.coefficient
        notes_data.append({
            'nom_matiere': matiere.nom_matiere,
            'coefficient': note.coefficient,
            'note': note.note,
            
        })
    
    moyenne = total_points / total_coefficients if total_coefficients > 0 else 0
    
    # Déterminer l'état et la mention
    etat = "Non noté"
    mention = "Non applicable"
    
    if moyenne > 0:
        if moyenne >= 10:
            etat = "Admis"
            if moyenne >= 18:
                mention = "Excellent"
            elif moyenne >= 16:
                mention = "Très Bien"
            elif moyenne >= 14:
                mention = "Bien"
            elif moyenne >= 12:
                mention = "Assez Bien"
            elif moyenne >= 10:
                mention = "Passable"
        elif moyenne >= 8:
            etat = "Rattrapage"
            mention = "Insuffisant"
        else:
            etat = "Ajourné"
            mention = "Insuffisant"
    
    # Statistiques de classe (exemple)
    class_stats = {
        'rank': 5,
        'class_average': 12.5,
        'total_students': 30,
        'matiere_averages': [
            {'matiere': 'Mathématiques', 'average': 14.2},
            {'matiere': 'Physique', 'average': 12.8},
            # ... autres matières
        ]
    }
    
    # Préparer les données pour le template
    stats = {
        'moyenne': moyenne,
        'etat': etat,
        'mention': mention,
        'total_coefficients': total_coefficients
    }
    
    return render_template('notes/afficher_note.html',
                         etudiant=etudiant,
                         notes=notes_data,
                         stats=stats,
                         class_stats=class_stats)
@note_bp.route('/ajouter_note/<int:id>', methods=['GET', 'POST'])
def ajouter_note(id):
    etudiant = Etudiant.query.get_or_404(id)
    matieres = Matiere.query.filter_by(classe=etudiant.class_).order_by(Matiere.nom_matiere).all()
    
    if request.method == 'POST':
        try:
            notes_submitted = False
            total_points = 0
            total_coefficients = 0
            
            # Récupérer les données du formulaire
            semester = request.form.get('semester')
            academic_year = request.form.get('academic_year')
            
            for matiere in matieres:
                note_key = f'note_{matiere.id_matiere}'
                if note_key in request.form and request.form[note_key]:
                    note_value = float(request.form[note_key])
                    coefficient = float(request.form.get(f'coefficient_{matiere.id_matiere}', matiere.coefficient))
                    
                    if 0 <= note_value <= 20:
                        new_note = Note(
                            etudiant_id=id,
                            matiere_id=matiere.id_matiere,
                            note=note_value,
                            coefficient=coefficient,
                            semester=semester,
                            academic_year=academic_year,
                            date=datetime.utcnow().date()
                        )
                        db.session.add(new_note)
                        notes_submitted = True
                        
                        # Calcul pour la moyenne
                        total_points += note_value * coefficient
                        total_coefficients += coefficient
            
            if notes_submitted:
                # Calcul de la moyenne
                moyenne = total_points / total_coefficients if total_coefficients > 0 else 0
                
                # Déterminer l'état et la mention
                etat = "Non noté"
                mention = "Non applicable"
                
                if moyenne > 0:
                    if moyenne >= 10:
                        etat = "Admis"
                        if moyenne >= 18:
                            mention = "Excellent"
                        elif moyenne >= 16:
                            mention = "Très Bien"
                        elif moyenne >= 14:
                            mention = "Bien"
                        elif moyenne >= 12:
                            mention = "Assez Bien"
                        elif moyenne >= 10:
                            mention = "Passable"
                    elif moyenne >= 8:
                        etat = "Rattrapage"
                        mention = "Insuffisant"
                    else:
                        etat = "Ajourné"
                        mention = "Insuffisant"
                
                # Vérifier si un bulletin existe déjà pour cet étudiant
                bulletin = Bulletin.query.filter_by(etudiant_id=id).first()
                
                if bulletin:
                    # Mettre à jour le bulletin existant
                    bulletin.moyenne = moyenne
                    bulletin.Etat = etat
                    bulletin.mention = mention
                    bulletin.updated_at = datetime.utcnow()
                else:
                    # Créer un nouveau bulletin
                    new_bulletin = Bulletin(
                        etudiant_id=id,
                        moyenne=moyenne,
                        Etat=etat,
                        mention=mention
                    )
                    db.session.add(new_bulletin)
                
                db.session.commit()
                flash('Notes et bulletin enregistrés avec succès!', 'success')
                return redirect(url_for('note.afficher_note', id=id))
            else:
                flash('Aucune note valide à enregistrer', 'warning')
                
        except ValueError:
            db.session.rollback()
            flash('Erreur: Veuillez entrer des notes valides (entre 0 et 20)', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'danger')
    
    return render_template('notes/ajouter_note.html',
                         etudiant=etudiant,
                         matieres=matieres)
@note_bp.route('/modifier_note/<int:id>', methods=['GET', 'POST'])
def modifier_note(id):
    etudiant = Etudiant.query.get_or_404(id)
    notes = Note.query.filter_by(etudiant_id=id).all()
    matieres = {note.matiere_id: Matiere.query.get(note.matiere_id) for note in notes}
    
    if request.method == 'POST':
        try:
            notes_updated = False
            total_points = 0
            total_coefficients = 0
            
            for note in notes:
                note_key = f'note_{note.id_note}'
                if note_key in request.form:
                    # Mettre à jour la note
                    new_note = float(request.form[note_key])
                    note.note = new_note
                    
                    # Mettre à jour le coefficient
                    coeff_key = f'coefficient_{note.id_note}'
                    if coeff_key in request.form:
                        note.coefficient = float(request.form[coeff_key])
                    
                    # Mettre à jour l'appréciation
                    appreciation_key = f'appreciation_{note.id_note}'
                    if appreciation_key in request.form:
                        note.appreciation = request.form[appreciation_key]
                    
                    note.updated_at = datetime.utcnow()
                    notes_updated = True
                    
                    # Calcul pour la moyenne
                    total_points += note.note * note.coefficient
                    total_coefficients += note.coefficient
            
            if notes_updated:
                # Calcul de la nouvelle moyenne
                moyenne = total_points / total_coefficients if total_coefficients > 0 else 0
                
                # Déterminer le nouvel état et mention
                etat = "Non noté"
                mention = "Non applicable"
                
                if moyenne > 0:
                    if moyenne >= 10:
                        etat = "Admis"
                        if moyenne >= 18:
                            mention = "Excellent"
                        elif moyenne >= 16:
                            mention = "Très Bien"
                        elif moyenne >= 14:
                            mention = "Bien"
                        elif moyenne >= 12:
                            mention = "Assez Bien"
                        elif moyenne >= 10:
                            mention = "Passable"
                    elif moyenne >= 8:
                        etat = "Rattrapage"
                        mention = "Insuffisant"
                    else:
                        etat = "Ajourné"
                        mention = "Insuffisant"
                
                # Mettre à jour le bulletin
                bulletin = Bulletin.query.filter_by(etudiant_id=id).first()
                if bulletin:
                    bulletin.moyenne = moyenne
                    bulletin.Etat = etat
                    bulletin.mention = mention
                    bulletin.updated_at = datetime.utcnow()
                else:
                    new_bulletin = Bulletin(
                        etudiant_id=id,
                        moyenne=moyenne,
                        Etat=etat,
                        mention=mention
                    )
                    db.session.add(new_bulletin)
                
                db.session.commit()
                flash('Notes et bulletin mis à jour avec succès!', 'success')
                return redirect(url_for('note.afficher_note', id=id))
            else:
                flash('Aucune modification à enregistrer', 'warning')
                
        except ValueError:
            db.session.rollback()
            flash('Erreur: Veuillez entrer des notes valides (entre 0 et 20)', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'danger')
    
    return render_template('notes/modifier_note.html',
                        etudiant=etudiant,
                        notes=notes,
                        matieres=matieres)
@note_bp.route('/generer_bulletin_pdf/<int:id>')
def generer_bulletin_pdf(id):
    # Récupérer les données de l'étudiant
    etudiant = Etudiant.query.get_or_404(id)
    notes = db.session.query(Note, Matiere)\
        .join(Matiere, Note.matiere_id == Matiere.id_matiere)\
        .filter(Note.etudiant_id == id)\
        .all()
    
    # Calculer la moyenne
    total_points = sum(note.note * note.coefficient for note, _ in notes)
    total_coefficients = sum(note.coefficient for note, _ in notes)
    moyenne = total_points / total_coefficients if total_coefficients > 0 else 0
    
    # Déterminer statut et mention
    if moyenne >= 10:
        etat = "Admis"
        if moyenne >= 18: mention = "Excellent"
        elif moyenne >= 16: mention = "Très Bien"
        elif moyenne >= 14: mention = "Bien"
        elif moyenne >= 12: mention = "Assez Bien"
        else: mention = "Passable"
    elif moyenne >= 8:
        etat = "Rattrapage"
        mention = "Insuffisant"
    else:
        etat = "Ajourné"
        mention = "Insuffisant"

    # Créer le PDF en mémoire
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,
        spaceAfter=20
    )
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=10
    )
    normal_style = styles['Normal']
    
    # Entête du bulletin
    elements.append(Paragraph("BULLETIN SCOLAIRE", title_style))
    elements.append(Paragraph("Année Académique 2023-2024", styles['Heading2']))
    
    # Informations de l'étudiant
    student_info = [
        ["Nom:", etudiant.nom],
        ["Prénom:", etudiant.prenom],
        ["Classe:", etudiant.class_],
        ["Date de naissance:", etudiant.date_naissance.strftime('%d/%m/%Y') if etudiant.date_naissance else "-"],
        ["Date d'édition:", datetime.now().strftime('%d/%m/%Y %H:%M')]
    ]
    
    student_table = Table(student_info, colWidths=[100, 300])
    student_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 20))
    
    # Tableau des notes
    elements.append(Paragraph("RÉSULTATS SCOLAIRES", header_style))
    
    note_data = [["Matière", "Coeff.", "Note", "Appréciation"]]
    for note, matiere in notes:
        note_data.append([
            matiere.nom_matiere,
            str(note.coefficient),
            f"{note.note:.2f}/20",
           
        ])
    
    notes_table = Table(note_data, colWidths=[250, 50, 50, 100])
    notes_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4472C4')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#D9E1F2')),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,1), (-1,-1), 9),
    ]))
    elements.append(notes_table)
    elements.append(Spacer(1, 20))
    
    # Résultats
    elements.append(Paragraph("RÉSULTAT FINAL", header_style))
    
    result_data = [
        ["Moyenne Générale:", f"{moyenne:.2f}/20"],
        ["Statut:", etat],
        ["Mention:", mention],
        ["Total Coefficients:", str(total_coefficients)]
    ]
    
    result_table = Table(result_data, colWidths=[150, 100])
    result_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F2F2F2')),
    ]))
    elements.append(result_table)
    elements.append(Spacer(1, 30))
    
    # Signature
    signature_data = [
        ["", "Le Directeur"],
        ["", "Signature & Cachet"]
    ]
    signature_table = Table(signature_data, colWidths=[300, 150])
    signature_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
    ]))
    elements.append(signature_table)
    
    # Générer le PDF
    doc.build(elements)
    
    # Retourner le PDF
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=bulletin_{etudiant.nom}_{etudiant.prenom}.pdf'
    return response