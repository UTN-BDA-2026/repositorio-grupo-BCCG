from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from gui.ventas_admin import Ventas
import os

class Admin():
    def __init__(self, usuario):
        loader = QUiLoader()
        # cargar archivo admin.ui
        ruta = os.path.join(os.path.dirname(__file__), "admin.ui")
        file = QFile(ruta)
        file.open(QFile.ReadOnly)
        self.ventana = loader.load(file)
        file.close()

        self.usuario = usuario
        try:
            self.ventana.lblUsuario.setText(f"Admin: {usuario.nombre}")
        except:
            pass
        # inici interfaz
        self.initGUI()
        self.ventana.show()

    def initGUI(self):
        # botones del administrador
        try:
            self.ventana.btnUsuarios.clicked.connect(self.abrir_usuarios)
        except:
            pass
        try:
            self.ventana.btnProductos.clicked.connect(self.abrir_productos)
        except:
            pass
        try:
            self.ventana.btnStock.clicked.connect(self.abrir_stock)
        except:
            pass
        try:
            self.ventana.btnVentas.clicked.connect(self.abrir_ventas_admin)
        except:
            pass
        try:
            self.ventana.btnVolver.clicked.connect(self.volver_login)
        except:
            pass

    def abrir_ventas_admin(self):
        self.ventana.hide()  # en vez de cerrar (mejor experiencia usuario)

        self.ventas = Ventas(
            self.usuario,
            volver_callback=self.mostrar_admin
        )

    def mostrar_admin(self):
        self.ventana.show()

    # volver al login
    def volver_login(self):
        from gui.login import Login

        self.login = Login()
        self.ventana.close()

    def abrir_usuarios(self):
        print("Abrir gestión de usuarios")

    def abrir_productos(self):
        print("Abrir gestión de productos")

    def abrir_stock(self):
        print("Abrir carga de stock")