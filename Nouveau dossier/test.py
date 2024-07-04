import os
from lire_codeg import LecteurCodeG


def verifier_division(chemin_fichier, nombre_phases, phases):
    lecteur_code_g = LecteurCodeG(chemin_fichier)
    couches = lecteur_code_g.obtenir_couches()

    for i, (debut, fin) in enumerate(phases):
        print(f"Phase {i + 1}: Couches {debut} à {fin}")
        for j in range(debut - 1, fin):
            print(couches[j][:5])  # Afficher les 5 premières lignes de chaque couche pour vérifier


chemin_fichier = input("Entrez le chemin du fichier G-code : ")
nombre_phases = int(input("Entrez le nombre de phases : "))
phases = []
for i in range(nombre_phases):
    couche_debut = int(input(f"Entrez la couche initiale de la phase {i + 1} : "))
    couche_fin = int(input(f"Entrez la couche finale de la phase {i + 1} : "))
    phases.append((couche_debut, couche_fin))

verifier_division(chemin_fichier, nombre_phases, phases)
