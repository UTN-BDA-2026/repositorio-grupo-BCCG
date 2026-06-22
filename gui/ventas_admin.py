from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from gui.mejor_vendedor import MejorVendedor
from gui.producto_mas_vendido import ProductoMasVendido
from services.reportes_service import ReportesService #importamos el servicio de reportes
import os

class Ventas():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),
            "ventas_admin.ui"
        )

        file = QFile(ruta)
        file.open(QFile.ReadOnly)

        self.ventana = loader.load(file)

        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback
        self.reportes_service = ReportesService() #instancia del servicio de reportes

        self.initGUI()
     
        self.ventana.show()

    def initGUI(self):
        try: #conectamos el boton de calcular total general
            self.ventana.btnTotalVendido.clicked.connect(
                self.calcularTotalGeneral
            )    
        except:
            pass
        
        try:
            self.ventana.btnVolver.clicked.connect(
                self.volver
                )
        except:
            pass

        try: 
            self.ventana.btnProdMasVendido.clicked.connect(
                self.abrir_productos_mas_vendidos)     
        except:
            pass

        try:
            self.ventana.btnMejorVendedor.clicked.connect(
                self.abrir_mejor_vendedor
            )
        except:
            pass

    def calcularTotalGeneral(self):
        total= self.reportes_service.total_vendido()
        self.ventana.lblTotalVendido.setText(f"${total:.2f}")
    
    def volver(self):
        self.ventana.hide()
        if self.volver_callback:
            self.volver_callback()

    def abrir_mejor_vendedor(self):
        self.mejor = MejorVendedor(
            self.usuario,
            volver_callback=self.mostrar_ventas
        )

        self.ventana.close()

    def abrir_productos_mas_vendidos(self):
        self.ventana.hide()
        self.productos_mas_vendidos = ProductoMasVendido(
            self.usuario,
            volver_callback=self.mostrar_ventas
        )

        self.ventana.close()

    def mostrar_ventas(self):
        self.ventana.show()