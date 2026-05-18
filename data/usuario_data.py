from bases_de_datos.sqlite_db import Conexion
from model.usuario import Usuario

class UsuarioData():
    def __init__(self):
        self.db = Conexion()

    def login(self,usuario,clave):
        try:
            self.db.cur.execute(
                "SELECT * FROM usuarios WHERE usuario=? AND clave=?", (usuario,clave))

            row= self.db.cur.fetchone()

            if row: 
                return Usuario(*row) #convierte a objeto Usuario
            else:
                return None
            
        except Exception as ex: 
            print("Error en login", ex)
            return None
    #funciones para el administrador de crear y eliminar usuarios, y obtener lista de usuarios
    def crear_usuario(self, nombre, usuario, clave, rol):
        try:
            self.db.cur.execute("""
                INSERT INTO usuarios
                (nombre, usuario, clave, rol)
                VALUES (?, ?, ?, ?)
            """, (nombre, usuario, clave, rol))
            self.db.con.commit()
            print("Usuario creado correctamente")
        except Exception as ex:
            print("Error al crear usuario:", ex)

    def eliminar_usuario(self, id_usuario):
        try:
            self.db.cur.execute("""
                DELETE FROM usuarios
                WHERE id = ?
            """, (id_usuario,))
            self.db.con.commit()
            print("Usuario eliminado")
        except Exception as ex:
            print("Error al eliminar usuario:", ex)

    def obtener_usuarios(self):
        try:
            self.db.cur.execute("""
                SELECT * FROM usuarios
            """)
            rows = self.db.cur.fetchall()
            return [Usuario(*row) for row in rows]
        except Exception as ex:
            print("Error al obtener usuarios:", ex)
            return []