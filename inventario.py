from PySide6.QtWidgets import QApplication
from gui.login import Login

class Inventario():
    def __init__(self):
        self.app = QApplication([])
        self.login = Login()
        self.app.exec() #ejecuta la app