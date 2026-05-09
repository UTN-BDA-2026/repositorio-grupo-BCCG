from bases_de_datos.sqlite_db import Conexion
from model.categoria import Categoria

class CategoriaData():
    def __init__(self):
        self.db = Conexion()

    def crear_categoria(self, nombre):
        try:
            self.db.cur.execute("""
                INSERT INTO categorias (nombre)
                VALUES (?)
            """, (nombre,))

            self.db.con.commit()
            print("Categoria creada")

        except Exception as ex:
            print("Error al crear categoria:", ex)

    def obtener_categorias(self):
        try:
            self.db.cur.execute("""
                SELECT * FROM categorias
            """)

            rows = self.db.cur.fetchall()

            categorias = []

            for row in rows:
                categorias.append(Categoria(*row))

            return categorias

        except Exception as ex:
            print("Error al obtener categorias:", ex)
            return []

    def eliminar_categoria(self, id_categoria):
        try:
            self.db.cur.execute("""
                DELETE FROM categorias
                WHERE id = ?
            """, (id_categoria,))

            self.db.con.commit()
            print("Categoria eliminada")

        except Exception as ex:
            print("Error al eliminar categoria:", ex)