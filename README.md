# 📊 Analyseur Power Tester (v1.1)

**Analyseur Power Tester** est une application de bureau conçue pour automatiser la mise en forme et la visualisation de courbes de tests de puissance. Elle permet de transformer des données brutes en graphiques précis et personnalisés.

---

## Fonctionnalités

* **Gestion multi-fichiers** : Importez plusieurs fichiers `.csv` simultanément pour superposer et comparer vos courbes sur un seul graphique.
* **Configuration dynamique des axes** :
    * **Axe X (Abscisses)** : Réglage du nom (par défaut "Number of Cycles"), des limites (Min/Max) et de l'intervalle des graduations.
    * **Axe Y (Ordonnées)** : Choix de la grandeur physique à afficher : *DeltaT (°C)*, *PowerStep (W)*, *TjMax (°C)*, *TjMin (°C)* ou *Von (V)*.
* **Moteur graphique** : Intégration de **Matplotlib** avec grille de lecture et légende automatique.
* **Exportation** : Enregistrez vos graphiques au format **PNG, JPEG, SVG ou PDF**.

---

## Installation & Utilisation

### Pour les utilisateurs (Windows)
1.  Allez dans l'onglet **Releases** de ce dépôt.
2.  Téléchargez le fichier `MiseEnFormeGraphiquePowerTester.zip`.
3.  Extrayez l'archive et lancez l'exécutable `MiseEnFormeGraphiquePowerTester.exe`.


### Pour les développeurs
Si vous souhaitez exécuter le projet à partir des sources :
1.  Installez Python 3.12+ et les dépendances nécessaires :
    ```bash
    pip install PySide6 pandas matplotlib
    ```
2.  Lancez l'application :
    ```bash
    python main.py
    ```

---

## Technologies utilisées

* **PySide6 (Qt pour Python)** : Interface utilisateur et gestion des fenêtres.
* **Pandas** : Analyse et traitement des données CSV.
* **Matplotlib** : Création et rendu des graphiques.
* **Qt Designer** : Conception des interfaces `.ui`.

---

## Structure du projet

* `main.py` : Point d'entrée de l'application.
* `fenetre_accueil.py` : Logique de la fenêtre principale et gestion des fichiers.
* `fenetre_graphique.py` : Gestion du dialogue d'affichage et d'export du graphique.
* `moteur_graphique.py` : Composant d'intégration Matplotlib dans l'interface Qt.
* `resources_rc.py` : Ressources compilées (logo de l'entreprise).

---
<p align="center">
  <img src="LOGO-DEEP-CONCEPT%20fc.png" alt="Logo DEEP Concept" width="200"/>
  <br>
  <i>Cette application a été développée au cours d'un stage au sein de l'entreprise <a href="https://deepconcept.fr/" target="_blank"><b>DEEP Concept</b></a>.</i>
</p>
