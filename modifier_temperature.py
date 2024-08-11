
class ModificateurTemperature:
    def __init__(self):
        pass

    # fonction qui permet de modifier la temperature couche par couche sur la phase choisie par
    # l'utilisateur de manière constante (même température sur chaque couche de la phase)
    def modifier_temperature_constante(self, couches, temperature):

        couches_modifiees = []
        for couche in couches:
            couche_modifiee = []
            for ligne in couche:
                couche_modifiee.append(ligne)
                    # les sigles M109 et M104 ne sont pas présents au début de la ligne de commande
                    # de chacune des couches donc on les ajoute avec la valeur de température choisie
                    # par l'utilisateur
                couche_modifiee.insert(0, f'M109 S{temperature} ; Attendre température extrudeur\n')
                couche_modifiee.insert(0, f'M104 S{temperature} ; Régler température extrudeur\n')
                couches_modifiees.append(couche_modifiee)
            return couches_modifiees

    # fonction qui permet de modifier la temperature couche par couche sur la phase choisie par
    # l'utilisateur de manière linéaire (température différente sur sur chaque couche de la phase)
    def modifier_temperature_lineaire(self, couches, temp_debut, temp_fin):
        nombre_couches = len(couches)
        pas_temp = (temp_fin - temp_debut) / (nombre_couches - 1)
        couches_modifiees = []
        for i, couche in enumerate(couches):
            temp_actuelle = temp_debut + i * pas_temp
            couche_modifiee = []
            for ligne in couche:
                couche_modifiee.append(ligne)
            couche_modifiee.insert(0, f'M109 S{temp_actuelle} ; Attendre température extrudeur\n')
            couche_modifiee.insert(0, f'M104 S{temp_actuelle} ; Régler température extrudeur\n')
            couches_modifiees.append(couche_modifiee)
        return couches_modifiees