from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QHeaderView, QTableWidgetItem
from services.reportes_service import ReportesService #importamos el servicio de reportes
import os

class MejorVendedor():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),
            "mejor_vendedor.ui"
        )

        file = QFile(ruta)
        file.open(QFile.ReadOnly)

        self.ventana = loader.load(file)

        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback
        self.reportes_service = ReportesService() #instancia del servicio de reportes

        self.initGUI()
        self.cargarMejorVendedor() #cargamos el mejor vendedor al iniciar la ventana
        self.ventana.show()

    def initGUI(self):

        try:
            self.ventana.btnVolver.clicked.connect(self.volver)
        except AttributeError:
            try:
                self.ventana.btnSalir.clicked.connect(self.volver)
            except AttributeError:
                print("Verifica el objectName del botón para regresar en mejor_vendedor.ui")

        #las columnas ocupan toda la pantalla de forma prolija
        try:
            self.ventana.tablaMejorVendedor.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        except AttributeError:
            print("Verifica el objectName de la QTableWidget en mejor_vendedor.ui")

    def cargarMejorVendedor(self):
        try:
            #consulta devuelve una unica fila con: nombre_vendedor, total_vendido
            vendedor_top = self.reportes_service.mejor_vendedor()

            if vendedor_top:
                self.ventana.tablaMejorVendedor.setRowCount(1)
                #celda 0: nombre del vendedor 
                self.ventana.tablaMejorVendedor.setItem(0, 0, QTableWidgetItem(str(vendedor_top[0])))
                #celda 1:total facturado acumulado 
                self.ventana.tablaMejorVendedor.setItem(0, 1, QTableWidgetItem(f"$ {vendedor_top[1]:.2f}"))
                #celda 2: una etiqueta de referencia
                self.ventana.tablaMejorVendedor.setItem(0, 2, QTableWidgetItem("Vendedor Top"))
            else:
                self.ventana.tablaMejorVendedor.setRowCount(0)
        except Exception as ex:
            print("Error al cargar el mejor vendedor:", ex)

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()