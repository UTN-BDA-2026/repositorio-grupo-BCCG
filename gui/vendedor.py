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
        from gui.realizar_venta import RealizarVenta
        self.ventana.hide()
        self.pestana_ventas = RealizarVenta(volver_callback=self.mostrar_vendedor)
        
        print("Realizar venta")

    def mostrar_vendedor(self):
        self.ventana.show()


    def abrir_mis_ventas(self):
        from gui.mis_ventas import MisVentas
        self.ventana.hide()
        self.mis_ventas = MisVentas(self.usuario, volver_callback=self.mostrar_vendedor)
        print("Mostrar ventas")


    def volver_login(self):

        from gui.login import Login

        self.login = Login()

        self.ventana.close()