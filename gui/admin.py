from PySide6.QtUiTools import QUiLoader
import os

class Admin():
    def __init__(self, usuario):
        loader = QUiLoader()

        # cargar archivo admin.ui
        ruta = os.path.join(os.path.dirname(__file__), "admin.ui")
        self.ventana = loader.load(ruta)
        self.usuario = usuario
        try:
            self.ventana.lblUsuario.setText(f"Admin: {usuario.nombre}")
        except:
            pass

        # inici interfaz
        self.initGUI()
        self.ventana.show()

    def initGUI(self):

        # boton volver
        try:
            self.ventana.btnVolver.clicked.connect(self.volver_login)
        except:
            pass
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
            self.ventana.btnVentas.clicked.connect(self.abrir_ventas)
        except:
            pass
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

    def abrir_ventas(self):
        print("Abrir reportes de ventas")