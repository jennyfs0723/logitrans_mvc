import tkinter as tk
from tkinter import ttk
import os
from controllers.incidentes_controller import IncidentesController


# Creacion clase ModuloIncidentes
class ModuloIncidentes:
    # Inicializamos variables, creamos contenedor
    def __init__(self, contenedor, conexion_db):
        self.contenedor = contenedor
        self.db = conexion_db
        self.controller = IncidentesController(self)
        self.inicializar_componentes()
        self.controller.cargar_tabla_visual()

    def inicializar_componentes(self):
        # Aqui creamos el marco izquierdo de la ventana
        self.lf_incidentes = tk.LabelFrame(self.contenedor, text=" Reporte de Novedades e Incidentes en Ruta ", padx=15,
                                           pady=15, font=("Arial", 10, "bold"))
        self.lf_incidentes.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        # Campos organizados con .grid() y damos entrada de escritura
        tk.Label(self.lf_incidentes, text="ID Vehículo Afectado (Número):").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_vehiculo_id = tk.Entry(self.lf_incidentes, width=15)
        self.ent_vehiculo_id.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_incidentes, text="ID Conductor (Número):").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_conductor_id = tk.Entry(self.lf_incidentes, width=15)
        self.ent_conductor_id.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        # Aqui es donde ponemos selecciones multiples
        tk.Label(self.lf_incidentes, text="Tipo de Incidente:").grid(row=2, column=0, sticky="w", pady=5)
        self.cmb_tipo_incidente = ttk.Combobox(self.lf_incidentes,
                                               values=["Falla Mecánica", "Pinchazo", "Accidente Vial",
                                                       "Retraso", "Condición Climática", "Otro"], width=22,
                                               state="readonly")
        # Hace que la primera opción de incidente aparezca seleccionada por defecto al abrir el formulario
        self.cmb_tipo_incidente.current(0)
        self.cmb_tipo_incidente.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_incidentes, text="Ubicación (Direccion/Ciudad):").grid(row=3, column=0, sticky="w",
                                                                                        pady=5)
        self.ent_ubicacion = tk.Entry(self.lf_incidentes, width=30)
        self.ent_ubicacion.grid(row=3, column=1, pady=5, padx=5, sticky="w")


        tk.Label(self.lf_incidentes, text="Descripción Detallada:").grid(row=4, column=0, sticky="w", pady=5)
        self.txt_descripcion = tk.Entry(self.lf_incidentes, width=40)
        self.txt_descripcion.grid(row=4, column=1, pady=5, padx=5, sticky="w")

        # Boton de alerta
        self.btn_emitir_alerta = tk.Button(
            self.lf_incidentes,
            text="Emitir reporte de incidente",
            command=self.controller.ejecutar_reporte_incidente,
            bg="#C0392B",
            fg="white",
            font=("Arial", 10, "bold")
        )
        # Publicacion del boton
        self.btn_emitir_alerta.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")

        # Creacion de botones de exportacion pdf y excel
        frame_exportar_directo = tk.Frame(self.lf_incidentes, pady=5)
        frame_exportar_directo.grid(row=6, column=0, columnspan=2, sticky="ew")

        self.btn_excel = tk.Button(frame_exportar_directo, text="Exportar a Excel",
                                   command=self.controller.exportar_excel_incidentes, bg="#1E8449", fg="white",
                                   font=("Arial", 10, "bold"), width=15)
        self.btn_excel.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        self.btn_pdf = tk.Button(frame_exportar_directo, text="Exportar a PDF", command=self.controller.exportar_pdf_incidentes,
                                 bg="#2471A3", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_pdf.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        # Creacion de panel derecho
        self.lf_tabla = tk.LabelFrame(self.contenedor, text=" Registro Histórico de Incidentes ", padx=10, pady=10,
                                      font=("Arial", 10, "bold"))
        self.lf_tabla.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        # aqui creamos el espacio para que la union con el mouse suceda
        self.listbox_incidentes = tk.Listbox(self.lf_tabla, font=("Courier", 9), selectmode=tk.SINGLE)
        self.listbox_incidentes.pack(expand=True, fill="both", pady=5)


if __name__ == '__main__':
    print("pruebas")
    root = tk.Tk()
    root.title("Modulo Incidentes")
    root.geometry("950x600")

    if os.path.exists("../imagenes/logitrans_ico.ico"):
        root.iconbitmap("../imagenes/logitrans_ico.ico")

    contenedor_prueba = tk.Frame(root)
    contenedor_prueba.pack(fill="both", expand=True)

    app_test = ModuloIncidentes(contenedor_prueba, conexion_db=None)

    root.mainloop()

