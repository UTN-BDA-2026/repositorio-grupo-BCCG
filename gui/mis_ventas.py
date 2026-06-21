import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from bases_de_datos.sqlite_db import Conexion
from data.venta_data import VentaData

class MisVentas():
    def __init__(self, usuario, volver_callback=None):
        loader = QUiLoader()
        self.ventana= loader.load("gui/mis_ventas.ui")

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
       
        self.ventana.tablaVentas.itemClicked.connect(self.cargarDetalleVenta)
        #ajustar columnas de la tabla
        self.ventana.tablaVentas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #ocultamos la tabla detalles hasta que se seleccione una venta
        try: 
            self.ventana.tablaDetalleVenta.hide()
        except AttributeError: 
            pass 

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

    def cargarDetalleVenta(self, item):
        try:
            self.ventana.tablaDetalleVenta.show()
            self.ventana.tablaDetalleVenta.setRowCount(0)

            fila_seleccionada = item.row()
            id_venta = self.ventana.tablaVentas.item(fila_seleccionada, 0).text()

            detalles = self.venta_data.obtener_detalle_venta(id_venta)

            for d in detalles:
                fila = self.ventana.tablaDetalleVenta.rowCount()
                self.ventana.tablaDetalleVenta.insertRow(fila)
                
                self.ventana.tablaDetalleVenta.setItem(fila, 0, QTableWidgetItem(str(d[0])))
                self.ventana.tablaDetalleVenta.setItem(fila, 1, QTableWidgetItem(str(d[1])))
                self.ventana.tablaDetalleVenta.setItem(fila, 2, QTableWidgetItem(f"$ {d[2]:.2f}"))
                self.ventana.tablaDetalleVenta.setItem(fila, 3, QTableWidgetItem(f"$ {d[3]:.2f}"))
                
        except Exception as ex:
            print(f"Error al cargar el detalle de la factura: {ex}")
            
    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()