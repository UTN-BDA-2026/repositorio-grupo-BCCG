from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os

class Vendedor():
    def __init__(self, usuario):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),
            "vendedor.ui"
        )

        file = QFile(ruta)
        file.open(QFile.ReadOnly)

        self.ventana = loader.load(file)

        file.close()

        self.usuario = usuario

        self.ventana.lblUsuario.setText(
            f"Vendedor: {usuario.nombre}"
        )

        self.initGUI()

        self.ventana.show()

    def initGUI(self):

        self.ventana.btnVentas.clicked.connect(
            self.abrir_ventas
        )

        self.ventana.btnStock.clicked.connect(
            self.abrir_stock
        )

        self.ventana.btnSalir.clicked.connect(
            self.volver_login
        )

    def abrir_ventas(self):
        print("Abrir ventas vendedor")

    def abrir_stock(self):
        print("Abrir stock vendedor")

    def volver_login(self):
        from gui.login import Login

        self.login = Login()
        self.ventana.close()