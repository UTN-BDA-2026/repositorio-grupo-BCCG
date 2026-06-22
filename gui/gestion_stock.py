import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDateTime
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from data.producto_data import ProductoData
from services.inventario_service import InventarioService

class StockAdmin():

    def __init__(self, usuario, volver_callback=None, db=None):
        loader = QUiLoader()
        ruta = os.path.join(os.path.dirname(__file__), "gestion_stock.ui")
        file = QFile(ruta)
        file.open(QFile.ReadOnly)
        self.ventana = loader.load(file)
        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback
        self.producto_data = ProductoData(db) 
        
        self.productos_en_lote = []

        self.inventario_service = InventarioService()

        self.initGUI()
        self.ventana.show()

    def initGUI(self):
        self.ventana.btnAgregar.clicked.connect(self.agregar_a_lista_temporal)
        self.ventana.btnCancelar.clicked.connect(self.cancelar_lote)
        self.ventana.btnConfirmar.clicked.connect(self.confirmar_y_subir_db)
        self.ventana.btnVolver.clicked.connect(self.volver)

        try:
            self.ventana.tablaStock.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        except Exception as e:
            print("Error al estirar cabeceras de tabla:", e)

    def agregar_a_lista_temporal(self):
        nombre_producto = self.ventana.txtProducto.text().strip()
        cantidad_txt = self.ventana.txtCantidad.text().strip()
        precio_txt = self.ventana.txtPrecio.text().strip()

        if not nombre_producto or not cantidad_txt or not precio_txt:
            QMessageBox.warning(self.ventana, "Campos Vacíos", "Por favor, completa Producto, Cantidad y Precio.")
            return

        try:
            cantidad = int(cantidad_txt)
            precio = float(precio_txt)
            if cantidad <= 0 or precio <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self.ventana, "Datos Inválidos", "Cantidad y Precio deben ser números mayores a cero.")
            return

        fecha_hora_actual = QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm:ss")

        item_lote = {
            "nombre": nombre_producto,
            "cantidad": cantidad,
            "precio": precio,
            "fecha_hora": fecha_hora_actual
        }
        self.productos_en_lote.append(item_lote)

        self.actualizar_tabla_visual()

        self.ventana.txtProducto.clear()
        self.ventana.txtCantidad.clear()
        self.ventana.txtPrecio.clear()
        self.ventana.txtProducto.setFocus()

    def actualizar_tabla_visual(self):
        self.ventana.tablaStock.setRowCount(len(self.productos_en_lote))
        for fila, prod in enumerate(self.productos_en_lote):
            self.ventana.tablaStock.setItem(fila, 0, QTableWidgetItem(prod["nombre"]))
            self.ventana.tablaStock.setItem(fila, 1, QTableWidgetItem(str(prod["cantidad"])))
            self.ventana.tablaStock.setItem(fila, 2, QTableWidgetItem(f"$ {prod['precio']:.2f}"))
            self.ventana.tablaStock.setItem(fila, 3, QTableWidgetItem(prod["fecha_hora"]))

    def cancelar_lote(self):
        if not self.productos_en_lote:
            QMessageBox.information(self.ventana, "Información", "La tabla ya está vacía.")
            return
        
        pregunta = QMessageBox.question(
            self.ventana, "Cancelar Carga",
            "¿Estás seguro de que deseas vaciar la lista? Se borrarán todos los productos cargados en la tabla.",
            QMessageBox.Yes | QMessageBox.No
        )
        if pregunta == QMessageBox.Yes:
            self.productos_en_lote.clear()
            self.actualizar_tabla_visual()

    def confirmar_y_subir_db(self):
        if not self.productos_en_lote:
            QMessageBox.warning(self.ventana, "Lista Vacía", "No hay ningún producto en el listado para procesar.")
            return

        pregunta = QMessageBox.question(
            self.ventana, "Confirmar Carga", 
            f"¿Deseas guardar estos {len(self.productos_en_lote)} productos definitivamente en la Base de Datos?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if pregunta == QMessageBox.Yes:
            from model.producto import Producto
            errores = 0
            
            id_categoria_valido= None
            try:
                cursor = self.producto_data.db.con.cursor()
                cursor.execute("SELECT id FROM categorias LIMIT 1")
                resultado = cursor.fetchone()

                if resultado:
                    id_categoria_valido = resultado[0]
                else:
                    cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", ('General',))
                    id_categoria_valido = cursor.lastrowid
            except Exception as e:
                print("Error al verificar categorias en SQLite, usando ID 1 por defecto:", e)
                id_categoria_valido = 1

            for item in self.productos_en_lote:
                try:
                    codigo_autogenerado = item["nombre"][:3].upper() + str(int(QDateTime.currentMSecsSinceEpoch()) % 1000)
                    id_categoria_defecto = 1 
                    
                    nuevo_producto = Producto(
                        id=None,
                        codigo=codigo_autogenerado,
                        nombre=item["nombre"],
                        id_categoria=id_categoria_valido,
                        precio=item["precio"],
                        stock_actual=item["cantidad"]
                    )
                    
                    self.producto_data.insertar(nuevo_producto)

                    #Registro de ingreso de mercaderia como una ENTRADA Mongo Historial 
                    self.inventario_service.mongo.registrar_movimiento({
                        "id_producto": nuevo_producto.id,
                        "tipo": "ENTRADA",
                        "cantidad": nuevo_producto.stock_actual,
                        "motivo": "Carga Inicial"
                    })
                except Exception as e:
                    print(f"Error al insertar el producto {item['nombre']}: {e}")
                    errores += 1

            if errores == 0:
                QMessageBox.information(self.ventana, "Éxito", "¡Todos los productos se guardaron correctamente en la Base de Datos!")
                self.productos_en_lote.clear()
                self.actualizar_tabla_visual()
            else:
                QMessageBox.warning(self.ventana, "Carga incompleta", f"Se procesó el lote, pero hubo problemas con {errores} registros.")
                
    def volver(self):
        if self.productos_en_lote:
            pregunta = QMessageBox.question(
                self.ventana, "Salir", 
                "Hay elementos en la tabla que no has subido. ¿Deseas salir de todas formas perdiendo los cambios?",
                QMessageBox.Yes | QMessageBox.No
            )
            if pregunta == QMessageBox.No:
                return

        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()