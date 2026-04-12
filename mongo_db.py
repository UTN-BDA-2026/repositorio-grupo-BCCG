from pymongo import MongoClient
class ConexionMongo():
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["inventario_mongo"]
            self.coleccion = self.db["movimientos_stock"] #coleccion donde se guarda movimientos de stock
            print("Conexion a MongoDB exitosa")
        except Exception as ex:
            print("Error al conectar a MongoDB: ", ex)
    
    def registrar_movimiento(self,data):
        """
        data debe ser un diccionario, ej: 
        {'id_producto': 1, 'tipo': 'SALIDA', 'cantidad': 2, 'motivo': 'Venta'}
        """
        try:
            self.coleccion.insert_one(data)
            print("Movimiento registrado en Mongo")
        except Exception as ex:
            print("Error al insertar en Mongo: ", ex)

# Probar la conexión
if __name__ == "__main__":
    mongo = ConexionMongo()

# Ejemplo de prueba: registrar un movimiento
    mongo.registrar_movimiento({'id_producto': 1, 'tipo': 'ENTRADA', 'cantidad': 10})