from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QInputDialog 
from data.producto_data import ProductoData
from bases_de_datos.sqlite_db import Conexion
from data.venta_data import VentaData
from services.inventario_service import InventarioService
from services.factura_service import FacturaService

class RealizarVenta():
    def __init__(self ,id_usuario, volver_callback =None):
        loader = QUiLoader()
        self.ventana = loader.load("gui/realizar_venta.ui")
        self.db_conexion = Conexion()
        self.producto_data = ProductoData(self.db_conexion)
        self.carrito= [] #lista de productos acumulados
        self.producto_seleccionado = None
        self.initGUI()
        self.ventana.show()
        self.volver_callback = volver_callback
    
        self.venta_data = VentaData(self.db_conexion)
        self.id_usuario = id_usuario

        self.inventario_service = InventarioService()
        self.factura_service = FacturaService()

    #conexion de botones
    def initGUI(self): 
        self.ventana.btnBuscar.clicked.connect(self.buscar_producto)
        self.ventana.btnAgregar.clicked.connect(self.agregarAlCarrito)
        self.ventana.btnBorrar.clicked.connect(self.eliminarDelCarrito)
        self.ventana.btnFin.clicked.connect(self.finalizarVenta)
        self.ventana.spnCantidad.setMinimum(1) 
        self.ventana.btn_volver.clicked.connect(self.volver)

    def buscar_producto(self):
        entrada = self.ventana.txtIdProducto.text().strip()
        
        if not entrada:
            QMessageBox.warning(self.ventana, "Atención", "Por favor, ingrese un ID o el nombre del producto.")
            return

        if entrada.isdigit():
            id_producto = int(entrada)
            producto = self.producto_data.obtener_por_id(id_producto)
            if producto:
                self.mostrar_producto_en_labels(producto)
            else:
                QMessageBox.information(self.ventana, "No encontrado", f"No se encontró ningún producto con el ID #{id_producto}")
        
        else:
            try:
                todos = self.producto_data.obtener_todos()
                coincidencias = [p for p in todos if entrada.lower() in p.nombre.lower()]
                
                if not coincidencias:
                    QMessageBox.information(self.ventana, "No encontrado", f"No hay productos de maquillaje que coincidan con '{entrada}'")
                    return
                
                #si encontró un solo producto con ese nombre, lo carga directo
                if len(coincidencias) == 1:
                    self.mostrar_producto_en_labels(coincidencias[0])
                
                else:
                    items = [f"#{p.id} - {p.nombre} (${p.precio:.2f})" for p in coincidencias]
                    seleccion, ok = QInputDialog.getItem(
                        self.ventana, 
                        "Seleccionar Producto", 
                        f"Se encontraron {len(coincidencias)} productos.\nSeleccione el correcto:", 
                        items, 0, False
                    )
                    
                    if ok and seleccion:
                        #extraemos el ID del elemento seleccionado
                        id_seleccionado = int(seleccion.split(" ")[0].replace("#", ""))
                        producto_elegido = self.producto_data.obtener_por_id(id_seleccionado)
                        self.mostrar_producto_en_labels(producto_elegido)
                        
            except Exception as e:
                QMessageBox.critical(self.ventana, "Error", f"Error en la búsqueda por nombre: {e}")

    def mostrar_producto_en_labels(self, producto):
        """Asigna los datos del producto de maquillaje a tus QLabels de la interfaz"""
        self.ventana.lblNombre.setText(producto.nombre)
        self.ventana.lblPrecio.setText(f"$ {producto.precio:.2f}")
        self.ventana.lblStock.setText(str(producto.stock_actual))
        
        #se usa el mismo nombre que en agregarAlCarrito
        self.producto_seleccionado = producto
    
    def agregarAlCarrito(self):
        if not self.producto_seleccionado:
            QMessageBox.warning(self.ventana, "Error", "Primero busque un producto")
            return

        cantidad_nueva = self.ventana.spnCantidad.value()

        #averigua si el producto ya fue agregado antes al carrito
        producto_repetido = None
        indice_fila = -1

        for i, item in enumerate(self.carrito):
            if item["id"] == self.producto_seleccionado.id:
                producto_repetido = item
                indice_fila = i #guardamos la posicion de la fila en la tabla
                break
        
        cantidad_total = cantidad_nueva 
        if producto_repetido: 
            cantidad_total += producto_repetido["cantidad"]

        #validacion de stock considerando el total acumulado
        if cantidad_total > self.producto_seleccionado.stock_actual:
            QMessageBox.warning(self.ventana, "Error", f"No hay suficiente stock. Quedan: {self.producto_seleccionado.stock_actual}")
            return
        
        #actualizar o insertar segun corresponda
        if producto_repetido:  
            #producto ya existia 
            producto_repetido["cantidad"] = cantidad_total
            producto_repetido["subtotal"] = cantidad_total * item["precio"]

            #actualizamos visualmente la fila que ya existía en la tabla (columnas 3 y 4)
            self.ventana.tablaDetalle.setItem(indice_fila, 3, QTableWidgetItem(str(producto_repetido["cantidad"])))
            self.ventana.tablaDetalle.setItem(indice_fila, 4, QTableWidgetItem(f"${producto_repetido["subtotal"]:.2f}"))
        
        else: 
            #producto nuevo
            subtotal = cantidad_nueva * self.producto_seleccionado.precio

            item = { 
                "id": self.producto_seleccionado.id,
                "nombre": self.producto_seleccionado.nombre,
                "precio": self.producto_seleccionado.precio,
                "cantidad": cantidad_nueva,
                "subtotal": subtotal
            }
            self.carrito.append(item)

             #agregamos fila nueva en la tabla Detalle
            fila = self.ventana.tablaDetalle.rowCount()
            self.ventana.tablaDetalle.insertRow(fila)

            self.ventana.tablaDetalle.setItem(fila, 0, QTableWidgetItem(str(item["id"])))
            self.ventana.tablaDetalle.setItem(fila, 1, QTableWidgetItem(str(item["nombre"])))
            self.ventana.tablaDetalle.setItem(fila, 2, QTableWidgetItem(f"${item['precio']:.2f}"))
            self.ventana.tablaDetalle.setItem(fila, 3, QTableWidgetItem(str(item["cantidad"])))
            self.ventana.tablaDetalle.setItem(fila, 4, QTableWidgetItem(f"${item["subtotal"]:.2f}"))

        #actualizacion del TOTAL GENERAL y limpieza del buscador de arriba
        self.actualizarTotalGeneral()
        self.limpiarCamposProducto()
        self.ventana.txtIdProducto.clear()

    #recalcula el total de la tabla 
    def actualizarTotalGeneral(self):
        total = sum(item["subtotal"] for item in self.carrito)
        self.ventana.lblTotal.setText(f"${total:.2f}")
    
    def eliminarDelCarrito(self):
        fila = self.ventana.tablaDetalle.currentRow()

        if fila < 0:
            QMessageBox.warning(self.ventana, "Error", "Seleccione un producto de la tabla para borrar")
            return
        
        self.carrito.pop(fila)
        self.ventana.tablaDetalle.removeRow(fila)
        self.actualizarTotalGeneral()
    
    #actualiza el stock en la base de datos
    def finalizarVenta(self):
        if len(self.carrito) == 0:
            QMessageBox.warning(self.ventana, "Error", "No hay productos cargados en la venta")
            return
        
        pregunta = QMessageBox.question(self.ventana, "Confirmar", "¿Desea confirmar la venta de los productos cargados en el carrito?",
            QMessageBox.Yes | QMessageBox.No
        )

        if pregunta == QMessageBox.No:
            return
        try:
           #calculo del total de la venta
           total = sum(item["subtotal"] for item in self.carrito) 

            #crear cabecera de la venta
           id_venta= self.venta_data.crear_venta(self.id_usuario, total)
        
           for item in self.carrito:
                producto_db = self.producto_data.obtener_por_id(item["id"])

                self.venta_data.agregar_detalle(
                    id_venta,
                    item["id"],
                    item["cantidad"],
                    item["precio"]
                )
        
                nuevo_stock = producto_db.stock_actual - item["cantidad"]
                self.producto_data.actualizar_stock(item["id"], nuevo_stock)
                
                self.inventario_service.mongo.registrar_movimiento({
                    "id_producto": item["id"],
                    "tipo": "SALIDA",
                    "cantidad": item["cantidad"],
                    "motivo": "Venta"
                })
           
            #guardar datos en sqlite
           self.db_conexion.con.commit()
           texto_del_ticket = self.factura_service.generar_ticket_txt(id_venta,list(self.carrito), total)
           msg = QMessageBox(self.ventana)
           msg.setIcon(QMessageBox.Icon.Information) # Icono de información explícito
           msg.setWindowTitle("Venta Confirmada")
           msg.setText(texto_del_ticket) # Acá le seteamos el texto limpio
           msg.setStyleSheet("QLabel{ font-family: 'Courier New'; font-size: 12px; }")
           msg.exec()
            
            #limpiar carrito y tabla
           self.carrito.clear()
           self.ventana.tablaDetalle.setRowCount(0)
           self.actualizarTotalGeneral()    
           self.limpiarCamposProducto()
           self.ventana.txtIdProducto.clear()
           self.ventana.txtIdProducto.setFocus()
       
        except Exception as ex:
            self.db_conexion.con.rollback()
            QMessageBox.critical(self.ventana, "Error", str(ex))

    def limpiarCamposProducto(self):
        self.producto_seleccionado = None
        self.ventana.lblNombre.setText("--")
        self.ventana.lblPrecio.setText("--")
        self.ventana.lblStock.setText("--")
        self.ventana.spnCantidad.setValue(1)

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()