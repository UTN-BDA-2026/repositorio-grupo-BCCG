import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from bases_de_datos.sqlite_db import Conexion
from data.venta_data import VentaData

class MisVentas():
    def __init__(self, usuario, volver_callback=None):
        loader = QUiLoader()
        ruta = os.path.join(os.path.dirname(__file__), "mis_ventas.ui")
        file = QFile(ruta)
        file.open(QFile.ReadOnly)
        self.ventana = loader.load(file)
        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback
        self.db_conexion = Conexion()
        self.venta_data = VentaData(self.db_conexion)

        #interfaz
        self.initGUI()
        self.cargarVentas()
        
        self.ventana.show()

    def initGUI(self):
        #boton volver
        try:
            self.ventana.btnVolver.clicked.connect(self.volver)
        except AttributeError:
            try:
                self.ventana.btn_volver.clicked.connect(self.volver)
            except AttributeError:
                print("Advertencia: No se encontró el botón para volver en mis_ventas.ui")

        #ajustar columnas de la tabla
        self.ventana.tablaVentas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def cargarVentas(self):
        try:
            ventas = self.venta_data.obtener_ventas_por_usuario(self.usuario.id)
            
            self.ventana.tablaVentas.setRowCount(len(ventas))
            
            for fila, venta in enumerate(ventas):
                self.ventana.tablaVentas.insertRow(fila
                                                   )
                self.ventana.tablaVentas.setItem(fila, 0, QTableWidgetItem(str(venta[0])))
                self.ventana.tablaVentas.setItem(fila, 1, QTableWidgetItem(str(venta[1])))
                self.ventana.tablaVentas.setItem(fila, 2, QTableWidgetItem(f"$ {venta[2]:.2f}"))
                
        except Exception as ex:
            QMessageBox.critical(self.ventana, "Error", f"No se pudieron cargar las ventas:\n{ex}")

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()