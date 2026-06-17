import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from bases_de_datos.sqlite_db import Conexion

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
            cursor = self.db_conexion.cur
            #consulta para traer las ventas del usuario actual
            cursor.execute("""
                SELECT id, fecha, total 
                FROM ventas 
                WHERE id_usuario = ?
                ORDER BY id DESC
            """, (self.usuario.id,))
            
            ventas = cursor.fetchall()
            
            self.ventana.tablaVentas.setRowCount(len(ventas))
            
            for fila, venta in enumerate(ventas):
                self.ventana.tablaVentas.setItem(fila, 0, QTableWidgetItem(str(venta[0])))
                self.ventana.tablaVentas.setItem(fila, 1, QTableWidgetItem(str(venta[1])))
                self.ventana.tablaVentas.setItem(fila, 2, QTableWidgetItem(f"$ {venta[2]:.2f}"))
                
        except Exception as ex:
            print("Error al cargar las ventas del vendedor:", ex)

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()