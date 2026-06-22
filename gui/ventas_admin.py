from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from gui.mejor_vendedor import MejorVendedor
from gui.producto_mas_vendido import ProductoMasVendido
from services.reportes_service import ReportesService #importamos el servicio de reportes
import os
from services.factura_service import FacturaService

class Ventas():

    def __init__(self, usuario, volver_callback=None):

        loader = QUiLoader()

        ruta = os.path.join(
            os.path.dirname(__file__),
            "ventas_admin.ui"
        )

        file = QFile(ruta)
        file.open(QFile.ReadOnly)

        self.ventana = loader.load(file)

        file.close()

        self.usuario = usuario
        self.volver_callback = volver_callback
        self.reportes_service = ReportesService() #instancia del servicio de reportes
        self.factura_service = FacturaService() #instancia del servicio de facturas

        self.initGUI()
     
        self.ventana.show()

    def initGUI(self):
        try: #conectamos el boton de calcular total general
            self.ventana.btnTotalVendido.clicked.connect(
                self.calcularTotalGeneral
            )    
        except:
            pass
        
        try:
            self.ventana.btnVolver.clicked.connect(
                self.volver
                )
        except:
            pass

        try: 
            self.ventana.btnProdMasVendido.clicked.connect(
                self.abrir_productos_mas_vendidos)     
        except:
            pass

        try:
            self.ventana.btnMejorVendedor.clicked.connect(
                self.abrir_mejor_vendedor
            )
        except:
            pass

        try: 
            self.ventana.btnExportarPdf.clicked.connect(
                self.exportarReporteMensual
            )
        except:
            pass

    def calcularTotalGeneral(self):
        total= self.reportes_service.total_vendido()
        self.ventana.lblTotalVendido.setText(f"${total:.2f}")
    
    def volver(self):
        self.ventana.hide()
        if self.volver_callback:
            self.volver_callback()

    def abrir_mejor_vendedor(self):
        self.mejor = MejorVendedor(
            self.usuario,
            volver_callback=self.mostrar_ventas
        )

        self.ventana.close()

    def abrir_productos_mas_vendidos(self):
        self.ventana.hide()
        self.productos_mas_vendidos = ProductoMasVendido(
            self.usuario,
            volver_callback=self.mostrar_ventas
        )

        self.ventana.close()

    def exportarReporteMensual(self):
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        import os # Aseguramos tener os importado para abrir el archivo
        
        # 1. El Admin elige el período
        mes, ok1 = QInputDialog.getInt(self.ventana, "Reporte Mensual", "Ingresa el número de mes (1-12):", 6, 1, 12)
        if not ok1: return
        
        anio, ok2 = QInputDialog.getInt(self.ventana, "Reporte Mensual", "Ingresa el año (Ejemplo: 2026):", 2026, 2020, 2030)
        if not ok2: return

        try:
            cursor = self.reportes_service.db.con.cursor()
            
            # 2. Consultamos las ventas totales para el Administrador
            query = """
                SELECT id, fecha, total 
                FROM ventas 
                WHERE strftime('%m', fecha) = ? AND strftime('%Y', fecha) = ?
            """
            cursor.execute(query, (f"{mes:02d}", str(anio)))
            ventas_db = cursor.fetchall()

            if len(ventas_db) == 0:
                QMessageBox.information(self.ventana, "Reporte Vacío", f"No se registraron ventas en {mes:02d}/{anio}.")
                return

            # 3. Se genera el PDF administrativo
            ruta_del_reporte = self.factura_service.generar_reporte_mensual_pdf(mes, anio, ventas_db)

            # 4. Avisamos que se generó y le damos paso a la apertura automática
            QMessageBox.information(
                self.ventana, 
                "Reporte Guardado", 
                f"El informe PDF se generó con éxito.\n\nA continuación se abrirá el documento de manera automática."
            )

            if os.path.exists(ruta_del_reporte):
                os.startfile(ruta_del_reporte)

        except Exception as ex:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo generar o abrir el reporte: {str(ex)}")

    def mostrar_ventas(self):
        self.ventana.show()