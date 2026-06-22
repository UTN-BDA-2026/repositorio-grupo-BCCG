from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from gui.ventas_admin import Ventas
from gui.usuarios_admin import Usuarios
from gui.menu_inventario import MenuInventario

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
            self.ventana.btnMenuInventario.clicked.connect(self.abrir_menu_inventario)
        except:
            pass
        try:
            self.ventana.btnReporte.clicked.connect(self.abrir_ventas_admin)
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
        self.ventana.hide()

        self.usuarios = Usuarios(
            volver_callback = self.mostrar_admin
        )

    def abrir_menu_inventario(self):
        print("Abrir menu intermedio de inventario")
        self.ventana.hide()
        
        # Creamos la instancia del controlador
        self.menu_inventario = MenuInventario(
            usuario=self.usuario, 
            volver_callback=self.mostrar_admin, 
            db=None
        )
        
        # Ocultamos el admin y mostramos la ventana real del inventario
        self.ventana.hide()
        self.menu_inventario.ventana.show()
        