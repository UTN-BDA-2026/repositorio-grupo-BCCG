from data.producto_data import ProductoData
from data.venta_data import VentaData
from bases_de_datos.mongo_db import ConexionMongo
from bases_de_datos.sqlite_db import Conexion

class InventarioService():
    def __init__(self):

        self.db = Conexion()

        self.producto_data = ProductoData(self.db)
        self.venta_data = VentaData(self.db)
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
        
        
        try:
            #iniciar transaccion 
            self.db.con.execute("BEGIN TRANSACTION")

             #crear venta
            id_venta = self.venta_data.crear_venta(id_usuario, total)
            
            #guardar detalle
            self.venta_data.agregar_detalle(id_venta,id_producto,cantidad,producto.precio)
           
            #actualizar stock
            nuevo_stock = producto.stock_actual - cantidad
            self.producto_data.actualizar_stock(id_producto, nuevo_stock)
            
            #confirma cambios en sql
            self.db.con.commit()
            
            #registrar logs/movimientos en Mongo
            self.mongo.registrar_movimiento({
                "id_producto": id_producto,
                "tipo": "SALIDA",
                "cantidad": cantidad,
                "motivo": "Venta"
            })
            print("Venta realizada correctamente")
        
        except Exception as ex:
            #deshacer cambios
            self.db.con.rollback()
            print("Error en la venta:", ex)
    
    #para que el administrador pueda cargar stock
    def agregar_stock(self, id_producto, cantidad):
        producto = self.producto_data.obtener_por_id(id_producto)

        if producto is None:
            print("Producto no existe")
            return
        
        try: 
            self.db.con.execute("BEGIN")

            nuevo_stock = producto.stock_actual + cantidad
            self.producto_data.actualizar_stock(
                id_producto,
                nuevo_stock
            )

            self.db.con.commit()

            self.mongo.registrar_movimiento({
                "id_producto": id_producto,
                "tipo": "ENTRADA",
                "cantidad": cantidad,
                "motivo": "Reposicion"
            })
            print("Stock agregado correctamente")
        
        except Exception as ex:
            self.db.con.rollback()

            print("Error al agregar stock:", ex)
