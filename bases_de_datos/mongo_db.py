import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() 

class ConexionMongo():
    def __init__(self):
        try: 
            mongo_uri = os.getenv("MONGO_URI")
            
            self.client = MongoClient(mongo_uri)
            self.db = self.client["inventario_mongo"]
            self.coleccion = self.db["movimientos_stock"]
            print("Conexion a MongoDB Atlas en la nube exitosa")
        except Exception as ex:
            print("Error al conectar a MongoDB: ", ex)
    
    def registrar_movimiento(self, data):
        try:
            self.coleccion.insert_one(data)
            print("Movimiento registrado en Mongo")
        except Exception as ex:
            print("Error al insertar en Mongo: ", ex)

    def obtener_movimientos(self):
        try:
            return list(self.coleccion.find())
        except Exception as ex:
            print("Error al obtener movimientos de Mongo: ", ex)
            return []