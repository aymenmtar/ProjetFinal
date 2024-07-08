"""Cette classe contient 4 fonctions qui permettent la lecture du fichier gcode donné par
l'ulisateur
La première fonction (_lire_codeg) permet de lire un fichier gcode lignes par lignes
La deuxième fonction (_diviser_en_couche) permet de diviser le fichier lu en une liste contenant
des listes contenant elle même une str des commandes de chaque couche
La troisième fonction (obtenir_couche) retourne les couches
La quatrième fonction (obtenir_nombre_de_couche) retourne le nombre de couche du fichier gcode

"""
class LecteurCodeG:
    def __init__(self, chemin_fichier):
        self.chemin_fichier = chemin_fichier
        self.couches = self._lire_codeg()

    #fonction qui permet de lire le gcode lignes par lignes
    def _lire_codeg(self):
        with open(self.chemin_fichier, 'r') as fichier:
            lignes = fichier.readlines()
        return self._diviser_en_couches(lignes)

    #fonction qui divise le fichier gcode lu couches par couches à l'aide du sigle "LAYER" présent
    #au début de chaque couche
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

    #fonction pour obtenir les couhes
    def obtenir_couches(self):
        return self.couches

    #fonction qui compte le nombre de couches totales
    def obtenir_nombre_de_couches(self):
        return len(self.couches) - 1
