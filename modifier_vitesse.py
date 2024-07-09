
class ModificateurVitesse:
    """Cette classe contient 2 fonctions qui permettent de gérer la modification de la vitesse
        :param couches: liste contenant les lignes de commandes de chaque couche d'un gcode
        :type couches: list
    La première fonction (modifier_vitesse_constante) modifie la vitesse de manière constante
    La deuxième fonction (modifier_vitesse_lineaire) modifie la vitesse de manière linéaire

    """
    def __init__(self):
        pass

# fonction qui modifie la vitesse de manière constante (même vitesse pour chaque ligne) dans la phase choisie couche par couche
    def modifier_vitesse_constante(self, couches, ratio_vitesse):
        """
           Modifier la vitesse de manière constante.

        """
        couches_modifiees = []
        for couche in couches:
            couche_modifiee = []
            for ligne in couche:
                if 'G1' in ligne and ' F' in ligne:
                    elements = ligne.split()
                    for k, element in enumerate(elements):
                        if element.startswith('F'):
                            vitesse_originale = int(element[1:])
                            nouvelle_vitesse = int(vitesse_originale * ratio_vitesse)
                            elements[k] = f'F{nouvelle_vitesse}'
                    ligne = ' '.join(elements) + '\n'
                couche_modifiee.append(ligne)
            couches_modifiees.append(couche_modifiee)
        return couches_modifiees

# fonction qui modifie la vitesse de manière linéaire (chaque ligne a une vitesse différente) dans la phase choisie couche par couche
    def modifier_vitesse_lineaire(self, couches, vitesse_debut, vitesse_fin):
        """
                   Modifier la vitesse de manière linéaire.

                   :param modifs_vitesse: les vitesses donnée par l'utilisateur dans le main
                   :param phases : liste contenant les commandes des couches de la phase
                   :type phases : liste
                   :return: couches : liste contenant les commandes pour chaque couche avec la vitesse modifiée de manière linéaire couches par
                   couches
                   """
        nombre_couches = len(couches)
        pas_vitesse = (vitesse_fin - vitesse_debut) / (nombre_couches - 1)
        couches_modifiees = []
        for i, couche in enumerate(couches):
            vitesse_actuelle = vitesse_debut + i * pas_vitesse
            couche_modifiee = []
            for ligne in couche:
                if 'G1' in ligne and ' F' in ligne:
                    elements = ligne.split()
                    for k, element in enumerate(elements):
                        if element.startswith('F'):
                            nouvelle_vitesse = int(vitesse_actuelle)
                            elements[k] = f'F{nouvelle_vitesse}'
                    ligne = ' '.join(elements) + '\n'
                couche_modifiee.append(ligne)
            couches_modifiees.append(couche_modifiee)
        return couches_modifiees