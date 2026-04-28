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
2.  Allez dans l'onglet **Releases** de ce dépôt.
3.  Téléchargez le fichier `Source code (zip)`.
4.  Extrayez l'archive qui contient tous les fichiers de code de l'application.
4.  Lancez l'application (dans un terinal) :
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

## Modifications éventuelles

### Mise à jour du logo de l'application

Si l'entreprise change de logo, voici la procédure à suivre pour mettre à jour l'application :

1. Remplacer l'image source
   * Remplacez le fichier de l'image à la racine du projet par le nouveau logo (conservez de préférence le format **PNG** avec fond transparent).
   * Si vous changez le nom du fichier, n'oubliez pas de mettre à jour le lien dans le fichier `resources.qrc`.

2. Recompiler les ressources Qt
   * L'application utilise un fichier de ressources compilé pour intégrer le logo directement dans le code. Pour appliquer le changement, lancez la commande suivante dans votre terminal :
   ```bash
   pyside6-rcc resources.qrc -o resources_rc.py
   ```

3. Mettre à jour l'icône de l'exécutable (.ico)
   Pour que l'icône du fichier .exe change également dans l'explorateur Windows :
      * Convertissez votre nouveau logo au format .ico (taille recommandée : 256x256 pixels) en utilisant le fichier `convert_ico.py` en remplaçant le nom du fichier d'origine par le nom du nouveau fichier (s'il a changé)
      * Remplacez le fichier `logo.ico` existant par le nouveau.

4. Re-générer l'exécutable
   Enfin, supprimez les dossiers build/ et dist/ et relancez la compilation avec PyInstaller pour inclure les nouvelles ressources (depuis la racine du dossier contenant tous les fichiers de code) :
   ```bash
   python -m PyInstaller --noconsole --onedir --name "MiseEnFormeGraphiquePowerTester" --icon="logo.ico" --add-data "graphique.ui;." --add-data "accueil.ui;." --collect-submodules pandas main.py
   ```


### Modification des types de fichiers supportés

Si vous souhaitez autoriser l'importation d'autres formats (comme .txt ou .dat), suivez ces étapes :

1. Modifier le filtre de sélection
Dans le fichier `fenetre_accueil.py`, dans la méthode ajouter_fichier, modifiez la chaîne de caractères du filtre dans getOpenFileNames :
```
# Pour ajouter les fichiers .txt par exemple :
fichiers, _ = QtWidgets.QFileDialog.getOpenFileNames(
    self, 
    "Sélectionner des fichiers", 
    "", 
    "Fichiers de données (*.csv *.txt)" # Ajoutez l'extension ici
)
```

2. Adapter la lecture des données
Dans le fichier `fenetre_graphique.py`, la méthode _lire_donnees utilise actuellement un séparateur par tabulation (\t). Si vos nouveaux fichiers utilisent un séparateur différent (comme une virgule ou un point-virgule), vous devrez ajuster ce paramètre :
```
# Dans fenetre_graphique.py
donnees_propre = pd.read_csv(chemin_fichier, sep='\t', header=None).dropna() 
# Changez sep='\t' par sep=',' ou sep=';' selon vos besoins.
```

3. Re-générer l'exécutable
Comme pour tout changement de code, n'oubliez pas de supprimer les dossiers build/ et dist/ et de relancer la commande de compilation PyInstaller pour que les modifications soient prises en compte.


---
<p align="center">
  <img src="LOGO-DEEP-CONCEPT%20fc.png" alt="Logo DEEP Concept" width="200"/>
  <br>
  <i>Cette application a été développée au cours d'un stage au sein de l'entreprise <a href="https://deepconcept.fr/" target="_blank"><b>DEEP Concept</b></a>.</i>
</p>
