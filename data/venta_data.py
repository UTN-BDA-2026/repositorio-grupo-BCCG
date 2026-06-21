#from bases_de_datos.sqlite_db import Conexion

class VentaData():
    def __init__(self,db):
        self.db = db

    def crear_venta(self, id_usuario, total):
        self.db.cur.execute("""
            INSERT INTO ventas (id_usuario, fecha, total)
            VALUES (?, DATETIME('now', 'localtime'),?)
        """, (id_usuario, total))
        return self.db.cur.lastrowid

    def agregar_detalle(self, id_venta, id_producto, cantidad, precio):
        self.db.cur.execute("""
            INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (id_venta, id_producto, cantidad, precio))
    
    def obtener_ventas_por_usuario(self, id_usuario):
        self.db.cur.execute("""
            SELECT id, fecha, total
            FROM ventas
            WHERE id_usuario = ?
            ORDER BY fecha DESC
            """ , (id_usuario,))
        return self.db.cur.fetchall() #devuelve una lista de tuplas con las ventas
    
    def obtener_detalle_venta(self, id_venta):
        self.db.cur.execute("""
            SELECT p.nombre, d.cantidad, d.precio_unitario, (d.cantidad * d.precio_unitario) AS subtotal
            FROM detalle_venta d
            JOIN productos p ON d.id_producto = p.id
            WHERE d.id_venta = ?
            """, (id_venta))
        return self.db.cur.fetchall()