Bienvenue sur ce projet. Le but de ce programme est de pouvoir modifier lignes par lignes dans un Gcode la température et/ou la vitesse d'extrusion de la buse d'une imprimante 3D FDM

Ce code est structuré de la manière suivante :
- 1 main
- 3 classes gérant respectivement la lecture lignes par lignes d'un fichier Gcode, la modification de la température dans les commandes de chaque couche et la modification de la vitesse dans les commandes de chaque couche

Comment utiliser le code :
- Pour utiliser le code il est nécessaire d'importer le module Os
L'utilisateur doit fournir un fichier Gcode à modifier ainsi que son chemin.
Ensuite l'utilisateur pourra choisir si il veut modifier la température et/ou la vitesse sur une certaine phase. Il lui sera demandé le nombre de phase à modifier ainsi que les numéro des couches initiales et finales des phases.
Puis l'utilisateur devra choisir si il souhaite une température/vitesse constante ou linéaire sur la phase choisie. Il donnera ensuite la ou les valeurs de température/vitesse voulues.
Après avoir modifier une phase, l'utilisateur pourra modiifer une autre phase que ce soit pour la vitesse ou la température.
Après avoir effectué toutes les modifications voulues sur le Gcode, le programme retournera un nouveau fichier Gcode nommé "nom_du_fichier + modifie.gcode"

Les valeurs de température sont à entrer en °C et celles de vitesse en mm/s

