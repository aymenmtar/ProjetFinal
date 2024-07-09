"""""Bienvenue, ce code permet de modifier un fichier gcode afin de modifier la vitesse
et la température d'extrusion par phase de la pièce
"""
#importattion des différents modules
import os
from lire_codeg import LecteurCodeG
from modifier_temperature import ModificateurTemperature
from modifier_vitesse import ModificateurVitesse

# fonction pour sauvegarder le nouveau fichier gcode
def sauvegarder_gcode(phases_modifiees, chemin_sortie):
    """
    Sauvegarder un fichier gcode.
    :param couches: liste contenant les commandes modifiées (vitesse et/ou température) pour chaque couche
    :type couches : list
    :param chemin_sortie : path pour le nouveau fichier
    :type chemin_sortie : str
                """
    code_final = []
    for phase in phases_modifiees:
        for couche in phase:
            code_final.extend(couche)
    with open(chemin_sortie, 'w') as fichier:
        fichier.writelines(code_final)


def main():
    # ouverture du fichier gcode à l'aide de la classe LecteurCodeG
    chemin_fichier = input("Entrez le chemin du fichier G-code : ")
    lecteur_codeg = LecteurCodeG(chemin_fichier)
    # affichage du nombre de couches de la pièce
    print(f"Nombre total de couches : {lecteur_codeg.obtenir_nombre_de_couches()}")
    # demande à l'utilisateur du nombre de phases, des couches initiales et finales
    nombre_phases = int(input("Entrez le nombre de phases : "))
    phases = []
    for i in range(nombre_phases):
        couche_debut = int(input(f"Entrez la couche initiale de la phase {i + 1} : "))
        couche_fin = int(input(f"Entrez la couche finale de la phase {i + 1} : "))
        phases.append((couche_debut, couche_fin))

    modifs_temp = {}
    # choix de modifier la température ou non et choix de la température en °C + constante/linéaire
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
            # modifier la température d'une autre phase
            continuer_changement = input("Voulez-vous changer la température pour une autre phase ? (oui/non) : ").strip().lower()
            if continuer_changement != 'oui':
                break

    modifs_vitesse = {}
    # choix de modifier la vitesse et choix de la vitesse en mm/s (constante/linéaire)
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
            # modifier la vitesse pour une autre phase
            continuer_changement = input("Voulez-vous changer la vitesse pour une autre phase ? (oui/non) : ").strip().lower()
            if continuer_changement != 'oui':
                break

    couches = lecteur_codeg.obtenir_couches()
    phases_modifiees = []

    for i, (debut, fin) in enumerate(phases):
        couches_phase = couches[debut - 1:fin]
        if i in modifs_temp:
            modificateur_temp = ModificateurTemperature()
            if isinstance(modifs_temp[i], int):  # Température constante
                couches_phase = modificateur_temp.modifier_temperature_constante(couches_phase, modifs_temp[i])
            elif isinstance(modifs_temp[i], tuple):  # Température linéaire
                couches_phase = modificateur_temp.modifier_temperature_lineaire(couches_phase, modifs_temp[i][0],
                                                                                modifs_temp[i][1])

        if i in modifs_vitesse:
            modificateur_vitesse = ModificateurVitesse()
            if isinstance(modifs_vitesse[i], float):  # Vitesse constante
                couches_phase = modificateur_vitesse.modifier_vitesse_constante(couches_phase, modifs_vitesse[i])
            elif isinstance(modifs_vitesse[i], tuple):  # Vitesse linéaire
                couches_phase = modificateur_vitesse.modifier_vitesse_lineaire(couches_phase, modifs_vitesse[i][0],
                                                                               modifs_vitesse[i][1])

        phases_modifiees.append(couches_phase)

    # sauvegarder le nouveau fichier G-code
    nom_fichier_entree = os.path.basename(chemin_fichier)
    nom_fichier_sortie = os.path.splitext(nom_fichier_entree)[0] + "_modifie.gcode"
    chemin_fichier_sortie = os.path.join(os.path.dirname(chemin_fichier), nom_fichier_sortie)
    # le nouveau fichier est sauvegardé sous le nom initial+modifier.gcode
    sauvegarder_gcode(phases_modifiees, chemin_fichier_sortie)
    print(f"Nouveau fichier G-code écrit dans {chemin_fichier_sortie}")

if __name__ == "__main__":
    main()