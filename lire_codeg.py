class LecteurCodeG:
    def __init__(self, chemin_fichier):
        self.chemin_fichier = chemin_fichier
        self.couches = self._lire_codeg()

    def _lire_codeg(self):
        with open(self.chemin_fichier, 'r') as fichier:
            lignes = fichier.readlines()
        return self._diviser_en_couches(lignes)

    def _diviser_en_couches(self, lignes):
        couches = []
        couche_actuelle = []

        for ligne in lignes:
            if ligne.startswith(';LAYER:'):
                if couche_actuelle:
                    couches.append(couche_actuelle)
                    couche_actuelle = []
            couche_actuelle.append(ligne)

        if couche_actuelle:
            couches.append(couche_actuelle)

        return couches

    def obtenir_couches(self):
        return self.couches

    def obtenir_nombre_de_couches(self):
        return len(self.couches) - 1

