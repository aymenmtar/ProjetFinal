class ModificateurVitesse:
    def __init__(self, couches):
        self.couches = couches

    def modifier_vitesse_constante(self, modifs_vitesse, phases):
        for i, (debut, fin) in enumerate(phases):
            if i in modifs_vitesse:
                ratio_vitesse = modifs_vitesse[i]
                for j in range(debut - 1, fin):
                    couche = self.couches[j]
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
                    self.couches[j] = couche_modifiee
        return self.couches

    def modifier_vitesse_lineaire(self, modifs_vitesse, phases):
        for i, (debut, fin) in enumerate(phases):
            if i in modifs_vitesse:
                vitesse_debut, vitesse_fin = modifs_vitesse[i]
                nombre_couches = fin - debut + 1
                pas_vitesse = (vitesse_fin - vitesse_debut) / (nombre_couches - 1)
                for j in range(debut - 1, fin):
                    vitesse_actuelle = vitesse_debut + (j - (debut - 1)) * pas_vitesse
                    couche = self.couches[j]
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
                    self.couches[j] = couche_modifiee
        return self.couches
