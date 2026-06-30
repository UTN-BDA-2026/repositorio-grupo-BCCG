import os
from datetime import datetime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QHeaderView
from data.producto_data import ProductoData

class InventarioAdmin(QDialog):

    def __init__(self, usuario, volver_callback=None, db=None):
        # NO llamamos a super().__init__() para evitar conflictos de doble ventana
        
        if db is None:
            try:
                from bases_de_datos.sqlite_db import Conexion
                db = Conexion()
            except Exception as e:
                print("Error al conectar base de datos:", e)

        self.producto_data = ProductoData(db)
        self.usuario = usuario
        self.volver_callback = volver_callback
        self.productos = []

        # Cargamos el diseño de forma independiente
        loader = QUiLoader()
        ruta = os.path.join(os.path.dirname(__file__), "inventario.ui")
        file = QFile(ruta)
        file.open(QFile.ReadOnly)
        self.ventana = loader.load(file) 
        file.close()

        self.initGUI()
        self.cargar_productos()
        
        self.ventana.show()

    def initGUI(self):
        self.ventana.btnActualizar.clicked.connect(self.cargar_productos)
        self.ventana.btnVolver.clicked.connect(self.volver)
        self.ventana.txtBuscar.textChanged.connect(self.filtrar_productos)

        try:
            self.ventana.tablaInventario.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        except Exception as e:
            print("Error al estirar cabeceras:", e)

    def cargar_productos(self):
        try:
            self.productos = self.producto_data.obtener_todos()
            self.mostrar_en_tabla(self.productos)
        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo cargar el inventario: {e}")

    def mostrar_en_tabla(self, lista_productos):
        from PySide6.QtCore import QDateTime
        self.ventana.tablaInventario.setRowCount(len(lista_productos))
        categorias_traductor = {
            1: "Maquillajes",
            2: "Cosméticos",
            3: "Accesorios",
            4: "Perfumería"
        }
        
        fecha_actual = QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm:ss")
        
        for fila, prod in enumerate(lista_productos):
            #Buscamos el nombre del rubro según el ID asignado
            nombre_categoria = categorias_traductor.get(prod.id_categoria, "General")

            # Creamos rigurosamente los 6 items de forma independiente
            item_id = QTableWidgetItem(str(prod.id))
            item_nombre = QTableWidgetItem(str(prod.nombre))
            item_categoria = QTableWidgetItem(str(nombre_categoria)) 
            item_stock = QTableWidgetItem(str(prod.stock_actual))
            item_precio = QTableWidgetItem(f"$ {prod.precio:.2f}")
            item_fecha = QTableWidgetItem(fecha_actual)

            # Alineaciones estéticas
            item_id.setTextAlignment(Qt.AlignCenter)
            item_categoria.setTextAlignment(Qt.AlignCenter)
            item_stock.setTextAlignment(Qt.AlignCenter)
            item_precio.setTextAlignment(Qt.AlignCenter)
            item_fecha.setTextAlignment(Qt.AlignCenter)

            # Alerta visual de stock mínimo
            if prod.stock_actual <= 5:
                item_stock.setForeground(Qt.red)

            self.ventana.tablaInventario.setItem(fila, 0, item_id)
            self.ventana.tablaInventario.setItem(fila, 1, item_nombre)
            self.ventana.tablaInventario.setItem(fila, 2, item_categoria) # Columna 2: Categoría limpia 🌟
            self.ventana.tablaInventario.setItem(fila, 3, item_stock)     # Columna 3: Cantidad / Stock
            self.ventana.tablaInventario.setItem(fila, 4, item_precio)    # Columna 4: Precio
            self.ventana.tablaInventario.setItem(fila, 5, item_fecha)     # Columna 5: Fecha ingreso

    def filtrar_productos(self):
        termino = self.ventana.txtBuscar.text().lower().strip()
        if not termino:
            self.mostrar_en_tabla(self.productos)
            return

        filtrados = [p for p in self.productos if termino in p.nombre.lower()]
        self.mostrar_en_tabla(filtrados)

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()