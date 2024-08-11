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

class ModificateurTemperature:
    def __init__(self):
        pass

    def modifier_temperature_constante(self, couches, temperature):
        couches_modifiees = []
        for couche in couches:
            couche_modifiee = []
            for ligne in couche:
                couche_modifiee.append(ligne)
            couche_modifiee.insert(0, f'M109 S{temperature} ; Attendre température extrudeur\n')
            couche_modifiee.insert(0, f'M104 S{temperature} ; Régler température extrudeur\n')
            couches_modifiees.append(couche_modifiee)
        return couches_modifiees

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

class ModificateurVitesse:
    def __init__(self):
        pass

    def modifier_vitesse_constante(self, couches, ratio_vitesse):
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

    def modifier_vitesse_lineaire(self, couches, vitesse_debut, vitesse_fin):
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

import os

def sauvegarder_gcode(phases_modifiees, chemin_sortie):
    code_final = []
    for phase in phases_modifiees:
        for couche in phase:
            code_final.extend(couche)
    with open(chemin_sortie, 'w') as fichier:
        fichier.writelines(code_final)

def main():
    chemin_fichier = input("Entrez le chemin du fichier G-code : ")
    lecteur_codeg = LecteurCodeG(chemin_fichier)
    print(f"Nombre total de couches : {lecteur_codeg.obtenir_nombre_de_couches()}")
    nombre_phases = int(input("Entrez le nombre de phases : "))
    phases = []
    for i in range(nombre_phases):
        couche_debut = int(input(f"Entrez la couche initiale de la phase {i + 1} : "))
        couche_fin = int(input(f"Entrez la couche finale de la phase {i + 1} : "))
        phases.append((couche_debut, couche_fin))

    modifs_temp = {}
    changer_temp = input("Voulez-vous changer la température de la buse pour une phase spécifique ? (oui/non) : ").strip().lower()
    if changer_temp == 'oui':
        while True:
            phase_num = int(input("Entrez le numéro de la phase où vous souhaitez changer la température : "))
            type_variation = input("Entrez le type de variation de la température (constante/linéaire) : ").strip().lower()
            if type_variation == 'constante':
                temperature = int(input("Entrez la température pour cette phase : "))
                modifs_temp[phase_num - 1] = temperature
            elif type_variation == 'linéaire':
                temp_debut = int(input("Entrez la température de la première couche de la phase : "))
                temp_fin = int(input("Entrez la température de la dernière couche de la phase : "))
                modifs_temp[phase_num - 1] = (temp_debut, temp_fin)
            continuer_changement = input("Voulez-vous changer la température pour une autre phase ? (oui/non) : ").strip().lower()
            if continuer_changement != 'oui':
                break

    modifs_vitesse = {}
    changer_vitesse = input("Voulez-vous changer la vitesse d'impression pour une phase spécifique ? (oui/non) : ").strip().lower()
    if changer_vitesse == 'oui':
        while True:
            phase_num = int(input("Entrez le numéro de la phase où vous souhaitez changer la vitesse : "))
            type_variation = input("Entrez le type de variation de la vitesse (constante/linéaire) : ").strip().lower()
            if type_variation == 'constante':
                vitesse = int(input("Entrez la vitesse en mm/s pour cette phase : "))
                vitesse_mm_min = vitesse * 60
                couche_milieu = (phases[phase_num - 1][0] + phases[phase_num - 1][1]) // 2
                ligne_vitesse_originale = next(ligne for ligne in lecteur_codeg.obtenir_couches()[couche_milieu - 1] if 'G1' in ligne and ' F' in ligne)
                vitesse_originale = int([partie[1:] for partie in ligne_vitesse_originale.split() if partie.startswith('F')][0])
                ratio_vitesse = vitesse_mm_min / vitesse_originale
                modifs_vitesse[phase_num - 1] = ratio_vitesse
            elif type_variation == 'linéaire':
                vitesse_debut = int(input("Entrez la vitesse de la première couche en mm/s de la phase : "))
                vitesse_fin = int(input("Entrez la vitesse de la dernière couche en mm/s de la phase : "))
                vitesse_debut_mm_min = vitesse_debut * 60
                vitesse_fin_mm_min = vitesse_fin * 60
                modifs_vitesse[phase_num - 1] = (vitesse_debut_mm_min, vitesse_fin_mm_min)
            continuer_changement = input("Voulez-vous changer la vitesse pour une autre phase ? (oui/non) : ").strip().lower()
            if continuer_changement != 'oui':
                break

    couches = lecteur_codeg.obtenir_couches()
    phases_modifiees = []

    for i, (debut, fin) in enumerate(phases):
        couches_phase = couches[debut-1:fin]
        if i in modifs_temp:
            modificateur_temp = ModificateurTemperature()
            if isinstance(modifs_temp[i], int):  # Température constante
                couches_phase = modificateur_temp.modifier_temperature_constante(couches_phase, modifs_temp[i])
            elif isinstance(modifs_temp[i], tuple):  # Température linéaire
                couches_phase = modificateur_temp.modifier_temperature_lineaire(couches_phase, modifs_temp[i][0], modifs_temp[i][1])

        if i in modifs_vitesse:
            modificateur_vitesse = ModificateurVitesse()
            if isinstance(modifs_vitesse[i], float):  # Vitesse constante
                couches_phase = modificateur_vitesse.modifier_vitesse_constante(couches_phase, modifs_vitesse[i])
            elif isinstance(modifs_vitesse[i], tuple):  # Vitesse linéaire
                couches_phase = modificateur_vitesse.modifier_vitesse_lineaire(couches_phase, modifs_vitesse[i][0], modifs_vitesse[i][1])

        phases_modifiees.append(couches_phase)

    # sauvegarder le nouveau fichier G-code
    nom_fichier_entree = os.path.basename(chemin_fichier)
    nom_fichier_sortie = os.path.splitext(nom_fichier_entree)[0] + "_modifie.gcode"
    chemin_fichier_sortie = os.path.join(os.path.dirname(chemin_fichier), nom_fichier_sortie)

    sauvegarder_gcode(phases_modifiees, chemin_fichier_sortie)
    print(f"Nouveau fichier G-code écrit dans {chemin_fichier_sortie}")

if __name__ == "__main__":
    main()
