import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
import re
import os

class ClienteController:
    def __init__(self, vista):
        self.vista = vista

    # Aqui definimos las acciones

    def seleccionar_imagen_disco(self):
        # Validacion de archivos de imagenes permitidas
        tipos_archivos = [("Imágenes de Control", "*.png *.jpg *.jpeg *.gif")]
        ruta = filedialog.askopenfilename(filetypes=tipos_archivos)
        if ruta: # si son los formatos permitidos cargar
            self.vista.ruta_imagen_cargada = ruta
            self.actualizar_miniatura_foto(ruta)

    def actualizar_miniatura_foto(self, ruta_imagen):
        # Corrección de ruta dinámica para pruebas individuales o ejecución desde la raíz
        if not os.path.exists(ruta_imagen) and os.path.exists(os.path.join("..", ruta_imagen)):
            ruta_imagen = os.path.join("..", ruta_imagen)

        # Actualizar foto miniatura
        if os.path.exists(ruta_imagen): # si el archivo pertenece a la carpeta de ejecuta
            img = Image.open(ruta_imagen) # abrimos la imagen
            # Aqui le damos el tamaño a la imagen para que quepa en el recuadro que creamos para ella
            img = img.resize((105, 85), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.BICUBIC)
            # llamamos a la etiqueta
            img_tk = ImageTk.PhotoImage(img)
            # esta parte del codigo nos permite que python conserve la imagen y no la borre
            self.vista.lbl_foto.config(image=img_tk)
            self.vista.lbl_foto.image = img_tk

    # Aqui llamamos a la funcion para guardar cliente
    def ejecutar_guardado_cliente(self):
        # Generamos el codigo automatico por medio de randint le damos un rango numerico
        codigo_automatico = f"CL-{random.randint(1000, 9999)}"


        # llamamos a los datos del formulario
        datos = self.obtener_datos_formulario()
        datos['codigo_unico'] = codigo_automatico # Renombramos la funcion de codigo unico de la db para que sea
        # automatico en el sistema de creacion de cliente

        # si el nombre del cliente es numerico da error
        if datos['nombre_o_razon_social'].isnumeric():
            messagebox.showerror("Error", "El nombre del cliente debe ser alfabetico.")
            return

        # validaciones
        # si no ha escrito los datos en el campo, no permitira guardar cliente
        if not datos['nombre_o_razon_social'] or not datos['rut_o_dni']:
            messagebox.showerror("Error de Campos", "Los campos Nombre/Empresa y Cc/Nit son obligatorios.")
            return

        # si los datos cc/nit no son numericos envia un mensaje de error
        if not datos['rut_o_dni'].isdigit():
            messagebox.showerror("Error Numérico",
                                 "El campo Cc / Nit solo permite numeros, intente de nuevo.")
            return

        # Validacion de email
        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Creamos los campos requeridos o validos
        # con re.match comprobamos si los campos cumplen con el requerimiento especifico, pasamos el re.match
        # y despues pasamos el requerimiento, en este caso datos
        if datos['email'] and not re.match(patron_correo, datos['email']):
            # mensaje de error solicitando que escriba bien el correo
            messagebox.showerror("Error", "El formato del correo electrónico ingresado no es válido "
                                 "(Ejemplo: usuario@dominio.com).")
            return

        # Envío a la base de datos el cliente si todas las validaciones se dan con exito
        if self.vista.db: #llamamos la funcion conexion con la database creada en el __init__
            exito, mensaje = self.vista.db.sp_insertar_cliente(datos) # insertamos los datos del cliente a la db
            if exito: # si es exitoso enviamos un mensaje confirmando
                messagebox.showinfo("Operación Exitosa","\nCliente registrado correctamente")

                # limpiamos la ventana
                self.limpiar_formulario()
                # recargamos la ventana
                self.cargar_tabla_visual()
            else: # si no enviamos un mensaje de error
                messagebox.showerror("Error en Base de Datos", mensaje)

    # actualizacion de cliente
    def ejecutar_actualizacion_cliente(self):

        # llamamos al procedimiento almacenado, si
        if not self.vista.cliente_seleccionado_id:
            messagebox.showwarning("Error", "Por favor seleccione primero un cliente de la lista de la "
                                   "derecha para poder editarlo.")
            return
        # Obtenemos los datos del formulario
        datos = self.obtener_datos_formulario()
        # Actualizamos cliente por id
        datos['cliente_id'] = self.vista.cliente_seleccionado_id

        # Mensaje para confirmar la actualizacion
        if messagebox.askyesno("Confirmar Actualización",
                               "¿Está segur@ de que desea guardar los cambios sobre este registro?"):
            if self.vista.db:
                # llamamos los datos de mysql
                exito, mensaje = self.vista.db.sp_actualizar_cliente(datos)
                if exito:
                    messagebox.showinfo("Registro actualizado", mensaje)
                    self.limpiar_formulario()
                    self.cargar_tabla_visual()
                else:
                    messagebox.showerror("Error Logístico", mensaje)
     # creamos la funcion para eliminar cliente
    def ejecutar_eliminacion_cliente(self):
        # curselection es para saber exactamente que estamos seleccionando desde el mouse
        seleccion = self.vista.listbox_clientes.curselection()
        if not seleccion: # si no se selecciona solicitamos nuevamente que lo seleccione para poderlo eliminar
            messagebox.showwarning("Atención", "Por favor seleccione un cliente de la lista para proceder.")
            return
        # Mensaje de confirmacion
        confirmar = messagebox.askyesno(
            "Atencion",
            "¿Está completamente segur@ de que desea eliminar este cliente de la base de datos?"
            "\nEsta acción no se puede deshacer."
        )
        # si confirma
        if confirmar:
            if self.vista.db:
                texto_fila = self.vista.listbox_clientes.get(seleccion) # Traemos la seleccion de cliente
                # Envolvemos el proceso en un try - except
                try:
                    # como estamos guardando los clientes en fila, este comando sirve
                    # que extraiga solo el id a eliminar
                    cliente_id = int(texto_fila.split(" | ")[0])

                    exito, mensaje = self.vista.db.sp_eliminar_cliente(cliente_id)
                    if exito:
                        messagebox.showinfo("Éxito", mensaje)
                        self.limpiar_formulario()
                        self.cargar_tabla_visual()
                    else:
                        messagebox.showerror("Error al borrar", mensaje)
                except (ValueError, IndexError) as e:
                    messagebox.showerror("Error", f"No se pudo extraer el ID del cliente: {e}")

    def cargar_cliente_seleccionado_en_campos(self, event):
        # Cargamos el cliente seleccionado en el mouse
        seleccion = self.vista.listbox_clientes.curselection()
        if not seleccion:
            return

        texto_fila = self.vista.listbox_clientes.get(seleccion) # Cargamos la seleccion a la ventana con los datos
        try:
            # separamos los elementos y los ubica en el espacio que van
            self.vista.cliente_seleccionado_id = int(texto_fila.split(" | ")[0])
        except (ValueError, IndexError):
            return

        if self.vista.db:
            conn = self.vista.db.conectar() # llamamos al metodo para conectarnos a la data base
            # Aqui hacemos la operacion CRUD, la encapsulamos en el bloque try para evitar que el programa se
            #cierre de forma abrupta si algo sucede
            if conn:
                try:
                    cursor = conn.cursor() # inicializamos el cursor
                    cursor.execute(
                        "SELECT tipo_cliente, nombre_o_razon_social, rut_o_dni, direccion_fiscal, "
                        "telefono, email, persona_contacto FROM cliente WHERE clienteID = %s",
                        (self.vista.cliente_seleccionado_id,)) # aqui va el crud
                    res = cursor.fetchone() # traemos los datos exacto de la database
                    if res:
                        # Si el cliente existe, limpiamos las cajas desde el inicio al fin y
                        # metemos los datos nuevos de la db
                        self.vista.cmb_tipo.set(res[0])
                        self.vista.ent_nombre.delete(0, tk.END)
                        self.vista.ent_nombre.insert(0, res[1])
                        self.vista.ent_rut.delete(0, tk.END)
                        self.vista.ent_rut.insert(0, res[2])
                        self.vista.ent_dir_fiscal.delete(0, tk.END)
                        self.vista.ent_dir_fiscal.insert(0, res[3])
                        self.vista.ent_telefono.delete(0, tk.END)
                        self.vista.ent_telefono.insert(0, res[4])
                        self.vista.ent_email.delete(0, tk.END)
                        self.vista.ent_email.insert(0, res[5])
                        self.vista.ent_contacto.delete(0, tk.END)
                        self.vista.ent_contacto.insert(0, res[6])
                    cursor.close() # Cerramos intermediario
                    conn.close() # cerramos la conexion
                except Exception as e:
                    print(f"Error al leer cliente: {e}")

    def obtener_datos_formulario(self):
        # mapeo de los campos del formulario
        # Aqui le estamos diciendo a pycharm, oye en la db se llama de una forma, pero va en el lugar donde esta
        #Creado este frame: ...
        return {
            'tipo_cliente': self.vista.cmb_tipo.get(),
            'nombre_o_razon_social': self.vista.ent_nombre.get().strip(),
            'rut_o_dni': self.vista.ent_rut.get().strip(),
            'direccion_fiscal': self.vista.ent_dir_fiscal.get().strip(),
            'direccion_recogida': self.vista.ent_dir_fiscal.get().strip(),
            'telefono': self.vista.ent_telefono.get().strip(),
            'email': self.vista.ent_email.get().strip(),
            'persona_contacto': self.vista.ent_contacto.get().strip(),
            'termino_pago': "Contado",
            'clasificacion_por_envio': "estándar"
        }

    def cargar_tabla_visual(self):
        # Limpiamos el listbox por completo antes de leer (Read) los clientes en tiempo real
        self.vista.listbox_clientes.delete(0, tk.END)

        if self.vista.db:
            conn = self.vista.db.conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Ejecutamos CRUD select para ver los clientes
                    cursor.execute(
                        "SELECT clienteID, nombre_o_razon_social, rut_o_dni FROM cliente ORDER BY clienteID DESC")
                    filas = cursor.fetchall()
                    for f in filas: # aqui recorremos cada cliente de la db
                        self.vista.listbox_clientes.insert(tk.END, f"{f[0]} | {f[1]} | NIT: {f[2]}")
                    cursor.close()
                    conn.close()
                except Exception as e:
                    print(f"Error al refrescar listbox: {e}")

    # Creamos la funcion para exportar
    def exportar_excel_clientes(self):
        wb = Workbook() # Funcion para crear un libro en excel
        ws = wb.active # Seleccionamos y activamos la primera hoja del libro
        ws.title = "Clientes"
        ws.append(["Clientes logitrans"])
        filtro_tipo = self.vista.cmb_tipo.get()

        # Recorremos cada cliente de la lista para que los muestre
        for i in range(self.vista.listbox_clientes.size()):
            linea = self.vista.listbox_clientes.get(i) # en linea estamos obteniendo los clientes
            ws.append([linea]) # aqui los agregamos al excel

        ruta_archivo = f"Reporte_Clientes_{filtro_tipo}.xlsx" # Generamos el archivo
        wb.save(ruta_archivo) # Guardamos el archivo
        messagebox.showinfo("Realizado", f"¡Excel generado correctamente!\nArchivo: {ruta_archivo}")

    # Generar reporte pdf
    def exportar_pdf_clientes(self):
        filtro_tipo = self.vista.cmb_tipo.get()
        ruta_pdf = f"Reporte_Clientes_{filtro_tipo}.pdf"
        c = canvas.Canvas(ruta_pdf, pagesize=letter) # Aqui cremoas el archivo pdf desde cero

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "Logitrans - Reporte de auditoria de clientes")
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 735, f"Filtro Automático de Cuenta: {filtro_tipo}  |  Auditoría: Jenny Florez")
        c.line(50, 725, 550, 725)
        y = 695
        c.setFont("Helvetica", 10)
        for i in range(self.vista.listbox_clientes.size()):
            linea = self.vista.listbox_clientes.get(i)
            c.drawString(50, y, linea)
            y -= 20
            if y < 50:
                c.showPage()
                y = 700
        c.save()
        messagebox.showinfo("Realizado", f"¡PDF generado con exito!\nArchivo: {ruta_pdf}")

    # Aqui limpiamos formulario
    def limpiar_formulario(self):
        # Reiniciamos el formulario por completo: borramos las cajas,
        # el ID seleccionado y regresamos la foto del camion
        self.vista.cliente_seleccionado_id = None
        self.vista.ent_nombre.delete(0, tk.END)
        self.vista.ent_rut.delete(0, tk.END)
        self.vista.ent_dir_fiscal.delete(0, tk.END)
        self.vista.ent_telefono.delete(0, tk.END)
        self.vista.ent_email.delete(0, tk.END)
        self.vista.ent_contacto.delete(0, tk.END)
        self.vista.cmb_tipo.current(0)
        self.vista.ruta_imagen_cargada = "imagenes/camion_logitrans.png"
        self.actualizar_miniatura_foto(self.vista.ruta_imagen_cargada)
