from datetime import datetime

class Conge:
    def __init__(self, date_debut, date_fin):
        self.date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
        self.date_fin = datetime.strptime(date_fin, "%Y-%m-%d")

        if self.date_fin < self.date_debut:
            raise ValueError("Date fin antérieure à date début")

    def calculer_jours(self):
        return (self.date_fin - self.date_debut).days + 1

class CongeAnnuel(Conge):
    def calculer_jours(self):
        return super().calculer_jours()

class CongeExceptionnel(Conge):
    def calculer_jours(self):
        return super().calculer_jours()

class CongeMaladie(Conge):
    def calculer_jours(self):
        return 0   # ne consomme pas le solde
