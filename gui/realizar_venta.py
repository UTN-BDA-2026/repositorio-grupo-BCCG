from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget
from data.producto_data import ProductoData
from bases_de_datos.sqlite_db import Conexion
from data.venta_data import VentaData

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

    #conexion de botones
    def initGUI(self): 
        self.ventana.btnBuscar.clicked.connect(self.buscarProducto)
        self.ventana.btnAgregar.clicked.connect(self.agregarAlCarrito)
        self.ventana.btnBorrar.clicked.connect(self.eliminarDelCarrito)
        self.ventana.btnFin.clicked.connect(self.finalizarVenta)
        self.ventana.spnCantidad.setMinimum(1) 
        self.ventana.btn_volver.clicked.connect(self.volver)

    def buscarProducto(self): 
        id_prod = self.ventana.txtIdProducto.text()

        producto = self.producto_data.obtener_por_id(id_prod)

        if producto:
            self.producto_seleccionado = producto
            self.ventana.lblNombre.setText(str(producto.nombre))
            self.ventana.lblPrecio.setText(f"${producto.precio:.2f}")
            self.ventana.lblStock.setText(str(producto.stock_actual))
        else:
            QMessageBox.warning(self.ventana, "Error", "El producto no existe")
            self.limpiarCamposProducto()
    
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

            # Actualizamos visualmente la fila que ya existía en la tabla (columnas 2 y 3)
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
            #guardar datos en sqlite
           self.db_conexion.con.commit()
            
           QMessageBox.information(self.ventana, "Éxito", "Venta realizada y stock actualizado")
            
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


