import sqlite3
from Models.demande_conger import CongeAnnuel, CongeExceptionnel, CongeMaladie

class GestionConges:
    def __init__(self, db_path="database/conges.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.creer_tables()
        self.initialiser_donnees_test()

    # ----------------- Base de données -----------------
    def creer_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT UNIQUE,
                nom TEXT,
                prenom TEXT,
                service TEXT,
                solde_conges INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS demandes_conge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employe_id INTEGER,
                date_debut TEXT,
                date_fin TEXT,
                type_conge TEXT,
                statut TEXT,
                commentaire TEXT
            )
        """)
        self.conn.commit()

    def initialiser_donnees_test(self):
        self.cursor.execute("SELECT COUNT(*) FROM employes")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("""
                INSERT INTO employes (matricule, nom, prenom, service, solde_conges)
                VALUES 
                ('E001','Dupont','Ali','IT',22),
                ('E002','Martin','Sara','RH',18)
            """)
            self.conn.commit()

    # ----------------- Employés -----------------
    def lister_employes(self):
        self.cursor.execute("SELECT * FROM employes")
        return [dict(row) for row in self.cursor.fetchall()]

    def ajouter_employe(self, matricule, nom, prenom, service, solde):
        self.cursor.execute("""
            INSERT INTO employes (matricule, nom, prenom, service, solde_conges)
            VALUES (?, ?, ?, ?, ?)
        """, (matricule, nom, prenom, service, solde))
        self.conn.commit()

    # ----------------- Congés -----------------
    def creer_conge(self, type_conge, date_debut, date_fin):
        if type_conge == "Annuel":
            return CongeAnnuel(date_debut, date_fin)
        elif type_conge == "Exceptionnel":
            return CongeExceptionnel(date_debut, date_fin)
        else:
            return CongeMaladie(date_debut, date_fin)

    def ajouter_demande(self, employe_id, date_debut, date_fin, type_conge, commentaire):
        conge = self.creer_conge(type_conge, date_debut, date_fin)
        conge.calculer_jours()  # valide dates

        self.cursor.execute("""
            INSERT INTO demandes_conge
            (employe_id, date_debut, date_fin, type_conge, statut, commentaire)
            VALUES (?, ?, ?, ?, 'En attente', ?)
        """, (employe_id, date_debut, date_fin, type_conge, commentaire))
        self.conn.commit()

    def lister_demandes(self, statut=None):
        if statut:
            self.cursor.execute("SELECT * FROM demandes_conge WHERE statut=?", (statut,))
        else:
            self.cursor.execute("SELECT * FROM demandes_conge")
        return [dict(row) for row in self.cursor.fetchall()]

    # ----------------- Traitement RH -----------------
    def traiter_demande(self, demande_id, accepter):
        self.cursor.execute("SELECT * FROM demandes_conge WHERE id=?", (demande_id,))
        d = self.cursor.fetchone()
        if not d or d["statut"] != "En attente":
            return "Déjà traitée"

        conge = self.creer_conge(d["type_conge"], d["date_debut"], d["date_fin"])
        jours = conge.calculer_jours()
        statut = "Refusé"

        if accepter:
            if d["type_conge"] in ["Annuel", "Exceptionnel"]:
                self.cursor.execute("SELECT solde_conges FROM employes WHERE id=?", (d["employe_id"],))
                solde = self.cursor.fetchone()["solde_conges"]
                if solde >= jours:
                    statut = "Accepté"
                    self.cursor.execute(
                        "UPDATE employes SET solde_conges = solde_conges - ? WHERE id=?",
                        (jours, d["employe_id"])
                    )
                else:
                    statut = "Refusé"
            else:
                statut = "Accepté"

        self.cursor.execute(
            "UPDATE demandes_conge SET statut=? WHERE id=?",
            (statut, demande_id)
        )
        self.conn.commit()
        return statut
