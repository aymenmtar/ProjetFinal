class ModificateurTemperature:
    def __init__(self, couches):
        self.couches = couches

    def modifier_temperature_constante(self, modifs_temp, phases):
        for i, (debut, fin) in enumerate(phases):
            if i in modifs_temp:
                temp = modifs_temp[i]
                for j in range(debut - 1, fin):
                    couche = self.couches[j]
                    couche_modifiee = []
                    for ligne in couche:
                        couche_modifiee.append(ligne)
                    couche_modifiee.insert(0, f'M109 S{temp} ; Attendre température extrudeur\n')
                    couche_modifiee.insert(0, f'M104 S{temp} ; Régler température extrudeur\n')
                    self.couches[j] = couche_modifiee
        return self.couches

    def modifier_temperature_lineaire(self, modifs_temp, phases):
        for i, (debut, fin) in enumerate(phases):
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
                    couche_modifiee.insert(0, f'M109 S{temp_actuelle} ; Attendre température extrudeur\n')
                    couche_modifiee.insert(0, f'M104 S{temp_actuelle} ; Régler température extrudeur\n')
                    self.couches[j] = couche_modifiee
        return self.couches
