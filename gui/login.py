from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QFile
from data.usuario_data import UsuarioData

class Login():
    def __init__(self):
        loader = QUiLoader()
        self.login = loader.load("gui/login.ui")
        self.usuario_data = UsuarioData()  # instancia de acceso a
        self.initGUI()
        self.login.lblError.setText("")  # muestra la interfaz grafica
        self.login.show()
        
    def ingresar(self):
        usuario = self.login.txtUsuario.text()
        clave = self.login.txtClave.text()

        # validar los campos vacios
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

            # aca desp abrimos la ventana de inventario
            # self.abrir_sistema()

        else:
            self.login.lblError.setText("Usuario o contraseña incorrecto")

    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)