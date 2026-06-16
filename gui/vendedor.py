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

        self.ventana.btnRealizarVenta.clicked.connect(
            self.abrir_realizar_venta
            )

        self.ventana.btnVentas.clicked.connect(
            self.abrir_mis_ventas
        )

        self.ventana.btnSalir.clicked.connect(
            self.volver_login
        )

    def abrir_realizar_venta(self):
        print("Realizar venta")

    def abrir_mis_ventas(self):
        print("Mostrar ventas")


    def volver_login(self):

        from gui.login import Login

        self.login = Login()

        self.ventana.close()