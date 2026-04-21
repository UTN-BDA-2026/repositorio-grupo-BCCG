from PySide6.QtUiTools import QUiLoader
import os

class Admin():
    def __init__(self, usuario):
        loader = QUiLoader()
        ruta = os.path.join(os.path.dirname(__file__), "admin.ui")
        self.ventana = loader.load(ruta)

        self.usuario = usuario
        try:
            self.ventana.lblUsuario.setText(f"Admin: {usuario.nombre}")
        except:
            pass

        self.ventana.show()
        
        #luego definiremos las acciones de los botones y demas componentes de la interfaz grafica del admin