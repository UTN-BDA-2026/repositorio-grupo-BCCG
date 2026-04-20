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