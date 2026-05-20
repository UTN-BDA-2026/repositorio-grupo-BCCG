from PySide6.QtUiTools import QUiLoader
import os

class StockBajo():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),

            "bajo_stock.ui"
        )

        self.ventana = loader.load(ruta)

        self.usuario = usuario

        self.initGUI()

        self.ventana.show()

    def initGUI(self):

        self.ventana.btnVolver.clicked.connect(
            self.volver
        )

    def volver(self):

        from gui.ventas_admin import Ventas

        self.ventas = Ventas(self.usuario)

        self.ventana.close()
