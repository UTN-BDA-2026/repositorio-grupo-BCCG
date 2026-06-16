from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QFile
from data.usuario_data import UsuarioData
from gui.admin import Admin
from gui.vendedor import Vendedor

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

        if usuario == "" or clave == "":
            self.login.lblError.setText(
                "Complete todos los campos"
            )
            return

        user = self.usuario_data.login(
            usuario,
            clave
        )

        if user:

            self.login.lblError.setText("")

            print("Bienvenido:", user.nombre)
            print("Rol:", user.rol)

            # Administrador
            if user.rol == "admin":

                print("Acceso de administrador")

                self.admin = Admin(user)

                self.login.close()

            # Vendedor
            elif user.rol == "vendedor":

                print("Acceso de vendedor")

                self.vendedor = Vendedor(user)

                self.login.close()

            else:

                self.login.lblError.setText(
                    "Rol no válido"
                )

        else:

            self.login.lblError.setText(
                "Usuario o contraseña incorrecto"
            )

    def initGUI(self):

        self.login.btnAcceder.clicked.connect(
            self.ingresar
        )