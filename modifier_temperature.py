
class ModificateurTemperature:
    """Cette classe contient 2 fonctions qui permettent de gérer la modification de la température
        :param couches: liste contenant les lignes de commandes de chaque couche d'un gcode
        :type couches: list
    La première fonction (modifier_temperature_constante) modifie la température de manière constante
    La deuxième fonction (modifier_temperature_lineaire) modifie la température de manière linéaire

    """
    def __init__(self):
        pass

    # fonction qui permet de modifier la temperature couche par couche sur la phase choisie par
    # l'utilisateur de manière constante (même température sur chaque couche de la phase)
    def modifier_temperature_constante(self, couches, temperature):
        """
                   Modifier la température de manière constante.

                   :param modifs_temp: la température donnée par l'utilisateur dans le main
                   :param phases : liste contenant les commandes des couches de la phase
                   :type phases : liste
                   :return: couches : liste contenant les commandes pour chaque couche avec la température modifiée de manière constante
                   """
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
        """
            Modifier la température de manière linéaire.
            :param modifs_temp: les températures donnée par l'utilisateur dans le main
            :param phases : liste contenant les commandes des couches de la phase
            :type phases : liste
            :return: couches : liste contenant les commandes pour chaque couche avec la température modifiée de manière linéaire couches par
            couches
            """
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