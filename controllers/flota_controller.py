import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class FlotaController:
    def __init__(self, vista):
        self.vista = vista

    # Procesamiento de datos
    def ejecutar_vinculacion_flota(self):
        # Validamos la entrada de datos, extraemos los datos los datos digitados por el usuario y lo limpiamos
        # Quitamos puntos o espacios con el .strip
        id_vehiculo = self.vista.ent_vehiculo.get().strip()
        id_conductor = self.vista.ent_conductor.get().strip()

        # aqui es donde validamos que no hayan campos vacios
        if not id_vehiculo or not id_conductor:
            messagebox.showerror("Campos Vacíos",
                                 "Error: Los campos ID Vehículo / ID Conductor son obligatorios.")
            return

        # validamos entrada numerica por medio de .isdigit
        if not id_vehiculo.isdigit() or not id_conductor.isdigit():
            messagebox.showerror("Error",
                                 "Error, los id vehiculo/conductor deben ser numericos.")
            return

        # Confirmacion antes de vincular al vehiculo con el conductor
        messagebox.showwarning(
            "LogiTrans - Flota",
            "El sistema procederá a verificar que el camión y el conductor estén en estado 'Disponible' antes del despacho."
        )

        # Aqui nos integramos con la db
        if self.vista.db:
            # llamamos al procedimiento almacenado para actualizar la vinculación
            exito, mensaje = self.vista.db.sp_asignar_conductor_vehiculo(int(id_conductor), int(id_vehiculo))
            if exito:
                # si es exitoso enviamos la info
                messagebox.showinfo("Operacion finalizada de form exitosa", mensaje)
                self.vista.ent_vehiculo.delete(0, tk.END) # limpiamos los campos
                self.vista.ent_conductor.delete(0, tk.END)
                self.cargar_tabla_visual()
            else:
                messagebox.showerror("Error Logístico", mensaje)

    def cargar_tabla_visual(self):
        # Limpiamos el tablero antes de hacer el read
        self.vista.listbox_flota.delete(0, tk.END)

        if self.vista.db:
            registros = self.vista.db.sp_obtener_monitoreo_flota() # Obtenemos el procedimiento almacenado
            # y obtenemos el resultado de la flota
            if registros: # Recorremos cada registro
                for r in registros:
                    # Aqui damos la orden de como queremos que se vea el texto en la lista
                    self.vista.listbox_flota.insert(tk.END, f"Asignación #{r} | Conductor: {r} | Placa: {r}")
            else:
                self.vista.listbox_flota.insert(tk.END, "[No hay asignaciones registradas en la flota]")
    # Aqui vamos a crear la exportacion para la cual ya le hicimos el espacio
    def exportar_excel_flota(self):
        # inicializamos una hoja nueva y la activamos
        wb = Workbook()
        ws = wb.active
        ws.title = "Flota Asignaciones"
        ws.append(["Historial del Panel de Control de Flota"])

        # filtramos el vehiculo ingresado
        filtro_vehiculo = self.vista.ent_vehiculo.get().strip()

        # iteramos registro por registro
        for i in range(self.vista.listbox_flota.size()):
            linea = self.vista.listbox_flota.get(i) # mostramos datos uno a uno
            if not filtro_vehiculo or filtro_vehiculo in linea:
                ws.append([linea]) # si pasa el filtro, se agrega la fila al Excel

        # Aqui le damos la ruta al archivo
        ruta_archivo = "Reporte_Flota_Modulo.xlsx"
        wb.save(ruta_archivo) # Guardamos
        # Enviamos mensaje info para decirle al usuario que se genero con exito
        messagebox.showinfo("Realizado",
                            f"¡Reporte Excel de flota generado correctamente!\nArchivo: {ruta_archivo}")

    # Aqui exportamos el pdf
    def exportar_pdf_flota(self):
        # Inicializamos pdf en blanco
        ruta_pdf = "Reporte_Flota_Modulo.pdf"
        c = canvas.Canvas(ruta_pdf, pagesize=letter)

        # Damos los parametros de config para el pdf que se va a generar
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "LOGITRANS - CONTROL DE RECURSOS Y OPERACIONES DE FLOTA")
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 735, f"Reporte de Monitoreo flota  |  Auditoría: Jenny Florez")
        c.line(50, 725, 550, 725) # linea que separa el encabezado
        y = 695 # Aqui damos la coordenada de ubicacion de los datos en el pdf
        c.setFont("Helvetica", 10)

        # Aqui añadimos los datos extraidos al pdf
        filtro_vehiculo = self.vista.ent_vehiculo.get().strip() # limpiamos espacios, llamamos la funcion
        for i in range(self.vista.listbox_flota.size()):
            linea = self.vista.listbox_flota.get(i) # mostramos los datos uno a uno
            if not filtro_vehiculo or filtro_vehiculo in linea:
                c.drawString(50, y, linea)
                y -= 20 # Aqui evitamos que los datos se junten
                if y < 50:
                    c.showPage() #  Creamos una nueva pagina en blanco si los datos no caben en la primera
                    y = 700 # Reiniciamos el renglon de arriba de toda la nueva hoja
        # Guardamos pdf
        c.save()
        messagebox.showinfo("Realizado", f"¡Reporte PDF generado con éxito!\nArchivo: {ruta_pdf}")
