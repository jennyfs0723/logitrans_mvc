import tkinter as tk
from tkinter import ttk
import os
from controllers.flota_controller import FlotaController

# Creamos la clase de ModuloFlota
class ModuloFlota:

# inicializamos los atributos
    def __init__(self, contenedor, conexion_db):
        self.contenedor = contenedor # Contenedor, pantalla donde mostramos datos
        self.db = conexion_db # Conexion a la db
        self.controller = FlotaController(self)
        self.inicializar_componentes() # Comando para inicializar los componentes
        self.controller.cargar_tabla_visual() # lo llamamos para cargar tabla
    #Definimos la variable para inicializar componentes
    def inicializar_componentes(self):
        # Creamos el frame izquierdo
        self.lf_flota = tk.LabelFrame(self.contenedor, text=" Asignación de Recursos de Transporte ", padx=15, pady=15,
                                      font=("Arial", 10, "bold"))
        self.lf_flota.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        # Entrada de datos y creacion del lablel
        tk.Label(self.lf_flota, text="ID Vehículo (numero):").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_vehiculo = tk.Entry(self.lf_flota, width=20)
        self.ent_vehiculo.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_flota, text="ID Conductor (Número):").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_conductor = tk.Entry(self.lf_flota, width=20)
        self.ent_conductor.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # Create en la tabla intermedia conductor-vehiculo
        # Creacion de boton
        self.btn_vincular = tk.Button(
            self.lf_flota,
            text="Vincular Conductor y Vehiculo",
            command=self.controller.ejecutar_vinculacion_flota,
            bg="#2980B9",
            fg="white",
            font=("Arial", 10, "bold")
        )
        # darle dimensiones al boton
        self.btn_vincular.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")

        #Creacion de botones para exportar pdf y excel
        frame_exportar_directo = tk.Frame(self.lf_flota, pady=5)
        frame_exportar_directo.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.btn_excel = tk.Button(frame_exportar_directo, text="Exportar a Excel", command=self.controller.exportar_excel_flota,
                                   bg="#1E8449", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_excel.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        self.btn_pdf = tk.Button(frame_exportar_directo, text="Exportar a PDF", command=self.controller.exportar_pdf_flota,
                                 bg="#2471A3", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_pdf.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        # Visualizacion de la tabla en el lado derecho.
        self.lf_tabla = tk.LabelFrame(self.contenedor, text=" Matriz de Asignaciones Activas ", padx=10, pady=10,
                                      font=("Arial", 10, "bold"))
        self.lf_tabla.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        # aqui creamos el espacio para que la union con el mouse suceda
        self.listbox_flota = tk.Listbox(self.lf_tabla, font=("Courier", 9), selectmode=tk.SINGLE)
        self.listbox_flota.pack(expand=True, fill="both", pady=5)


if __name__ == '__main__':
    print("pruebas")
    root = tk.Tk()
    root.title("Módulo Flota")
    root.geometry("950x600")

    if os.path.exists("../imagenes/logitrans_ico.ico"):
        root.iconbitmap("../imagenes/logitrans_ico.ico")

    contenedor_prueba = tk.Frame(root)
    contenedor_prueba.pack(fill="both", expand=True)

    app_test = ModuloFlota(contenedor_prueba, conexion_db=None)

    root.mainloop()

