import sys
from PySide6.QtWidgets import QApplication
from fenetre_accueil import FenetreAccueil

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = FenetreAccueil()
    main_window.show()
    sys.exit(app.exec())