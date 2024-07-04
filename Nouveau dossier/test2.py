import os
from lire_codeg import LecteurCodeG
from modifier_temperature import ModificationTemperature
from modifier_vitesse import ModificationVitesse


def appliquer_modifications(chemin_fichier, nombre_phases, phases, modifications_temp, modifications_temp_type,
                            modifications_vitesse, modifications_vitesse_type):
    lecteur_code_g = LecteurCodeG(chemin_fichier)
    couches = lecteur_code_g.obtenir_couches()

    if modifications_temp:
        mod_temp = ModificationTemperature(couches)
        for phase in modifications_temp:
            if modifications_temp_type[phase] == 'lineaire':
                mod_temp.modifier_temperature_lineaire({phase: modifications_temp[phase]}, [phases[phase]])
            elif modifications_temp_type[phase] == 'constante':
                mod_temp.modifier_temperature_constante({phase: modifications_temp[phase][0]}, [phases[phase]])

    if modifications_vitesse:
        mod_vit = ModificationVitesse(couches)
        for phase in modifications_vitesse:
            if modifications_vitesse_type[phase] == 'lineaire':
                mod_vit.modifier_vitesse_lineaire({phase: modifications_vitesse[phase]}, [phases[phase]])
            elif modifications_vitesse_type[phase] == 'constante':
                mod_vit.modifier_vitesse_constante({phase: modifications_vitesse[phase][0]}, [phases[phase]])

    nom_fichier_entree = os.path.basename(chemin_fichier)
    nom_fichier_sortie = os.path.splitext(nom_fichier_entree)[0] + "_modifié.gcode"
    chemin_sortie = os.path.join(os.path.dirname(chemin_fichier), nom_fichier_sortie)

    with open(chemin_sortie, 'w') as fichier:
        for couche in couches:
            fichier.writelines(couche)

    print(f"Nouveau fichier G-code écrit dans {chemin_sortie}")


chemin_fichier = input("Entrez le chemin du fichier G-code : ")
nombre_phases = int(input("Entrez le nombre de phases : "))
phases = []
for i in range(nombre_phases):
    couche_debut = int(input(f"Entrez la couche initiale de la phase {i + 1} : "))
    couche_fin = int(input(f"Entrez la couche finale de la phase {i + 1} : "))
    phases.append((couche_debut, couche_fin))

modifications_temp = {}
modifications_temp_type = {}
changer_temp = input("Voulez-vous changer la température de la buse pour une phase spécifique ? (oui/non) : ").lower()
if changer_temp == 'oui':
    for i in range(nombre_phases):
        changer = input(f"Changer la température pour la phase {i + 1} ? (oui/non) : ").lower()
        if changer == 'oui':
            temp_debut = float(input(f"Température initiale pour la phase {i + 1} : "))
            temp_fin = float(input(f"Température finale pour la phase {i + 1} : "))
            modifications_temp[i] = (temp_debut, temp_fin)
            type_mod_temp = input(
                f"Type de modification de température pour la phase {i + 1} (lineaire/constante) : ").lower()
            modifications_temp_type[i] = type_mod_temp

modifications_vitesse = {}
modifications_vitesse_type = {}
changer_vitesse = input("Voulez-vous changer la vitesse d'impression pour une phase spécifique ? (oui/non) : ").lower()
if changer_vitesse == 'oui':
    for i in range(nombre_phases):
        changer = input(f"Changer la vitesse pour la phase {i + 1} ? (oui/non) : ").lower()
        if changer == 'oui':
            vitesse_debut = float(input(f"Vitesse initiale pour la phase {i + 1} (en mm/s) : "))
            vitesse_fin = float(input(f"Vitesse finale pour la phase {i + 1} (en mm/s) : "))
            modifications_vitesse[i] = (vitesse_debut, vitesse_fin)
            type_mod_vit = input(
                f"Type de modification de vitesse pour la phase {i + 1} (lineaire/constante) : ").lower()
            modifications_vitesse_type[i] = type_mod_vit

appliquer_modifications(chemin_fichier, nombre_phases, phases, modifications_temp, modifications_temp_type,
                        modifications_vitesse, modifications_vitesse_type)
