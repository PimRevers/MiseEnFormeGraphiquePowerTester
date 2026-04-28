import sys
import os

from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from fenetre_graphique import FenetreGraphique
import resources_rc

def ressource_path(relative_path):
    """ Gestion des chemins pour PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class FenetreAccueil(QtWidgets.QMainWindow):
    def __init__ (self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        # Charge l'interface Qt Designer depuis le fichier .ui.
        ui_path = ressource_path("accueil.ui")
        self.ui = loader.load(ui_path)
        self._ajuster_logo_entreprise()

        self.liste_chemins = []     # Contient tous les fichiers ajoutés pour faire le graphique

        self.ui.btnAjoutFichier.clicked.connect(self.ajouter_fichier)
        self.ui.btnCreer.clicked.connect(self.creer_graphique)
        self.ui.btnQuitter.clicked.connect(self.ui.close)

    def show(self):
        self.ui.show()

    def _ajuster_logo_entreprise(self):
        # Évite la déformation du logo en conservant son ratio.
        if not hasattr(self.ui, "logoEntreprise"):
            return

        logo = self.ui.logoEntreprise
        pixmap = QtGui.QPixmap(":/images/logo_entreprise.png")
        if pixmap.isNull():
            return

        pixmap_redim = pixmap.scaled(
            logo.size(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )
        logo.setPixmap(pixmap_redim)
        logo.setAlignment(QtCore.Qt.AlignCenter)

    def ajouter_fichier(self):
        # Permet de sélectionner plusieurs CSV en une seule fois.
        fichiers, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Sélectionner des fichiers", "", "Fichiers CSV (*.csv)")
        for chemin in fichiers:
            # Évite les doublons dans la liste interne et dans la vue.
            if chemin in self.liste_chemins:
                continue

            self.liste_chemins.append(chemin)
            item = QtWidgets.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, chemin)
            self.ui.listFichiers.addItem(item)
            self._creer_ligne_fichier(item, chemin)

    def _creer_ligne_fichier(self, item, chemin):
        # Crée une ligne personnalisée : nom du fichier + bouton de suppression.
        ligne_widget = QtWidgets.QWidget()
        ligne_layout = QtWidgets.QHBoxLayout(ligne_widget)
        ligne_layout.setContentsMargins(4, 2, 4, 2)

        label = QtWidgets.QLabel(Path(chemin).name)
        label.setToolTip(chemin)
        bouton = QtWidgets.QPushButton("Supprimer")
        bouton.setMaximumWidth(110)
        bouton.clicked.connect(lambda _=False, i=item, c=chemin: self.supprimer_fichier(i, c))

        ligne_layout.addWidget(label)
        ligne_layout.addStretch()
        ligne_layout.addWidget(bouton)

        item.setSizeHint(ligne_widget.sizeHint())
        self.ui.listFichiers.setItemWidget(item, ligne_widget)

    def supprimer_fichier(self, item, chemin):
        # Supprime le fichier à la fois de l'état métier et de l'interface.
        if chemin in self.liste_chemins:
            self.liste_chemins.remove(chemin)

        ligne = self.ui.listFichiers.row(item)
        if ligne >= 0:
            self.ui.listFichiers.takeItem(ligne)

    def creer_graphique(self):
        # Vérifie qu'au moins un fichier est présent avant de lancer le traitement.
        if not self.liste_chemins:
            QtWidgets.QMessageBox.warning(self.ui, "Aucun fichier", "Ajoutez au moins un fichier CSV avant de créer le graphique.")
            return

        dialog = FenetreGraphique(self.ui)

        # Regroupe tous les réglages saisis dans la fenêtre d'accueil.
        parametres = {
            "fichiers": self.liste_chemins,
            "titre": self.ui.editTitre.text(),
            "x_nom": self.ui.textLegendeAbs.text(),
            "x_min": self.ui.spinnerMinAbs.value(),
            "x_max": self.ui.spinnerMaxAbs.value(),
            "x_intervalle": self.ui.spinnerIntervalleAbs.value(),
            "y_nom": self.ui.spinnerNomOrd.currentText(),
            "y_min": self.ui.spinnerMinOrd.value(),
            "y_max": self.ui.spinnerMaxOrd.value(),
            "y_intervalle": self.ui.spinnerIntervalleOrd.value(),
        }

        # Génère puis affiche la fenêtre graphique en mode modal (on ne peut pas interagir avec la fenêtre d'accueil sans avoir fermer celle-ci).
        dialog.generer_graphique(parametres)
        dialog.exec()