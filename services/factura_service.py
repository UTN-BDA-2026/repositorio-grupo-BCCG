import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class FacturaService():
    def __init__(self):
        #carpeta para los tickets diarios en txt
        self.carpeta_txt= os.path.join(os.path.dirname(__file__), "tickets")
        if not os.path.exists(self.carpeta_txt):
            os.makedirs(self.carpeta_txt, exist_ok=True)

        #carpeta para los reportes administrativos en PDF
        self.carpeta_reportes = os.path.join(os.path.dirname(__file__), "reportes_mensuales")
        if not os.path.exists(self.carpeta_reportes):
            os.makedirs(self.carpeta_reportes, exist_ok=True)


    def generar_ticket_txt(self, id_venta, carrito, total):
        os.path.exists("tickets") or os.makedirs("tickets", exist_ok=True)
        nombre_archivo = f"tickets/ticket_{id_venta}.txt"

        texto_ticket = "====================================\n"
        texto_ticket += "          TICKET DE VENTA           \n"
        texto_ticket += "====================================\n"
        texto_ticket += f"Venta N°: {id_venta}\n"
        texto_ticket += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        texto_ticket += "PRODUCTOS:\n"
        texto_ticket += "------------------------------------\n"
        
        for item in carrito:
            precio_unitario = item["subtotal"] / item["cantidad"]
            texto_ticket += f"{item['nombre']} x{item['cantidad']} \n"
            texto_ticket += f'${precio_unitario:.2f} c/u    Subtotal: ${item["subtotal"]:.2f}\n\n'

        texto_ticket += "====================================\n"
        texto_ticket += f"TOTAL: ${total:.2f}\n"
        texto_ticket += "====================================\n"
        texto_ticket += "¡Gracias por su compra!\n"

        #guardamos en el archivo .txt
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(texto_ticket)

        return texto_ticket

    def generar_reporte_mensual_pdf(self, mes, anio, ventas_mes):
        nombre_archivo = f"reporte_ventas_{anio}_{mes:02d}.pdf"
        ruta_pdf = os.path.join(self.carpeta_reportes, nombre_archivo)

        c = canvas.Canvas(ruta_pdf, pagesize=letter)
        ancho, alto = letter
        y = alto - 60 #Coordenada de inicio vertical

        #encabezado del reporte
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(ancho / 2, y, f"REPORTE MENSUAL DE VENTAS")
        y -= 30
        c.setFont("Helvetica", 11)
        c.drawCentredString(ancho / 2, y, f"Periodo Comercial: {mes:02d} / {anio}")
        
        y -= 25
        c.setLineWidth(0.5)
        c.line(70, y, ancho - 70, y) #línea horizontal

        #encabezado de la tabla
        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(80, y, "ID Venta")
        c.drawString(150, y, "Fecha y Hora")
        c.drawRightString(ancho - 80, y, "Total Facturado")

        y -= 10
        c.line(70, y, ancho - 70, y)
        
        # --- LISTADO DINÁMICO DE VENTAS ---
        c.setFont("Helvetica", 10)
        total_acumulado = 0
        
        for v in ventas_mes:
            y -= 20
            id_v, fecha, total = v # Desestructuramos los datos que vienen de SQLite
            
            c.drawString(70, y, f"#{id_v}")
            c.drawString(180, y, str(fecha))
            c.drawRightString(ancho - 70, y, f"$ {total:.2f}")
            total_acumulado += total
            
            # Control de fin de página (por si hay muchas ventas en el mes)
            if y < 60:
                c.showPage()
                y = alto - 60
                c.setFont("Helvetica", 10)
                
        # --- CIERRE DE INFORME Y TOTALES ---
        y -= 25
        c.line(70, y, ancho - 70, y)
        
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y, "TOTAL RECAUDADO EN EL MES:")
        c.drawRightString(ancho - 70, y, f"$ {total_acumulado:.2f}")
        
        y -= 15
        c.line(70, y, ancho - 70, y)
        
        # Cerramos y guardamos el documento
        c.save()
        return ruta_pdf