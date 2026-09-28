import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
import os

class EnviosController:
    def __init__(self, vista):
        self.vista = vista

    def buscar_imagen_disco(self):
        # Validacion de archivos de imagenes permitidas
        tipos = [("Imagenes de control", "*.png *.jpg *.jpeg *.gif")]
        ruta = filedialog.askopenfilename(filetypes=tipos)
        if ruta: # si son los formatos permitidos cargar
            self.vista.ruta_foto_guia = ruta
            self.cargar_miniatura_pillow(ruta)

    def cargar_miniatura_pillow(self, ruta_img):
        # Si la ruta existe cargar imagen en archivo
        if not os.path.exists(ruta_img) and os.path.exists(os.path.join("..", ruta_img)):
            ruta_img = os.path.join("..", ruta_img)

        if os.path.exists(ruta_img):
            img = Image.open(ruta_img)
            img = img.resize((105, 85), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.BICUBIC)
            img_tk = ImageTk.PhotoImage(img)
            self.vista.lbl_foto_guia.config(image=img_tk)
            self.vista.lbl_foto_guia.image = img_tk

    def registrar_orden_despacho(self):
        guia_automatica = f"G-{random.randint(10000, 99999)}" # randint para generar guia automatica
        try: #extraemos el peso de la caja de texto y lo convertimos en un numero decimal
            peso_kg = float(self.vista.ent_peso.get().strip() or 0.0)
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número válido.")
            return

        # Jalamos el texto de las dimensiones, limpiamos espacios y pasamos a minisculas
        dim_texto = self.vista.ent_dimensiones.get().strip().lower()
        # Creamos un interruptor apagado para controlar si el paquete requiere un cobro extra por tamaño
        recargo_dimension = False

        if 'x' in dim_texto:
            try:
                # Si encontramos la X, cortamos las dimensiones por el separador para sacar los tamaños
                partes = dim_texto.split('x')
                alto = float(partes[0].strip())
                ancho = float(partes[1].strip())
                # Si el alto o el ancho superan los 50 centímetros, encendemos el cobro extra
                if alto > 50 or ancho > 50:
                    recargo_dimension = True
            except (ValueError, IndexError):
                # para que pase sin problema sin generar error y cerrar de forma abrupta el programa
                pass

        tarifa_por_kg = 4000
        if recargo_dimension:
            tarifa_por_kg += 500
        # Aqui generamos el calculo del costo que aparecera en el mensaje de confirmacion de envio
        costo_final_calculado = peso_kg * tarifa_por_kg

        # Traemos los datos necesario de la db y generamos de forma automatica algunos para que no vaya a generar error

        datos = {
            'numero_guia': guia_automatica,
            'fecha_hora_recepcion': self.vista.ent_fecha.get() + " 17:41:00",
            'id_cliente': self.vista.ent_id_cliente.get().strip(),
            'remitente': self.vista.ent_remitente.get().strip(),
            'destinatario': self.vista.ent_destinatario.get().strip(),
            'direccion_origen': self.vista.ent_origen.get().strip(),
            'direccion_destino': self.vista.ent_destino.get().strip(),
            'tipo_servicio': self.vista.cmb_servicio.get(),
            'descripcion_contenido': "Mercancía General Despachada",
            'peso': peso_kg,
            'dimensiones': self.vista.ent_dimensiones.get().strip() or "N/A",
            'valor_declarado': self.vista.ent_costo.get().strip() or "0.0",
            'costo': costo_final_calculado,
            'forma_pago': self.vista.cmb_pago.get(),
            'estado_actual': "en transito",
            'instrucciones_especiales': self.vista.ent_instrucciones.get().strip(),
            'ruta_distribucion': 1
        }

        # Validaciones de entrada de datos
        if not datos['id_cliente'] or not datos['direccion_destino']:
            messagebox.showerror("Error", "Los campos ID del Cliente y la Dirección Destino son obligatorios.")
            return

        # si el id cliente no es numerico lanza error
        if not str(datos['id_cliente']).isdigit():
            messagebox.showerror("Error", "El ID de Cliente debe ser un valor numérico.")
            return

        if self.vista.db:
            exito, mensaje = self.vista.db.sp_insertar_envio(datos) # traemos procedimiento almacenado y damos datos
            if exito:
                detalle_cobro = f"\n\n-GUIA\nTarifa por Kg: ${tarifa_por_kg:,}\nCOSTO TOTAL: ${costo_final_calculado:,}"
                messagebox.showinfo("Envio", f"{mensaje}\nNúmero de Guía asignado: {guia_automatica}{detalle_cobro}")
                self.limpiar_cajas()
                self.cargar_tabla_visual()
            else:
                messagebox.showerror("Falla Operativa", mensaje)
    # Cargar tabla visual
    def cargar_tabla_visual(self):
        # Extraemos los datos de mysql
        self.vista.listbox_envios.delete(0, tk.END) # Limpiamos campos

        if self.vista.db:
            registros = self.vista.db.sp_obtener_todos_envios()
            if registros:
                for r in registros:
                    self.vista.listbox_envios.insert(tk.END,
                                               f"Guía: {r[1]} | Cliente ID: {r[2]} | Destinatario: {r[3]} | Estado: {r[6]}")
            else:
                self.vista.listbox_envios.insert(tk.END, "[No hay guías de envío registradas]")

    def compilar_reporte_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Envíos"
        ws.append(["Historial de Envíos en Sistema"])

        filtro_servicio = self.vista.cmb_servicio.get()
        for i in range(self.vista.listbox_envios.size()):
            linea = self.vista.listbox_envios.get(i)
            if filtro_servicio in linea.lower() or filtro_servicio == "normal":
                ws.append([linea])

        ruta_archivo = f"Reporte_Envios_{filtro_servicio}.xlsx"
        wb.save(ruta_archivo)
        messagebox.showinfo("Realizado", f"¡Excel generado con éxito!\nArchivo: {ruta_archivo}")

    def compilar_reporte_pdf(self):
        filtro_servicio = self.vista.cmb_servicio.get()
        ruta_pdf = f"Reporte_Envios_{filtro_servicio}.pdf"
        c = canvas.Canvas(ruta_pdf, pagesize=letter)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "LOGITRANS - REPORTE DE AUDITORÍA DE ENVÍOS")
        c.line(50, 725, 550, 725)
        y = 695
        c.setFont("Helvetica", 10)
        for i in range(self.vista.listbox_envios.size()):
            linea = self.vista.listbox_envios.get(i)
            c.drawString(50, y, linea)
            y -= 20
        c.save()
        messagebox.showinfo("Realizado", f"¡PDF generado con exito!\nArchivo: {ruta_pdf}")

    # Funcion para limpiar campos
    def limpiar_cajas(self):
        self.vista.ent_id_cliente.delete(0, tk.END)
        self.vista.ent_remitente.delete(0, tk.END)
        self.vista.ent_destinatario.delete(0, tk.END)
        self.vista.ent_origen.delete(0, tk.END)
        self.vista.ent_destino.delete(0, tk.END)
        self.vista.ent_peso.delete(0, tk.END)
        self.vista.ent_dimensiones.delete(0, tk.END)
        self.vista.ent_costo.delete(0, tk.END)
        self.vista.ruta_foto_guia = "imagenes/camion_logitrans.png"
        self.cargar_miniatura_pillow(self.vista.ruta_foto_guia)
