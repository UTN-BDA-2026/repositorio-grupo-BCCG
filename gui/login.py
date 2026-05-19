from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QFile
from data.usuario_data import UsuarioData
from gui.admin import Admin

class Login():
    def __init__(self):
        loader = QUiLoader()
        self.login = loader.load("gui/login.ui")

        self.usuario_data = UsuarioData()

        self.initGUI()

        self.login.lblError.setText("")

        self.login.show()
        
    def ingresar(self):

        usuario = self.login.txtUsuario.text()
        clave = self.login.txtClave.text()

        if usuario == "" and clave == "":
            self.login.lblError.setText("Complete todos los campos")
            return
        user = self.usuario_data.login(usuario, clave)

        if user:
            self.login.lblError.setText("")
            print("Bienvenido:", user.nombre)
            print("Rol:", user.rol)
            # acceso administrador
            if user.rol == "admin":
                print("Acceso de administrador")
                self.admin = Admin(user)
                self.login.close()
            # acceso vendedor
            else:
                print("Acceso de vendedor")
        else:
            self.login.lblError.setText(
                "Usuario o contraseña incorrecto"
            )
    def initGUI(self):
        self.login.btnAcceder.clicked.connect(
            self.ingresar
        )