import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
from datetime import datetime

class IncidentesController:
    def __init__(self, vista):
        self.vista = vista

    # Procesamiento de datos
    def ejecutar_reporte_incidente(self):
        # Create de alertas, limpiamos espacios.
        v_id = self.vista.ent_vehiculo_id.get().strip()
        c_id = self.vista.ent_conductor_id.get().strip()
        ubicacion = self.vista.ent_ubicacion.get().strip()
        desc = self.vista.txt_descripcion.get().strip() # Aqui ajustamos si la descripcion es larga

        # Validaciones, si no hay datos ingresados no se pueden generar reportes
        if not v_id or not c_id or not ubicacion or not desc:
            messagebox.showerror("Campos Incompletos",
                                 "Error: Todos los campos del reporte de incidente son obligatorios.")
            return

        # Validacion numerica con .isdigit --> Rechaza letras
        if not v_id.isdigit() or not c_id.isdigit():
            messagebox.showerror("Error",
                                 "Los códigos de vehículo y conductor deben contener únicamente números.")
            return
        # Aqui por medio de randint vamos a generar el codigo aleatorio
        codigo_alerta = f"IS-{random.randint(10000, 99999)}"
        # Aqui vamos a dejar el incidente con la fecha ya hora exacta que se reporta
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Simulamos la ubicacion geografica
        gps_simulado = f"{random.uniform(6.1, 6.3):.4f}, -75.5888"

        # Aqui tenemos todo lo que la db necesita reunir, por este motivo hay unos datos inventados.
        datos = {
            'vehiculo_id': int(v_id),
            'conductor_id': int(c_id),
            'codigo': codigo_alerta,
            'fecha_hora': fecha_actual,
            'tipo_incidente': self.vista.cmb_tipo_incidente.get(),
            'ubicacion': ubicacion,
            'descripcion': desc,
            'causas': "Investigación en curso", # Inventado
            'consecuencias': "Retraso logístico controlado", # Inventado
            'medidas_tomadas': "Asistencia enviada por centro de control", # Inventado
            'estado_resolucion': "Pendiente" # Inventado
        }

        # Alerta de incidente registrado
        messagebox.showerror(
            "LOGITRANS",
            f"¡Incidente Reportado!\nSe ha notificado al Centro de Distribución de forma prioritaria."
            f"\n\nCódigo: {codigo_alerta}\nUbicación GPS Enviada: {gps_simulado}"
        )

        if self.vista.db:
            exito, mensaje = self.vista.db.sp_insertar_incidente(datos) # Aqui traemos el procedimiento almacenado
            if exito:
                self.limpiar_campos() # Limpiamos campos
                self.cargar_tabla_visual() # Recargamos tabla
            else:
                messagebox.showerror("Error de Red", mensaje)
    def cargar_tabla_visual(self):
        # Limpiamos el tablero antes de hacer el read
        self.vista.listbox_incidentes.delete(0, tk.END)

        if self.vista.db:
            registros = self.vista.db.sp_obtener_incidentes_activos() # Obtenemos el procedimiento almacenado
            if registros:
                for r in registros:
                    # Aqui damos la orden de como queremos que se vea el texto en la lista
                    self.vista.listbox_incidentes.insert(tk.END, f"Alerta {r} | Fecha: {r} | Placa: {r} | Tipo: {r}")
            else:
                self.vista.listbox_incidentes.insert(tk.END, "[No hay incidentes viales activos en las rutas]")


    # Exportacion pdf y excel
    def exportar_excel_incidentes(self):
        # inicializamos la hoja en blanco
        wb = Workbook()
        ws = wb.active
        ws.title = "Incidentes"
        ws.append(["Historial de Control de Incidentes"])
        # Filtramos el incidente ingresado
        filtro_tipo = self.vista.cmb_tipo_incidente.get()

        for i in range(self.vista.listbox_incidentes.size()):
            linea = self.vista.listbox_incidentes.get(i)
            ws.append([linea])
            # Aqui no es necesario hacerle validacion de campos, dado que tenemos una lista desplegable

        ruta_archivo = "Reporte_Incidentes_Modulo.xlsx"
        wb.save(ruta_archivo)
        messagebox.showinfo("openpyxl Realizado",
                            f"¡Excel de incidentes generado correctamente!\nArchivo: {ruta_archivo}")
    # Exportamos a pdf
    def exportar_pdf_incidentes(self):
        # Creamos la hoja y damos parametros
        filtro_tipo = self.vista.cmb_tipo_incidente.get()
        ruta_pdf = "Reporte_Incidentes_Modulo.pdf"
        c = canvas.Canvas(ruta_pdf, pagesize=letter)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "LOGITRANS - CONTROL DE RECURSOS Y OPERACIONES DE FLOTA")
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 735, f"Reporte de Contingencias y Siniestros  |  Filtro Automático: {filtro_tipo}")
        c.line(50, 725, 550, 725)
        y = 695
        c.setFont("Helvetica", 10)

        for i in range(self.vista.listbox_incidentes.size()):
            linea = self.vista.listbox_incidentes.get(i)
            c.drawString(50, y, linea)
            y -= 20
            if y < 50:
                c.showPage()
                y = 700

        c.save()
        messagebox.showinfo("Realizado",
                            f"¡Reporte de incidentes guardado con éxito!\nArchivo: {ruta_pdf}")
    # Funcion para limpiar campos
    def limpiar_campos(self):
        self.vista.ent_vehiculo_id.delete(0, tk.END)
        self.vista.ent_conductor_id.delete(0, tk.END)
        self.vista.ent_ubicacion.delete(0, tk.END)
        self.vista.txt_descripcion.delete(0, tk.END)
        self.vista.cmb_tipo_incidente.current(0)
