import sys
import os

from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets, QtUiTools
from fenetre_graphique import FenetreGraphique
import resources_rc

# Ce module implémente la fenêtre d'accueil de l'application.
# Il gère :
# - le chargement de l'interface Qt Designer (.ui)
# - la sélection et la gestion d'une liste de fichiers CSV
# - la collecte des paramètres utilisateur et l'appel à la fenêtre de génération de graphique

def ressource_path(relative_path):
    """Retourne le chemin absolu d'une ressource.

    Explication : lorsque l'application est empaquetée avec PyInstaller,
    les ressources sont extraites dans un répertoire temporaire accessible
    via `sys._MEIPASS`. Cette fonction unifie l'accès aux fichiers
    (fichiers .ui, images, etc.) pour le développement et l'exécutable.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class FenetreAccueil(QtWidgets.QMainWindow):
    def __init__ (self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        # Charge l'interface Qt Designer depuis le fichier .ui.
        # Utilise `ressource_path` pour être compatible avec PyInstaller.
        ui_path = ressource_path("accueil.ui")
        self.ui = loader.load(ui_path)

        # Ajustements visuels (logo, alignements) après chargement de l'UI.
        self._ajuster_logo_entreprise()

        # État métier : liste des chemins vers les fichiers CSV sélectionnés.
        # Cette liste est la source de vérité pour la génération du graphique.
        self.liste_chemins = []

        # Connexions (signaux -> slots) : actions utilisateurs.
        self.ui.btnAjoutFichier.clicked.connect(self.ajouter_fichier)
        self.ui.btnCreer.clicked.connect(self.creer_graphique)
        self.ui.btnQuitter.clicked.connect(self.ui.close)

    def show(self):
        self.ui.show()

    def _ajuster_logo_entreprise(self):
        # Ajuste le `QLabel` contenant le logo pour conserver le ratio
        # et appliquer un rendu lissé. Si le widget n'existe pas
        # dans l'UI ou si la ressource est introuvable, on quitte silencieusement.
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
        # Ouvre un dialogue pour sélectionner plusieurs fichiers CSV.
        # Le filtre limite la sélection aux fichiers .csv.
        fichiers, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Sélectionner des fichiers", "", "Fichiers CSV (*.csv)")
        for chemin in fichiers:
            # Évite les doublons : un même chemin ne doit pas être ajouté deux fois.
            if chemin in self.liste_chemins:
                continue

            # Mise à jour de l'état et de l'UI : on crée un item personnalisé
            # (nom du fichier + bouton Supprimer) pour la liste visible.
            self.liste_chemins.append(chemin)
            item = QtWidgets.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, chemin)
            self.ui.listFichiers.addItem(item)
            self._creer_ligne_fichier(item, chemin)

    def _creer_ligne_fichier(self, item, chemin):
        # Construit dynamiquement le widget affiché dans la QListWidget.
        # Avantage : permet d'avoir un label + bouton par ligne.
        ligne_widget = QtWidgets.QWidget()
        ligne_layout = QtWidgets.QHBoxLayout(ligne_widget)
        ligne_layout.setContentsMargins(4, 2, 4, 2)

        label = QtWidgets.QLabel(Path(chemin).name)
        label.setToolTip(chemin)  # info complète au survol
        bouton = QtWidgets.QPushButton("Supprimer")
        bouton.setMaximumWidth(110)
        # Le lambda capture `item` et `chemin` pour pouvoir identifier
        # la ligne à supprimer lors du clic.
        bouton.clicked.connect(lambda _=False, i=item, c=chemin: self.supprimer_fichier(i, c))

        ligne_layout.addWidget(label)
        ligne_layout.addStretch()
        ligne_layout.addWidget(bouton)

        item.setSizeHint(ligne_widget.sizeHint())
        self.ui.listFichiers.setItemWidget(item, ligne_widget)

    def supprimer_fichier(self, item, chemin):
        # Supprime une entrée choisie : retire le chemin de la liste
        # métier, puis supprime la ligne correspondante dans la QListWidget.
        if chemin in self.liste_chemins:
            self.liste_chemins.remove(chemin)

        ligne = self.ui.listFichiers.row(item)
        if ligne >= 0:
            self.ui.listFichiers.takeItem(ligne)

    def creer_graphique(self):
        # Vérification minimale : il faut au moins un fichier pour tracer.
        if not self.liste_chemins:
            QtWidgets.QMessageBox.warning(self.ui, "Aucun fichier", "Ajoutez au moins un fichier CSV avant de créer le graphique.")
            return

        # Crée la fenêtre de graphique (dialog modal) et lui passe
        # l'ensemble des paramètres saisis par l'utilisateur.
        dialog = FenetreGraphique(self.ui)

        # On regroupe ici tous les paramètres nécessaires à la génération
        # du graphique dans un dictionnaire. La clé `fichiers` contient
        # la liste des chemins; les autres valeurs viennent des widgets UI.
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

        # Appel de la logique de génération puis affichage modal.
        dialog.generer_graphique(parametres)
        dialog.exec()