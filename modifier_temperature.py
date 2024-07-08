"""Cette classe contient 2 fonctions qui permettent de gérer la modification de la température
La première fonction (modifier_temperature_constante) modifie la température de manière constante
La deuxième fonction (modifier_temperature_lineaire) modifie la température de manière linéaire

"""
class ModificateurTemperature:
    def __init__(self, couches):
        self.couches = couches

    # fonction qui permet de modifier la temperature couche par couche sur la phase choisie par
    # l'utilisateur de manière constante (même température sur chaque couche de la phase)
    def modifier_temperature_constante(self, modifs_temp, phases):
        for i, (debut, fin) in enumerate(phases):
            if i in modifs_temp:
                temp = modifs_temp[i]
                for j in range(debut - 1, fin):
                    couche = self.couches[j]
                    couche_modifiee = []
                    for ligne in couche:
                        couche_modifiee.append(ligne)
                    # les sigles M109 et M104 ne sont pas présents au début de la ligne de commande
                    # de chacune des couches donc on les ajoute avec la valeur de température choisie
                    # par l'utilisateur
                    couche_modifiee.insert(0, f'M109 S{temp} ; Attendre température extrudeur\n')
                    couche_modifiee.insert(0, f'M104 S{temp} ; Régler température extrudeur\n')
                    self.couches[j] = couche_modifiee
        return self.couches

    # fonction qui permet de modifier la temperature couche par couche sur la phase choisie par
    # l'utilisateur de manière linéaire (température différente sur sur chaque couche de la phase)
    def modifier_temperature_lineaire(self, modifs_temp, phases):
        for i, (debut, fin) in enumerate(phases):
            #création du pas de température en fonction des températures initiales et finales et
            # du nombre de couches
            if i in modifs_temp:
                temp_debut, temp_fin = modifs_temp[i]
                nombre_couches = fin - debut + 1
                pas_temp = (temp_fin - temp_debut) / (nombre_couches - 1)
                for j in range(debut - 1, fin):
                    temp_actuelle = temp_debut + (j - (debut - 1)) * pas_temp
                    couche = self.couches[j]
                    couche_modifiee = []
                    for ligne in couche:
                        couche_modifiee.append(ligne)
                    # les sigles M109 et M104 ne sont pas présents au début de la ligne de commande
                    # de chacune des couches donc on les ajoute a chaque ligne avec la température
                    #correspondant a la ligne en fonction du pas de température
                    couche_modifiee.insert(0, f'M109 S{temp_actuelle} ; Attendre température extrudeur\n')
                    couche_modifiee.insert(0, f'M104 S{temp_actuelle} ; Régler température extrudeur\n')
                    self.couches[j] = couche_modifiee
        return self.couches