import os 
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox

from services.inventario_service import InventarioService
from data.producto_data import ProductoData
from bases_de_datos.sqlite_db import Conexion

class MovimientosStock():
    def __init__(self, usuario, volver_callback=None):
        loader = QUiLoader()
        ruta = os.path.join(os.path.dirname(__file__), "movimientos_stock.ui")
        file = QFile(ruta)
        file.open(QFile.ReadOnly)
        self.ventana = loader.load(file)
        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback

        self.inventario_service = InventarioService()
        self.producto_data = ProductoData(Conexion())

        self.initGUI()
        self.cargar_movimientos()

        self.ventana.show()

    def initGUI(self):
        self.ventana.btnVolver.clicked.connect(self.volver)
        try:
            self.ventana.tablaMovimientos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        except Exception as e:
            print("Error al estirar cabeceras:", e)

    def cargar_movimientos(self):
        try:
            #recupera la lista de documentos de
            logs = self.inventario_service.obtener_historial_movimientos()

            self.ventana.tablaMovimientos.setRowCount(len(logs))    
            
            for fila, log in enumerate(logs):
                #Mongo guarda el ID, buscamos el Nombre en SQLite
                id_prod = log.get("id_producto")
                producto = self.producto_data.obtener_por_id(id_prod)
                nombre_producto= producto.nombre if producto else f"Producto #{id_prod}"

                tipo = log.get("tipo", "-")
                cantidad= log.get("cantidad", 0)
                motivo = log.get("motivo", "-")

                item_prod = QTableWidgetItem(nombre_producto)
                item_tipo = QTableWidgetItem(str(tipo))
                item_cant = QTableWidgetItem(str(cantidad))
                item_motivo = QTableWidgetItem(str(motivo))

                item_cant.setTextAlignment(Qt.AlignCenter)
                item_tipo.setTextAlignment(Qt.AlignCenter)

                # Estética: Alertar con colores (Rojo para egresos, Verde para ingresos)
                if tipo == "SALIDA":
                    item_tipo.setForeground(Qt.red)
                elif tipo == "ENTRADA":
                    item_tipo.setForeground(Qt.darkGreen)
                
                self.ventana.tablaMovimientos.setItem(fila, 0, item_prod)
                self.ventana.tablaMovimientos.setItem(fila, 1, item_tipo)
                self.ventana.tablaMovimientos.setItem(fila, 2, item_cant)
                self.ventana.tablaMovimientos.setItem(fila, 3, item_motivo)

        except Exception as ex:
            QMessageBox.critical(self.ventana, "Error", f"No se pudieron cargar los movimientos:\n{ex}")

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()