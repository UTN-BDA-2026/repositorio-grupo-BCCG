import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from bases_de_datos.sqlite_db import Conexion   
from gui.gestion_stock import StockAdmin
from gui.inventario import InventarioAdmin
from gui.bajo_stock import StockBajo
from gui.movimientos_stock import MovimientosStock

class MenuInventario():
    def __init__(self, usuario, volver_callback=None, db=None):
        loader = QUiLoader()
        ruta = os.path.join(os.path.dirname(__file__), "menu_inventario.ui")
        file = QFile(ruta)
        file.open(QFile.ReadOnly)
        self.ventana = loader.load(file)
        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback
        
        self.initGUI()
        self.ventana.show()

    def initGUI(self):
        self.ventana.btnProductos.clicked.connect(self.abrir_inventario_general)
        self.ventana.btnStock.clicked.connect(self.abrir_gestion_stock)
        self.ventana.btnStockBajo.clicked.connect(self.abrir_stock_bajo)
        self.ventana.btnHistorial.clicked.connect(self.abrir_movimientos_stock)
        self.ventana.btnVolver.clicked.connect(self.volver)

    def abrir_inventario_general(self):
        print("Abrir control de inventario")
        self.inventario = InventarioAdmin(self.usuario, volver_callback=self.mostrar_menu_inventario, db=None)
        self.ventana.hide()
        self.inventario.ventana.show()
        
    def abrir_gestion_stock(self):
        self.ventana.hide()
        self.stock = StockAdmin(self.usuario, volver_callback=self.mostrar_menu_inventario, db=Conexion())

    def abrir_stock_bajo(self):
        print("Abrir reporte de stock bajo")
        self.ventana.hide()
        self.bajo_stock = StockBajo(self.usuario,volver_callback=self.mostrar_menu_inventario)


    def abrir_movimientos_stock(self):
        print("Abrir movimientos de stock")
        self.ventana.hide()
        self.movimientos = MovimientosStock(self.usuario, volver_callback=self.mostrar_menu_inventario)

    def mostrar_menu_inventario(self):
        self.ventana.show()

    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()