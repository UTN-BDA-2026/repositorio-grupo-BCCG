from bases_de_datos.sqlite_db import Conexion

class ReportesService():
    def __init__(self):
        self.db = Conexion()

    #para el total vendido
    def total_vendido(self):
        try:
            self.db.cur.execute("""
                SELECT SUM(total)
                FROM ventas
            """)

            resultado = self.db.cur.fetchone()

            if resultado[0] is None:
                return 0

            return resultado[0]

        except Exception as ex:
            print("Error al calcular total vendido:", ex)
            return 0

    #para los productos con bajo stock
    def productos_bajo_stock(self):
        try:
            self.db.cur.execute("""
                SELECT nombre, stock_actual
                FROM productos
                WHERE stock_actual <= 5
            """)

            return self.db.cur.fetchall()

        except Exception as ex:
            print("Error al obtener productos con bajo stock:", ex)
            return []

    #productos mas vendidos
    def productos_mas_vendidos(self):
        try:
            self.db.cur.execute("""
                SELECT productos.nombre,
                       SUM(detalle_venta.cantidad) as total_vendido
                FROM detalle_venta

                JOIN productos
                ON detalle_venta.id_producto = productos.id

                GROUP BY productos.id

                ORDER BY total_vendido DESC
            """)

            return self.db.cur.fetchall()

        except Exception as ex:
            print("Error al obtener productos más vendidos:", ex)
            return []

    #mejor vendedor
    def mejor_vendedor(self):
        try:
            self.db.cur.execute("""
                SELECT usuarios.nombre,
                       SUM(ventas.total) as total_vendido

                FROM ventas

                JOIN usuarios
                ON ventas.id_usuario = usuarios.id

                GROUP BY usuarios.id

                ORDER BY total_vendido DESC

                LIMIT 1
            """)

            return self.db.cur.fetchone()

        except Exception as ex:
            print("Error al obtener mejor vendedor:", ex)
            return None