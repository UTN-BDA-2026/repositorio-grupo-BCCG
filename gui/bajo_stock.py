from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from services.reportes_service import ReportesService #importamos el servicio de reportes
import os

class StockBajo():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),

            "bajo_stock.ui"
        )

        self.ventana = loader.load(ruta)

        self.usuario = usuario
        self.volver_callback = volver_callback
        self.reportes_service = ReportesService() #instancia del servicio de reportes

        self.initGUI()
        self.cargarTablaBajoStock() #cargamos la tabla de productos con bajo stock al iniciar la ventana
        self.ventana.show()

    def initGUI(self):
        #boton para regresar al panel de reportes
        try:
            self.ventana.btnVolver.clicked.connect(self.volver)
        except AttributeError:
            try:
                self.ventana.btnSalir.clicked.connect(self.volver)
            except AttributeError:
                print("Verifica el objectName del botón de volver en bajo_stock.ui")
        #ajuste de las columnas para que ocupen todo el espacio disponible
        try:
            self.ventana.tablaStock.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        except AttributeError:
            print("Verifica el objectName de la QTableWidget en bajo_stock.ui")

    def cargarTablaBajoStock(self):
        try:
            #lista de consulta 
            productos = self.reportes_service.productos_bajo_stock()

            #definimos la cantidad de filas de la tabla segun los resultados
            self.ventana.tablaStock.setRowCount(len(productos))

            for fila, prod in enumerate(productos):
                # prod[0] es el nombre del producto, prod[1] es el stock actual
                self.ventana.tablaStock.setItem(fila, 0, QTableWidgetItem(str(prod[0])))
                self.ventana.tablaStock.setItem(fila, 1, QTableWidgetItem(str(prod[1])))
        except Exception as ex:
            print("Error al cargar la tabla de bajo stock:", ex)

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()