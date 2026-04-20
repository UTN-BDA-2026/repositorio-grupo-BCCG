import sqlite3

class Conexion():
    def __init__(self):
        try:
            self.con= sqlite3.connect("inventario.db")
            self.cur = self.con.cursor()
            self.crearTablas()
            self.crearAdmin()
        except Exception as ex: 
            print("Error al conectar: ",ex)
    
    def crearTablas(self):
        # Tabla de usuarios (para el login y roles)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nombre TEXT NOT NULL, 
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'vendedor' -- 'admin' o 'vendedor'
            )""")

        # Tabla categorias (para organizar los productos)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre TEXT NOT NULL
        )
        """)

        #Tabla productos 
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            codigo TEXT UNIQUE NOT NULL, 
            nombre TEXT NOT NULL, 
            id_categoria INTEGER,
            precio REAL NOT NULL,
            stock_actual INTEGER DEFAULT 0,
            FOREIGN KEY (id_categoria) REFERENCES categorias(id)
            )
        """)

        #Tabla de Ventas 
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_usuario INTEGER,
            total REAL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
            )
            """)    
        
        #Detalle de la venta (que productos se llevaron en cada venta)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_venta INTEGER, 
            id_producto INTEGER,
            cantidad INTEGER,
            precio_unitario REAL,
            FOREIGN KEY (id_venta) REFERENCES ventas(id),
            FOREIGN KEY (id_producto) REFERENCES productos(id)
        )
        """)
        self.con.commit()
    

    def crearAdmin(self):
        try: 
            self.cur.execute(
                "SELECT * FROM usuarios WHERE usuario =?", ("admin",)
            )
            admin = self.cur.fetchone()
            if admin is None:
                self.cur.execute("""
                    INSERT INTO usuarios (nombre, usuario, clave, rol)
                    VALUES (?,?,?,?)
                    """, ("Administrador", "admin", "admin123", "admin"))
                self.con.commit()
                print("Admin creado correctamente")
            else:
                print("El admin ya existe")
        except Exception as ex:
            print("Error al crear admin:", ex)

#nuevo 
    def conectar(self): 
        return self.con  
           
# cierra conexion 
    def cerrar(self):
        self.con.close()

if __name__ == "__main__":
    con = Conexion()
    con.cerrar()

