from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from gui.bajo_stock import StockBajo
import os

class Ventas():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),
            "ventas_admin.ui"
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

        try:
            self.ventana.btnStockBajo.clicked.connect(
                self.abrir_stock_bajo
            )
        except:
            pass

    def volver(self):

        self.ventana.close()

        if self.volver_callback:
            self.volver_callback()

    def abrir_stock_bajo(self):

        self.stock = StockBajo(
            self.usuario,
            volver_callback=self.mostrar_ventas
        )

        self.ventana.close()

    def mostrar_ventas(self):

        self.ventana.show()