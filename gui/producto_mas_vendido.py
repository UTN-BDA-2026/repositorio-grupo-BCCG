import os 
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from services.reportes_service import ReportesService   

class ProductoMasVendido():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),
            "producto_mas_vendido.ui"
        )

        file = QFile(ruta)
        file.open(QFile.ReadOnly)

        self.ventana = loader.load(file)

        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback
        self.reportes_service = ReportesService() #instancia del servicio de reportes

        self.initGUI()
        self.cargar_tabla_ranking()
        self.ventana.show()

    def initGUI(self):
        self.ventana.btnVolver.clicked.connect(self.volver)
        self.ventana.tablaRanking.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #ajustar columnas al ancho de la tabla
    
    def cargar_tabla_ranking(self):
        try:
            ranking = self.reportes_service.obtener_productos_mas_vendidos()
            self.ventana.tablaRanking.setRowCount(len(ranking))

            for fila, prod in enumerate(ranking):
                item_nombre= QTableWidgetItem(str(prod[0]))
                item_cantidad = QTableWidgetItem(str(prod[1]))

                item_cantidad.setTextAlignment(Qt.AlignCenter)
                self.ventana.tablaRanking.setItem(fila, 0, item_nombre)
                self.ventana.tablaRanking.setItem(fila, 1, item_cantidad)
        except Exception as ex:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo cargar el ranking de productos:\n{ex}")
        
    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()