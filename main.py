import os
from lire_codeg import LecteurCodeG
from modifier_temperature import ModificateurTemperature
from modifier_vitesse import ModificateurVitesse

def sauvegarder_gcode(couches, chemin_sortie):
    code_final = []
    for couche in couches:
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

    couches_modifiees = lecteur_codeg.obtenir_couches()

    if modifs_temp:
        modificateur_temp = ModificateurTemperature(couches_modifiees)
        for i, variation_type in modifs_temp.items():
            if isinstance(variation_type, int):  # Température constante
                couches_modifiees = modificateur_temp.modifier_temperature_constante({i: variation_type}, [phases[i]])
            elif isinstance(variation_type, tuple):  # Température linéaire
                couches_modifiees = modificateur_temp.modifier_temperature_lineaire({i: variation_type}, [phases[i]])

    if modifs_vitesse:
        modificateur_vitesse = ModificateurVitesse(couches_modifiees)
        for i, variation_type in modifs_vitesse.items():
            if isinstance(variation_type, float):  # Vitesse constante
                couches_modifiees = modificateur_vitesse.modifier_vitesse_constante({i: variation_type}, [phases[i]])
            elif isinstance(variation_type, tuple):  # Vitesse linéaire
                couches_modifiees = modificateur_vitesse.modifier_vitesse_lineaire({i: variation_type}, [phases[i]])

    # sauvegarder le nouveau fichier G-code
    nom_fichier_entree = os.path.basename(chemin_fichier)
    nom_fichier_sortie = os.path.splitext(nom_fichier_entree)[0] + "_modifie.gcode"
    chemin_fichier_sortie = os.path.join(os.path.dirname(chemin_fichier), nom_fichier_sortie)

    sauvegarder_gcode(couches_modifiees, chemin_fichier_sortie)
    print(f"Nouveau fichier G-code écrit dans {chemin_fichier_sortie}")

if __name__ == "__main__":
    main()