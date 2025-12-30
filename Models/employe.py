class Employe:
    def __init__(self, id, matricule, nom, prenom, service, solde_conges):
        self.id = id
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.service = service
        self._solde_conges = solde_conges  # encapsulation

    def get_solde(self):
        return self._solde_conges

    def debiter(self, jours):
        if jours > self._solde_conges:
            raise ValueError("Solde insuffisant")
        self._solde_conges -= jours

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"
