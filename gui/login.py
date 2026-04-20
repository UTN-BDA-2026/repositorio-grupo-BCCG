from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox
from data.usuario_data import UsuarioData
from gui.principal import Principal
import os

class Login():
    def __init__(self):
        loader = QUiLoader()
        ruta = os.path.join(os.path.dirname(__file__), "login.ui")
        self.login = loader.load(ruta)

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

            if user.rol == "admin":
                print("Acceso de administrador")
            else: 
                print("Acceso de vendedor")
            
            self.abrir_sistema(user)

        else: 
            self.login.lblError.setText("Usuario o contraseña incorrecto")

    def abrir_sistema(self, user):
        self.principal = Principal(user)
        self.login.close()

    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)