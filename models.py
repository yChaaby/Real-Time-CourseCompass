class Formation:
    def __init__(self, id_formation, domaine_categorie, sous_domaine_categorie, formation_cours):
        self.ID_FORMATION = id_formation
        self.DOMAINE_CATGEGORIE = domaine_categorie
        self.SOUS_DOMAINE_CATEGORIE = sous_domaine_categorie
        self.FORMATION_COURS = formation_cours

    def __str__(self):
        return f"{self.FORMATION_COURS} - {self.SOUS_DOMAINE_CATEGORIE} "
    
class Formateur:
    def __init__(self, nom_formateur, formation_id, site_web, numero, adresse):
        self.NOM_FORMATEUR = nom_formateur
        self.FORMATION_ID = formation_id
        self.SITE_WEB = site_web
        self.NUMERO = numero
        self.ADRESSE = adresse

    def __str__(self):
        return f" {self.NOM_FORMATEUR} || "