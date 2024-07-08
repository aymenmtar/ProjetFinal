
class ModificateurVitesse:
    """Cette classe contient 2 fonctions qui permettent de gérer la modification de la vitesse
        :param couches: liste contenant les lignes de commandes de chaque couche d'un gcode
        :type couches: list
    La première fonction (modifier_vitesse_constante) modifie la vitesse de manière constante
    La deuxième fonction (modifier_vitesse_lineaire) modifie la vitesse de manière linéaire

    """
    def __init__(self, couches):
        self.couches = couches

# fonction qui modifie la vitesse de manière constante (même vitesse pour chaque ligne) dans la phase choisie couche par couche
    def modifier_vitesse_constante(self, modifs_vitesse, phases):
        """
           Modifier la vitesse de manière constante.

           :param modifs_vitesse: la vitesse donnée par l'utilisateur dans le main
           :param phases : liste contenant les commandes des couches de la phase
           :type phases : liste
           :return: couches : liste contenant les commandes pour chaque couche avec la vitesse modifiée de manière constante
           """
        for i, (debut, fin) in enumerate(phases):
            if i in modifs_vitesse:
                ratio_vitesse = modifs_vitesse[i]
                for j in range(debut - 1, fin):
                    couche = self.couches[j]
                    couche_modifiee = []
                    for ligne in couche:
                        # trouver les lignes contenant G1 ou F
                        if 'G1' in ligne and ' F' in ligne:
                            elements = ligne.split()
                            for k, element in enumerate(elements):
                                if element.startswith('F'):
                                    vitesse_originale = int(element[1:])
                                    nouvelle_vitesse = int(vitesse_originale * ratio_vitesse)
                                    elements[k] = f'F{nouvelle_vitesse}'
                            ligne = ' '.join(elements) + '\n'
                        couche_modifiee.append(ligne)
                    self.couches[j] = couche_modifiee
        return self.couches

# fonction qui modifie la vitesse de manière linéaire (chaque ligne a une vitesse différente) dans la phase choisie couche par couche
    def modifier_vitesse_lineaire(self, modifs_vitesse, phases):
        """
                   Modifier la vitesse de manière linéaire.

                   :param modifs_vitesse: les vitesses donnée par l'utilisateur dans le main
                   :param phases : liste contenant les commandes des couches de la phase
                   :type phases : liste
                   :return: couches : liste contenant les commandes pour chaque couche avec la vitesse modifiée de manière linéaire couches par
                   couches
                   """
        for i, (debut, fin) in enumerate(phases):
            # création du pas de vitesse en fonction des vitesses choisies par l'utilisateur et du
            #nombre de couches
            if i in modifs_vitesse:
                vitesse_debut, vitesse_fin = modifs_vitesse[i]
                nombre_couches = fin - debut + 1
                pas_vitesse = (vitesse_fin - vitesse_debut) / (nombre_couches - 1)
                for j in range(debut - 1, fin):
                    vitesse_actuelle = vitesse_debut + (j - (debut - 1)) * pas_vitesse
                    couche = self.couches[j]
                    couche_modifiee = []
                    # trouver les lignes contenant G1 et F
                    for ligne in couche:
                        if 'G1' in ligne and ' F' in ligne:
                            elements = ligne.split()
                            for k, element in enumerate(elements):
                                if element.startswith('F'):
                                    nouvelle_vitesse = int(vitesse_actuelle)
                                    elements[k] = f'F{nouvelle_vitesse}'
                            ligne = ' '.join(elements) + '\n'
                        couche_modifiee.append(ligne)
                    self.couches[j] = couche_modifiee
        return self.couches