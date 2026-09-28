import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import os
from controllers.envios_controller import EnviosController

# Creacion de la clase ModuloEnvios
class ModuloEnvios:

    # Inicializamos variables, creamos contenedor
    def __init__(self, contenedor, conexion_db):
        self.contenedor = contenedor
        self.db = conexion_db
        self.ruta_foto_guia = "imagenes/camion_logitrans.png"  # Imagen de la carpeta de imagenes
        self.controller = EnviosController(self)
        self.inicializar_componentes()
        self.controller.cargar_tabla_visual()

    def inicializar_componentes(self):
        # Formulario izquierdo
        self.lf_envio = tk.LabelFrame(self.contenedor, text=" Datos para generar la Guía de Distribución ", padx=15,
                                      pady=15, font=("Arial", 10, "bold"))
        self.lf_envio.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        # Implementacion de tkcalendar, entregamos la fecha exactamente como esta estipulada segun date_pattern
        tk.Label(self.lf_envio, text="Fecha Recepción:").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_fecha = DateEntry(self.lf_envio, width=19, background='darkblue', foreground='white', borderwidth=2,
                                   date_pattern='yyyy-mm-dd')
        self.ent_fecha.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_envio, text="ID Cliente (Número):").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_id_cliente = tk.Entry(self.lf_envio, width=15)
        self.ent_id_cliente.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_envio, text="Remitente:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_remitente = tk.Entry(self.lf_envio, width=25)
        self.ent_remitente.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_envio, text="Destinatario:").grid(row=3, column=0, sticky="w", pady=5)
        self.ent_destinatario = tk.Entry(self.lf_envio, width=25)
        self.ent_destinatario.grid(row=3, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_envio, text="Dirección Origen:").grid(row=4, column=0, sticky="w", pady=5)
        self.ent_origen = tk.Entry(self.lf_envio, width=30)
        self.ent_origen.grid(row=4, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_envio, text="Dirección Destino:").grid(row=5, column=0, sticky="w", pady=5)
        self.ent_destino = tk.Entry(self.lf_envio, width=30)
        self.ent_destino.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        # Lista despleglable
        tk.Label(self.lf_envio, text="Tipo Servicio:").grid(row=6, column=0, sticky="w", pady=5)
        self.cmb_servicio = ttk.Combobox(self.lf_envio, values=["normal", "express", "mismo dia"], width=19,
                                         state="readonly")
        # Hace que la primera opción de incidente aparezca seleccionada por defecto al abrir el formulario
        self.cmb_servicio.current(0)
        self.cmb_servicio.grid(row=6, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_envio, text="Peso Declarado (Kg):").grid(row=7, column=0, sticky="w", pady=5)
        self.ent_peso = tk.Entry(self.lf_envio, width=15)
        self.ent_peso.grid(row=7, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_envio, text="Dimensiones (Alto x Ancho):").grid(row=8, column=0, sticky="w", pady=5)
        self.ent_dimensiones = tk.Entry(self.lf_envio, width=22)
        self.ent_dimensiones.grid(row=8, column=1, pady=5, padx=5, sticky="w")

        # Valor estimado del producto segun cliente
        tk.Label(self.lf_envio, text="Valor Estimado ($):").grid(row=9, column=0, sticky="w", pady=5)
        self.ent_costo = tk.Entry(self.lf_envio, width=15)
        self.ent_costo.grid(row=9, column=1, pady=5, padx=5, sticky="w")

        # Forma de pago
        tk.Label(self.lf_envio, text="Forma de pago:"). grid(row=10, column=0, sticky="w", pady=5)
        self.cmb_pago = ttk.Combobox(self.lf_envio, values=["Efectivo", "Tarjeta", "Transferencia"],
                                     width=19,state="readonly")
        self.cmb_pago.current(0)
        self.cmb_pago.grid(row=10, column=1, pady=5, padx=5, sticky="w")

        # Instrucciones NO obligatorias
        tk.Label(self.lf_envio, text="Instrucciones especiales").grid(row=11, column=0, sticky="w", pady=5)
        self.ent_instrucciones = tk.Entry(self.lf_envio,width=22)
        self.ent_instrucciones.grid(row=11, column=1, pady=5, padx=5, sticky="w")

        # Creacion del frame donde ira la imagen
        self.frame_guia_img = tk.Frame(self.lf_envio, width=110, height=90, relief="groove", borderwidth=2)
        self.frame_guia_img.grid(row=0, column=2, rowspan=4, padx=15, pady=5)
        self.frame_guia_img.pack_propagate(False)

        # Etiqueta interna donde ponemos que ocupe todo el espacio
        self.lbl_foto_guia = tk.Label(self.frame_guia_img)
        self.lbl_foto_guia.pack(fill="both", expand=True)
        self.controller.cargar_miniatura_pillow(self.ruta_foto_guia)

        # Creacion de boton para cargar imagen
        self.btn_cargar_img = tk.Button(self.lf_envio, text="Cargar Foto", command=self.controller.buscar_imagen_disco,
                                        font=("Arial", 9, "bold"), bg="#95A5A6")
        self.btn_cargar_img.grid(row=4, column=2, padx=15, sticky="ew")

        # Creacion de boton para guardar guia
        self.btn_guardar_guia = tk.Button(
            self.lf_envio,
            text="Generar Guía de Envío",
            command=self.controller.registrar_orden_despacho,
            bg="#27AE60",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_guardar_guia.grid(row=12, column=0, columnspan=3, pady=15, sticky="ew")

        # Creacion de botones de exportacion
        frame_exportar_directo = tk.Frame(self.lf_envio, pady=5)
        frame_exportar_directo.grid(row=13, column=0, columnspan=3, sticky="ew")

        self.btn_excel = tk.Button(frame_exportar_directo, text="Exportar a Excel", command=self.controller.compilar_reporte_excel, bg="#1E8449", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_excel.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        self.btn_pdf = tk.Button(frame_exportar_directo, text="Exportar a PDF", command=self.controller.compilar_reporte_pdf, bg="#2471A3", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_pdf.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        # Frame derecho
        self.lf_tabla = tk.LabelFrame(self.contenedor, text=" Envíos Activos en Sistema ", padx=10, pady=10, font=("Arial", 10, "bold"))
        self.lf_tabla.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        # aqui creamos el espacio para que la union con el mouse suceda
        self.listbox_envios = tk.Listbox(self.lf_tabla, font=("Courier", 9), selectmode=tk.SINGLE)
        self.listbox_envios.pack(expand=True, fill="both", pady=5)


if __name__ == '__main__':
    print("Pruebas")
    root = tk.Tk()
    root.title("Módulo Envíos")
    root.geometry("950x600")
    if os.path.exists("../imagenes/logitrans_ico.ico"):
        root.iconbitmap("../imagenes/logitrans_ico.ico")
    contenedor_prueba = tk.Frame(root)
    contenedor_prueba.pack(fill="both", expand=True)
    app_test = ModuloEnvios(contenedor_prueba, conexion_db=None)
    root.mainloop()


