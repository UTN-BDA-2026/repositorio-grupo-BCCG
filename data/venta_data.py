from bases_de_datos.sqlite_db import Conexion

class VentaData():
    def __init__(self):
        self.db = Conexion()

    def crear_venta(self, id_usuario, total):
        self.db.cur.execute("""
            INSERT INTO ventas (id_usuario, total)
            VALUES (?, ?)
        """, (id_usuario, total))
        self.db.con.commit()
        return self.db.cur.lastrowid

    def agregar_detalle(self, id_venta, id_producto, cantidad, precio):
        self.db.cur.execute("""
            INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (id_venta, id_producto, cantidad, precio))
        self.db.con.commit()