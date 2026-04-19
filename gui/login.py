from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QFile 

class Login():
    def __init__(self):
        loader = QUiLoader()
        self.login = loader.load("gui/login.ui")
        self.initGUI()
        self.login.lblError.setText("")#muestra la interfaz grafica
        self.login.show()
        
    def ingresar(self):
        usuario = self.login.txtUsuario.text()
        contraseña = self.login.txtClave.text()

        if usuario == "admin" and contraseña == "1234":
            self.login.lblError.setText("")
            print("Acceso concedido")
            #aca desp abrimos la ventana de inventario
        else: 
            self.login.lblError.setText("Acceso denegado")
    
    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)

