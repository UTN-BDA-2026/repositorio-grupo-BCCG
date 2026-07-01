import os
from datetime import datetime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDateTime, Qt 
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from data.producto_data import ProductoData
from services.inventario_service import InventarioService
from model.producto import Producto

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
        self.ventana.btnQuitar.clicked.connect(self.quitar_producto_seleccionado)
        self.ventana.btnBuscar.clicked.connect(self.buscar_producto_existente)
        self.ventana.btnCancelar_2.clicked.connect(self.limpiar_tabla_busqueda)
        self.ventana.tablaBusqueda.cellChanged.connect(self.actualizar_fecha_hora_edicion)
        
        try:
            self.producto_data.db.cur.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (1, 'Maquillajes')")
            self.producto_data.db.cur.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (2, 'Cosméticos')")
            self.producto_data.db.cur.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (3, 'Accesorios')")
            self.producto_data.db.cur.execute("INSERT OR IGNORE INTO categorias (id, nombre) VALUES (4, 'Perfumería')")
            self.producto_data.db.con.commit() # Guardamos en la base de datos
        except Exception as e:
            print("Aviso: No se pudieron forzar las categorías en SQLite:", e)

        self.ventana.combo_categoria.clear()
        self.ventana.combo_categoria.addItems([
            "1 - Maquillajes",
            "2 - Cosméticos",
            "3 - Accesorios",
            "4 - Perfumería",
        ])
        
        try:
            self.ventana.tablaStock.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ventana.tablaBusqueda.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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

        texto_combo = self.ventana.combo_categoria.currentText().strip()
        
        categorias_db = {
            "1 - Maquillajes": 1,
            "2 - Cosméticos": 2,
            "3 - Accesorios": 3,
            "4 - Perfumería": 4
        }
        
        id_cat = categorias_db.get(texto_combo, 1)
        
        if " - " in texto_combo:
            categoria_texto = texto_combo.split(" - ")[1].strip()
        else:
            categoria_texto = texto_combo

        fecha_hora_actual = QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm:ss")

        item_lote = {
            "nombre": nombre_producto,
            "id_categoria": id_cat,      
            "categoria": categoria_texto, 
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
            self.ventana.tablaStock.setItem(fila, 1, QTableWidgetItem(prod["categoria"]))   
            self.ventana.tablaStock.setItem(fila, 2, QTableWidgetItem(str(prod["cantidad"])))
            self.ventana.tablaStock.setItem(fila, 3, QTableWidgetItem(f"$ {prod['precio']:.2f}")) 
            self.ventana.tablaStock.setItem(fila, 4, QTableWidgetItem(prod["fecha_hora"]))  
            
            self.ventana.tablaStock.item(fila, 2).setTextAlignment(Qt.AlignCenter)
            self.ventana.tablaStock.item(fila, 3).setTextAlignment(Qt.AlignCenter)

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
        filas_busqueda = self.ventana.tablaBusqueda.rowCount()
        
        if not self.productos_en_lote and filas_busqueda == 0:
            QMessageBox.warning(self.ventana, "Tablas Vacías", "No hay elementos cargados en el lote ni modificaciones de stock en la búsqueda.")
            return

        pregunta = QMessageBox.question(
            self.ventana, "Confirmar Cambios", 
            "¿Deseas procesar todas las operaciones (Carga masiva y modificaciones) definitivamente?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if pregunta == QMessageBox.No:
            return

        errores_lote = 0
        
        if self.productos_en_lote:
            for item in self.productos_en_lote:
                try:
                    codigo_autogenerado = item["nombre"][:3].upper() + str(int(QDateTime.currentMSecsSinceEpoch()) % 1000)
                    
                    nuevo_producto = Producto(
                        id=0,
                        codigo=codigo_autogenerado,
                        nombre=item["nombre"],
                        id_categoria=item["id_categoria"], 
                        precio=item["precio"],
                        stock_actual=item["cantidad"]
                    )
                    
                    self.producto_data.insertar(nuevo_producto)

                    try:
                        ultimo_id = self.producto_data.db.cur.lastrowid
                    except Exception:
                        ultimo_id = 1

                    self.inventario_service.mongo.registrar_movimiento({
                        "id_producto": ultimo_id,
                        "tipo": "ENTRADA",
                        "cantidad": nuevo_producto.stock_actual,
                        "motivo": "Carga Inicial"
                    })
                except Exception as error_real:
                    QMessageBox.critical(
                        self.ventana, 
                        "ERROR DETECTADO EN EL LOTE", 
                        f"Producto con problemas: {item['nombre']}\n\nEl error real es: {error_real}"
                    )
                    errores_lote += 1

        try:
            categorias_inverso = {
                "Maquillajes": 1,
                "Cosméticos": 2,
                "Accesorios": 3,
                "Perfumería": 4
            }

            for fila in range(filas_busqueda):
                fecha_item = self.ventana.tablaBusqueda.item(fila, 4)
                if fecha_item is not None and fecha_item.text() != "--":
                    id_producto = self.ventana.tablaBusqueda.item(fila, 0).data(Qt.UserRole)
                    
                    nombre_editado = self.ventana.tablaBusqueda.item(fila, 0).text().strip()
                    categoria_editada_txt = self.ventana.tablaBusqueda.item(fila, 1).text().strip()
                    nueva_cantidad = int(self.ventana.tablaBusqueda.item(fila, 2).text())

                    precio_editado_txt = self.ventana.tablaBusqueda.item(fila, 3).text().replace("$", "").strip()
                    precio_editado = float(precio_editado_txt)

                    id_categoria_editado = categorias_inverso.get(categoria_editada_txt, 1)
                    
                    self.producto_data.actualizar_datos_producto(id_producto, nombre_editado, id_categoria_editado, precio_editado)
                    
                    prod_antiguo = self.producto_data.obtener_por_id(id_producto)
                    stock_anterior = prod_antiguo.stock_actual if prod_antiguo else nueva_cantidad
                    
                    self.producto_data.actualizar_stock(id_producto, nueva_cantidad)
                    
                    diferencia = nueva_cantidad - stock_anterior
                    if diferencia != 0:
                        tipo_mov = "ENTRADA" if diferencia > 0 else "SALIDA"
                        self.inventario_service.mongo.registrar_movimiento({
                            "id_producto": id_producto,
                            "tipo": tipo_mov,
                            "motivo": f"Ajuste masivo interactivo (Stock de {stock_anterior} -> {nueva_cantidad})"
                        })

            self.producto_data.db.con.commit()
            
            if errores_lote == 0:
                QMessageBox.information(self.ventana, "Éxito", "¡Todo el inventario y stock han sido actualizados de forma exitosa!")
                self.productos_en_lote.clear()
                self.actualizar_tabla_visual()
                self.limpiar_tabla_busqueda()
            else:
                QMessageBox.warning(self.ventana, "Carga incompleta", f"Se procesaron los datos, pero hubo problemas con {errores_lote} registros del lote.")

        except Exception as e:
            self.producto_data.db.con.rollback()
            QMessageBox.critical(self.ventana, "Error", f"No se pudo completar la carga: {e}")
            
    def quitar_producto_seleccionado(self):
        fila_seleccionada = self.ventana.tablaStock.currentRow()
        
        if fila_seleccionada == -1:
            QMessageBox.warning(self.ventana, "Atención", "Por favor, selecciona primero un producto de la tabla para quitarlo.")
            return
            
        nombre_prod = self.productos_en_lote[fila_seleccionada]["nombre"]
        pregunta = QMessageBox.question(
            self.ventana, "Quitar Producto",
            f"¿Seguro de que deseas quitar '{nombre_prod}' de la lista?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if pregunta == QMessageBox.Yes:
            self.productos_en_lote.pop(fila_seleccionada)
            self.actualizar_tabla_visual()
            
    def buscar_producto_existente(self):
        nombre_buscar = self.ventana.txtProducto_2.text().strip().lower()
        if not nombre_buscar:
            QMessageBox.warning(self.ventana, "Atención", "Por favor, ingresa un nombre para buscar.")
            return

        categorias_traductor = {
            1: "Maquillajes",
            2: "Cosméticos",
            3: "Accesorios",
            4: "Perfumería"
        }

        try:
            todos = self.producto_data.obtener_todos()
            coincidencias = [p for p in todos if nombre_buscar in p.nombre.lower()]
            
            self.ventana.tablaBusqueda.cellChanged.disconnect()
            self.ventana.tablaBusqueda.setRowCount(0)
            
            if not coincidencias:
                QMessageBox.information(self.ventana, "No encontrado", f"No se encontraron productos con el nombre '{nombre_buscar}'.")
                self.ventana.tablaBusqueda.cellChanged.connect(self.actualizar_fecha_hora_edicion)
                return

            for producto in coincidencias:
                fila = self.ventana.tablaBusqueda.rowCount()
                self.ventana.tablaBusqueda.insertRow(fila)
                item_nombre = QTableWidgetItem(producto.nombre)
                
                nombre_categoria = categorias_traductor.get(producto.id_categoria, "General")
                item_categoria = QTableWidgetItem(nombre_categoria)
                
                item_cantidad = QTableWidgetItem(str(producto.stock_actual))
                
                item_precio = QTableWidgetItem(f"${producto.precio:.2f}")
                
                item_fecha = QTableWidgetItem("--")
                item_fecha.setFlags(item_fecha.flags() ^ Qt.ItemIsEditable)
                
                item_nombre.setData(Qt.UserRole, producto.id)
            
                self.ventana.tablaBusqueda.setItem(fila, 0, item_nombre)    
                self.ventana.tablaBusqueda.setItem(fila, 1, item_categoria) 
                self.ventana.tablaBusqueda.setItem(fila, 2, item_cantidad)  
                self.ventana.tablaBusqueda.setItem(fila, 3, item_precio)    
                self.ventana.tablaBusqueda.setItem(fila, 4, item_fecha)     

                self.ventana.tablaBusqueda.item(fila, 2).setTextAlignment(Qt.AlignCenter)
                self.ventana.tablaBusqueda.item(fila, 3).setTextAlignment(Qt.AlignCenter)
           
            self.ventana.tablaBusqueda.cellChanged.connect(self.actualizar_fecha_hora_edicion)
            
        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"Error al buscar: {e}")

    def actualizar_fecha_hora_edicion(self, fila, columna):
        if columna in [0, 1, 2, 3]:
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.ventana.tablaBusqueda.cellChanged.disconnect()
            self.ventana.tablaBusqueda.setItem(fila, 4, QTableWidgetItem(ahora)) 
            self.ventana.tablaBusqueda.cellChanged.connect(self.actualizar_fecha_hora_edicion)

    def limpiar_tabla_busqueda(self):
        self.ventana.txtProducto_2.clear()
        self.ventana.tablaBusqueda.setRowCount(0)
    
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