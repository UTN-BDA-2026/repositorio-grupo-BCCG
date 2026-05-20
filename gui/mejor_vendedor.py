from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QHeaderView
import os

class MejorVendedor():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),
            "mejor_vendedor.ui"
        )

        file = QFile(ruta)
        file.open(QFile.ReadOnly)

        self.ventana = loader.load(file)

        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback

        self.initGUI()

        self.ventana.show()

    def initGUI(self):

        try:
            self.ventana.btnVolver.clicked.connect(
                self.volver
            )
        except:
            pass

        # hace que las 3 columnas ocupen el mismo espacio
        self.ventana.tablaMejorVendedor.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    def volver(self):

        self.ventana.close()

        if self.volver_callback:
            self.volver_callback()