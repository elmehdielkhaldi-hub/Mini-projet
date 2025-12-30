📅 Mini-projet Python – Gestion des congés
1. Description

Ce projet permet de gérer les congés d’une entreprise via une application Python avec interface web Streamlit et base de données SQLite.

Fonctionnalités :

Gestion des employés (ajout, consultation)

Création de demandes de congé (annuel, exceptionnel, maladie)

Validation ou refus des demandes par le responsable RH

Contrôle automatique du solde de congés

Mise à jour immédiate du solde après acceptation

2. Organisation des fichiers
Mini-projet/
│
├─ Models/
│   ├─ demande_conger.py    # Classes Conge et ses sous-classes
│   └─ gestion_conge.py     # Classe GestionConges (logique métier + accès SQLite)
│
├─ database/
│   └─ conges.db            # Base SQLite (créée automatiquement)
│
├─ app.py                   # Interface Streamlit
└─ README.md

3. Installation des dépendances

Installer Python 3.7+

Installer les librairies nécessaires :

pip install streamlit pandas

4. Lancement de l’application

Depuis le terminal, à la racine du projet :

streamlit run app.py


L’interface web s’ouvrira automatiquement dans ton navigateur.

5. Initialisation de la base

La base conges.db est créée automatiquement si elle n’existe pas.

Des employés de test sont insérés automatiquement :

Ali Dupont – IT – solde 22 jours

Sara Martin – RH – solde 18 jours

6. Scénario de test minimal

Employés

Vérifier les employés existants

Ajouter un nouvel employé

Nouvelle demande

Sélectionner un employé

Indiquer les dates de début/fin

Sélectionner le type de congé

Ajouter un commentaire

Envoyer la demande

Validation RH

Consulter les demandes en attente

Accepter ou refuser la demande

Vérifier que le solde de l’employé est mis à jour automatiquement

Les congés maladie ne modifient pas le solde

Demandes

Consulter toutes les demandes pour vérifier le statut et les informations

7. Réponses aux questions de réflexion
7.1 Encapsulation et intégrité des données

Attribut protégé : _solde_conges (ne peut être modifié que par traiter_demande)

Exemple : contrôle du solde avant acceptation, mise à jour en base seulement si suffisant.

7.2 Héritage et polymorphisme

Classe Conge → base pour CongeAnnuel, CongeExceptionnel, CongeMaladie

Méthode polymorphe : calculer_jours()

Les données sont stockées dans demandes_conge avec le type de congé (type_conge)

7.3 Gestion et couche DAO

GestionConges : création de tables, gestion employés, gestion demandes, contrôle solde

Méthode spécifique à la gestion : traiter_demande()

Les requêtes SQL sont isolées de la logique métier

7.4 Évolutivité

Ajouter de nouveaux types d’absences : créer de nouvelles classes héritant de Conge

Schéma SQLite : ajouter type_conge ou nouvelle table type_absence

Interface : ajouter les nouvelles options dans le selectbox

7.5 Concepts POO

Encapsulation : _solde_conges

Héritage : Conge → sous-classes

Polymorphisme : calculer_jours()

Abstraction : Conge définit l’interface commune

8. Notes complémentaires

Interface web basée sur Streamlit, responsive et simple à utiliser

Base SQLite persistante, pas besoin de serveur

Tableaux mis à jour automatiquement après validation RH
