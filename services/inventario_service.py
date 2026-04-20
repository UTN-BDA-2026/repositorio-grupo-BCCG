from data.producto_data import ProductoData
from data.venta_data import VentaData
from bases_de_datos.mongo_db import ConexionMongo

class InventarioService():
    def __init__(self):
        self.producto_data = ProductoData()
        self.venta_data = VentaData()
        self.mongo = ConexionMongo()

    def vender_producto(self, id_usuario, id_producto, cantidad):
        producto = self.producto_data.obtener_por_id(id_producto)

        if producto is None:
            print("Producto no existe")
            return

        if producto.stock_actual < cantidad:
            print("Stock insuficiente")
            return
        total = producto.precio * cantidad
        #crear venta
        id_venta = self.venta_data.crear_venta(id_usuario, total)
        #guardar detalle
        self.venta_data.agregar_detalle(
            id_venta,
            id_producto,
            cantidad,
            producto.precio
        )
        #actualizar stock
        nuevo_stock = producto.stock_actual - cantidad
        self.producto_data.actualizar_stock(id_producto, nuevo_stock)
        #registrar en Mongo
        self.mongo.registrar_movimiento({
            "id_producto": id_producto,
            "tipo": "SALIDA",
            "cantidad": cantidad,
            "motivo": "Venta"
        })

        print("Venta realizada correctamente")