import sys
import os

from pathlib import Path

import pandas as pd
from PySide6 import QtWidgets, QtUiTools
from matplotlib.ticker import MultipleLocator
from moteur_graphique import MoteurGraphique

def ressource_path(relative_path):
    """ Gestion des chemins pour PyInstaller """
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

    def exec(self):
        return self.ui.exec()

    def show(self):
        self.ui.show()

    def _lire_donnees(self, chemin_fichier):
        try:
            # Lit le fichier et supprime les lignes vides.
            donnees_propre = pd.read_csv(chemin_fichier, sep='\t', header=None).dropna()
        except Exception:
            return None

        # Vérifie que le fichier contient exactement 2 colonnes de données numériques
        if donnees_propre.shape[1] != 2:
            return None

        # Convertit les données en numériques et supprime les lignes non valides
        x = pd.to_numeric(donnees_propre.iloc[:, 0])
        y = pd.to_numeric(donnees_propre.iloc[:, 1])
        donnees = pd.DataFrame({"x": x, "y": y}).dropna()
        if donnees.empty:
            return None

        return donnees

    def _tracer_fichier(self, chemin_fichier):
        # Ignore les fichiers invalides pour ne pas bloquer tout le tracé.
        donnees = self._lire_donnees(chemin_fichier)
        if donnees is None:
            return

        label = Path(chemin_fichier).name
        self.canvas.ax.plot(donnees["x"], donnees["y"], linewidth=0.8, alpha=0.5, label=label)

    def _appliquer_parametres(self, parametres):
        # Applique les libellés et limites d'axes uniquement si les valeurs sont cohérentes.
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

        x_interval = parametres.get("x_intervalle", 0)
        if x_interval:
            self.canvas.ax.xaxis.set_major_locator(MultipleLocator(x_interval))

        y_interval = parametres.get("y_intervalle", 0)
        if y_interval:
            self.canvas.ax.yaxis.set_major_locator(MultipleLocator(y_interval))

    def generer_graphique(self, parametres):
        # Réinitialise l'axe avant de tracer les nouvelles séries.
        self.canvas.ax.clear()

        for chemin_fichier in parametres.get("fichiers", []):
            self._tracer_fichier(chemin_fichier)

        self._appliquer_parametres(parametres)
        self.canvas.ax.grid(True, linestyle=':', alpha=0.5)     # Affiche une grille légère pour faciliter la lecture des valeurs
        if self.canvas.ax.has_data():
            self.canvas.ax.legend(loc="best")       # Affiche la légende si au moins une courbe a été tracée

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

        extension = Path(chemin_fichier).suffix.lower()
        if not extension:
            # Ajoute automatiquement l'extension en fonction du filtre choisi lors de l'enregistrement.
            if "png" in filtre.lower():
                chemin_fichier += ".png"
            elif "jpeg" in filtre.lower() or "jpg" in filtre.lower():
                chemin_fichier += ".jpg"
            elif "svg" in filtre.lower():
                chemin_fichier += ".svg"
            elif "pdf" in filtre.lower():
                chemin_fichier += ".pdf"

        # Sauvegarde de l'image.
        self.canvas.fig.savefig(chemin_fichier, bbox_inches="tight", dpi=300)