import pandas as pd
import os
from datetime import datetime

# Créer le dossier test_files s'il n'existe pas
if not os.path.exists('test_files'):
    os.makedirs('test_files')

# 1. Fichier pour l'importation d'étudiants (noms marocains)
etudiants_data = {
    'nom': ['El Amrani', 'Benjelloun', 'Cherkaoui', 'Lahlou', 'Bennani'],
    'prenom': ['Ahmed', 'Fatima', 'Mehdi', 'Amina', 'Youssef'],
    'Email': ['ahmed.elamrani@email.com', 'fatima.benjelloun@email.com', 
              'mehdi.cherkaoui@email.com', 'amina.lahlou@email.com', 'youssef.bennani@email.com'],
    'date_naissance': ['2000-05-15', '2001-02-20', '1999-11-30', '2000-08-22', '2001-03-10'],
    'telephone': ['0612345678', '0623456789', '0634567890', '0645678901', '0656789012'],
    'class': ['GI3', 'GI1', 'GAE3', 'GAE1', 'GI3'],  # Répartition entre GI et GAE
    'address': ['123 Rue Hassan II, Casablanca', '456 Avenue Mohammed V, Rabat', 
                '789 Boulevard Zerktouni, Marrakech', '101 Rue Al Massira, Fès', '202 Avenue Palestine, Tanger'],
    'Photo': ['', '', '', '', ''],
    'annee_universitaire': ['2023-2024', '2023-2024', '2023-2024', '2023-2024', '2023-2024'],
    'genre': ['M', 'F', 'M', 'F', 'M'],
    'date_inscription': ['2023-09-01', '2023-09-01', '2023-09-01', '2023-09-01', '2023-09-01']
}

# 2. Fichier pour l'importation de professeurs (noms marocains)
professeurs_data = {
    'nom': ['El Fassi', 'Bouzoubaa', 'Mansouri'],
    'prenom': ['Karim', 'Leila', 'Hicham'],
    'Email': ['karim.elfassi@email.com', 'leila.bouzoubaa@email.com', 'hicham.mansouri@email.com'],
    'date_naissance': ['1975-04-12', '1980-07-25', '1978-09-30'],
    'Telephone': ['0712345678', '0723456789', '0734567890'],
    'address': ['12 Rue des Universités, Casablanca', '25 Avenue des Sciences, Rabat', '30 Boulevard des Facultés, Fès'],
    'Photo': ['', '', ''],
    'genre': ['M', 'F', 'M'],
    'Departement': ['Informatique', 'Mathématiques', 'Gestion'],
    'Specialite': ['Réseaux', 'Algèbre', 'Comptabilité'],
    'siteWeb': ['www.kelfassi.com', 'www.lbouzoubaa.com', 'www.hmansouri.com'],
    'annee_universitaire': ['2023-2024', '2023-2024', '2023-2024'],
    'Date_embauche': ['2010-09-01', '2015-09-01', '2012-09-01'],
    'LinkedIn': ['linkedin.com/kelfassi', 'linkedin.com/lbouzoubaa', 'linkedin.com/hmansouri'],
    'Biographie': ['Expert en réseaux informatiques', 'Spécialiste en algèbre linéaire', 'Expert-comptable certifié'],
    'status': ['active', 'active', 'active']
}

# 3. Fichier pour l'importation de matières (adaptées à GI et GAE)
matieres_data = {
    'nom_matiere': [
        'Base de données',          # GI
        'Réseaux Informatiques',    # GI
        'Programmation Web',        # GI
        'Comptabilité Générale',    # GAE
        'Marketing Digital',        # GAE
        'Systèmes d\'Information',  # Commun
        'Mathématiques Financières' # GAE
    ],
    'coefficient': [2.0, 1.5, 1.5, 2.0, 1.5, 1.0, 2.0],
    'volume_horaire': [60, 45, 45, 60, 45, 30, 60],
    'semestre': ['S1', 'S1', 'S2', 'S1', 'S2', 'S1', 'S2'],
    'classe': ['GI3', 'GI3', 'GI3', 'GAE3', 'GAE3', 'GI3', 'GAE3'],
    'annee_universitaire': ['2023-2024']*7,
    'id_prof': [1, 1, 1, 3, 3, 2, 2]  # Correspondance avec les professeurs
}

# 4. Fichier pour l'importation de notes
notes_data = {
    'etudiant_id': [1, 1, 1, 2, 2, 3, 3, 4, 5, 5],  # IDs étudiants
    'matiere_id': [1, 2, 6, 1, 6, 4, 7, 4, 1, 3],   # IDs matières
    'note': [15.5, 18.0, 14.0, 12.5, 16.0, 13.5, 17.0, 14.5, 19.0, 15.0],
    'coefficient': [2.0, 1.5, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.5],  # Ajout des coefficients
    'semester': ['S1', 'S1', 'S1', 'S1', 'S1', 'S1', 'S2', 'S1', 'S1', 'S2'],
    'academic_year': ['2023-2024']*10,
    'date': ['2023-12-15', '2023-12-18', '2024-01-10', '2023-12-16', '2024-01-12', 
             '2023-12-20', '2024-02-05', '2023-12-22', '2023-12-17', '2024-02-10']
}

# Créer les DataFrames
df_etudiants = pd.DataFrame(etudiants_data)
df_professeurs = pd.DataFrame(professeurs_data)
df_matieres = pd.DataFrame(matieres_data)
df_notes = pd.DataFrame(notes_data)

# Sauvegarder en Excel avec le bon format
with pd.ExcelWriter('test_files/import_etudiants.xlsx') as writer:
    df_etudiants.to_excel(writer, index=False, sheet_name='Étudiants')

with pd.ExcelWriter('test_files/import_professeurs.xlsx') as writer:
    df_professeurs.to_excel(writer, index=False, sheet_name='Professeurs')

with pd.ExcelWriter('test_files/import_matieres.xlsx') as writer:
    df_matieres.to_excel(writer, index=False, sheet_name='Matières')

with pd.ExcelWriter('test_files/import_notes.xlsx') as writer:
    df_notes.to_excel(writer, index=False, sheet_name='Notes')

print("Fichiers Excel générés avec succès dans le dossier test_files/")