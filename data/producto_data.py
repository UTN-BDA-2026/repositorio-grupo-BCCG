from bases_de_datos.sqlite_db import Conexion
from model.producto import Producto

class ProductoData():
    def __init__(self):
        self.db = Conexion()

    def obtener_todos(self):
        self.db.cur.execute(
            "SELECT * FROM productos")
        
        rows = self.db.cur.fetchall()
        return [Producto(*row) for row in rows]

    def insertar(self, producto):
        self.db.cur.execute("""
            INSERT INTO productos (codigo, nombre, id_categoria, precio, stock_actual)
            VALUES (?, ?, ?, ?, ?) 
        """, (producto.codigo, producto.nombre, producto.id_categoria, producto.precio, producto.stock_actual)) #pasar valores desde Python a la consulta SQL, sin preocuparse por las comillas, string, etc
        self.db.con.commit() 

    def actualizar_stock(self, id_producto, nuevo_stock):
        self.db.cur.execute("""
            UPDATE productos SET stock_actual=? WHERE id=?
        """, (nuevo_stock, id_producto))
        self.db.con.commit()

    def obtener_por_id(self, id_producto):
        self.db.cur.execute(
            "SELECT * FROM productos WHERE id=?", (id_producto,))
        
        row = self.db.cur.fetchone()
        if row:
            return Producto(*row)
        return None
    
    #para eliminar un producto
    def eliminar_producto(self, id_producto):
        self.db.cur.execute("""
            DELETE FROM productos
            WHERE id = ?
        """, (id_producto,))
        self.db.con.commit()
    
    #para actualizar precio
    def actualizar_precio(self, id_producto, nuevo_precio):
        self.db.cur.execute("""
            UPDATE productos
            SET precio = ?
            WHERE id = ?
        """, (nuevo_precio, id_producto))
        self.db.con.commit()