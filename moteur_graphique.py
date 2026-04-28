import matplotlib
# Force le backend Qt pour intégrer matplotlib dans l'interface PySide6.
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MoteurGraphique(FigureCanvas):
    def __init__(self, parent=None, width=14, height=7, dpi=100):
        # Crée la figure principale avec une taille adaptée à la fenêtre de l'application.
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        # Crée un axe unique (1 ligne, 1 colonne, position 1) pour tracer les courbes.
        self.ax = self.fig.add_subplot(111)
        
        # Initialise le canvas Qt à partir de la figure matplotlib.
        super().__init__(self.fig)