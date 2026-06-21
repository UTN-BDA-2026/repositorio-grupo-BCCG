from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from gui.ventas_admin import Ventas
from gui.usuarios_admin import Usuarios

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
        self.ventana.hide()

        self.usuarios = Usuarios(
            volver_callback = self.mostrar_admin
        )

    def abrir_productos(self):
        print("Abrir control de inventario")
        from gui.inventario import InventarioAdmin
        
        # Creamos la instancia del controlador
        self.controlador_inventario = InventarioAdmin(
            self.usuario, 
            volver_callback=self.mostrar_admin, 
            db=None
        )
        
        # Ocultamos el admin y mostramos la ventana real del inventario
        self.ventana.hide()
        self.controlador_inventario.ventana.show()
        
    def abrir_stock(self):
        print("Abrir carga de stock")
        from gui.gestion_stock import StockAdmin 
        
        #conexion de base de datos asociada al usuario o sistema
        base_datos = getattr(self.usuario, 'db', None)
        
        self.ventana_stock = StockAdmin(self.usuario, volver_callback=self.mostrar_admin, db=base_datos)
        self.ventana.hide()