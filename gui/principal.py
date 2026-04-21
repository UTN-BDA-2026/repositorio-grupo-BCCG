from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox
from services.inventario_service import InventarioService
import os

class Principal():
    def __init__(self, usuario):
        loader = QUiLoader()

        # 🔥 RUTA CORRECTA
        ruta = os.path.join(os.path.dirname(__file__), "principal.ui")
        self.ventana = loader.load(ruta)

        self.usuario = usuario
        self.service = InventarioService()

        self.initGUI()
        self.ventana.show()

    def initGUI(self):
        self.ventana.btnVender.clicked.connect(self.vender)

    def vender(self):
        try:
            if self.ventana.txtIdProducto.text() == "" or self.ventana.txtCantidad.text() == "":
                self.ventana.lblMensaje.setText("Complete los campos")
                return

            id_producto = int(self.ventana.txtIdProducto.text())
            cantidad = int(self.ventana.txtCantidad.text())

            self.service.vender_producto(
                self.usuario.id,
                id_producto,
                cantidad
            )

            self.ventana.lblMensaje.setText("Venta realizada correctamente")

        except Exception as ex:
            QMessageBox.critical(self.ventana, "Error", str(ex))