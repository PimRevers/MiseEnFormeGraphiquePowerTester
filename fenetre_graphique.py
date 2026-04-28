import sys
import os

from pathlib import Path

import pandas as pd
from PySide6 import QtWidgets, QtUiTools
from matplotlib.ticker import MultipleLocator
from moteur_graphique import MoteurGraphique

def ressource_path(relative_path):
    """Retourne le chemin absolu d'une ressource.

    Comme dans `fenetre_accueil.py`, cette fonction gère le cas
    PyInstaller où les ressources sont extraites dans `sys._MEIPASS`.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class FenetreGraphique(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        loader = QtUiTools.QUiLoader()
        # Charge l'interface du dialogue de graphique depuis le fichier .ui.
        ui_path = ressource_path("graphique.ui")
        self.ui = loader.load(ui_path)
        self.ui.resize(1400, 800)
        self.ui.setMinimumSize(1400, 800)

        # Intègre le canvas matplotlib dans le conteneur dédié de l'UI.
        self.canvas = MoteurGraphique(self.ui)
        layout = self.ui.widGraphique.layout()
        if layout is None:
            layout = QtWidgets.QVBoxLayout(self.ui.widGraphique)
            layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.ui.btnAnnuler.clicked.connect(self.ui.reject)
        self.ui.btnEnregistrer.clicked.connect(self.sauvegarder)

        # Remarque : `MoteurGraphique` encapsule l'objet Figure/Axes
        # de Matplotlib et expose `fig`, `ax` et `draw()` utilisés ci-dessous.

    def exec(self):
        return self.ui.exec()

    def show(self):
        self.ui.show()

    def _lire_donnees(self, chemin_fichier):
        try:
            # Lit le fichier en supposant un séparateur tabulation (`\t`) et sans en-tête.
            # `dropna()` élimine les lignes entièrement vides éventuelles.
            donnees_propre = pd.read_csv(chemin_fichier, sep='\t', header=None).dropna()
        except Exception:
            return None

        # Vérifie que le fichier contient exactement 2 colonnes de données numériques
        if donnees_propre.shape[1] != 2:
            return None

        # Convertit les données en numériques et supprime les lignes non valides
        # `pd.to_numeric` convertit en float/int; les valeurs non convertibles
        # deviendront NaN et seront ensuite supprimées par `dropna()`.
        x = pd.to_numeric(donnees_propre.iloc[:, 0])
        y = pd.to_numeric(donnees_propre.iloc[:, 1])
        donnees = pd.DataFrame({"x": x, "y": y}).dropna()
        if donnees.empty:
            return None

        return donnees

    def _tracer_fichier(self, chemin_fichier):
        # Lit et trace une série depuis un fichier.
        # Si `_lire_donnees` retourne None, le fichier est ignoré (format invalide).
        donnees = self._lire_donnees(chemin_fichier)
        if donnees is None:
            return

        label = Path(chemin_fichier).name
        # `alpha` et `linewidth` définissent l'esthétique; `label` est utilisé
        # pour la légende affichée plus tard.
        self.canvas.ax.plot(donnees["x"], donnees["y"], linewidth=0.8, alpha=0.5, label=label)

    def _appliquer_parametres(self, parametres):
        # Applique les libellés et limites d'axes uniquement si les valeurs sont cohérentes.
        # Les contrôles empêchent d'inverser accidentellement les bornes ou
        # d'appliquer des intervalles nuls.
        if parametres.get("titre"):
            self.canvas.ax.set_title(parametres["titre"])

        if parametres.get("x_nom"):
            self.canvas.ax.set_xlabel(parametres["x_nom"])

        if parametres.get("y_nom"):
            self.canvas.ax.set_ylabel(parametres["y_nom"])

        x_min = parametres.get("x_min")
        x_max = parametres.get("x_max")
        if x_min is not None and x_max is not None and x_min < x_max:
            self.canvas.ax.set_xlim(x_min, x_max)

        y_min = parametres.get("y_min")
        y_max = parametres.get("y_max")
        if y_min is not None and y_max is not None and y_min < y_max:
            self.canvas.ax.set_ylim(y_min, y_max)

        # Les intervalles déterminent les pas de la grille/labels principaux.
        x_interval = parametres.get("x_intervalle", 0)
        if x_interval:
            self.canvas.ax.xaxis.set_major_locator(MultipleLocator(x_interval))

        y_interval = parametres.get("y_intervalle", 0)
        if y_interval:
            self.canvas.ax.yaxis.set_major_locator(MultipleLocator(y_interval))

    def generer_graphique(self, parametres):
        # Réinitialise l'axe avant de tracer les nouvelles séries pour
        # éviter la superposition indésirable lors d'appels répétés.
        self.canvas.ax.clear()

        # Trace chaque fichier fourni dans la liste `fichiers`.
        for chemin_fichier in parametres.get("fichiers", []):
            self._tracer_fichier(chemin_fichier)

        # Applique titres, labels, limites et pas d'axes.
        self._appliquer_parametres(parametres)

        # Grille discrète pour aider la lecture; légende uniquement si des données ont été tracées.
        self.canvas.ax.grid(True, linestyle=':', alpha=0.5)
        if self.canvas.ax.has_data():
            self.canvas.ax.legend(loc="best")

        # Optimise les marges et redessine le canvas.
        self.canvas.fig.tight_layout()
        self.canvas.draw()

    def sauvegarder(self):
        # Propose plusieurs formats d'export via la boîte de dialogue native.
        chemin_fichier, filtre = QtWidgets.QFileDialog.getSaveFileName(
            self.ui,
            "Enregistrer le graphique",
            "graphique.png",
            "Images PNG (*.png);;Images JPEG (*.jpg *.jpeg);;Images SVG (*.svg);;PDF (*.pdf)"
        )

        if not chemin_fichier:
            return

        # Si l'utilisateur n'a pas saisi d'extension, on l'ajoute
        # automatiquement selon le filtre sélectionné pour éviter
        # d'enregistrer sans suffixe.
        extension = Path(chemin_fichier).suffix.lower()
        if not extension:
            if "png" in filtre.lower():
                chemin_fichier += ".png"
            elif "jpeg" in filtre.lower() or "jpg" in filtre.lower():
                chemin_fichier += ".jpg"
            elif "svg" in filtre.lower():
                chemin_fichier += ".svg"
            elif "pdf" in filtre.lower():
                chemin_fichier += ".pdf"

        # Sauvegarde de la figure Matplotlib en haute résolution.
        self.canvas.fig.savefig(chemin_fichier, bbox_inches="tight", dpi=300)