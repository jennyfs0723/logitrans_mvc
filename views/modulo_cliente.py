import tkinter as tk
from tkinter import ttk
import os
from controllers.cliente_controller import ClienteController

class ModuloCliente:
    # Vamos a diseñar el formulario visual
    def __init__(self, contenedor, conexion_db): # contenedor sera la pantalla donde vamos a poner los datos
        # la conexion es donde vamos a conectarnos con la db
        self.contenedor = contenedor
        self.db = conexion_db
        self.ruta_imagen_cargada = "imagenes/camion_logitrans.png"  # Imagen de la carpeta imagenes
        self.cliente_seleccionado_id = None  # Control interno para la operación de Update,
        # si no es None da un valor
        self.controller = ClienteController(self)
        self.inicializar_componentes() # estamos creando las variables para iniciar rutas y cargar tabla
        self.controller.cargar_tabla_visual()

    def inicializar_componentes(self): # aqui vamos a crear el contenedor de la tabla
        # Creamos el frame
        self.lf_formulario = tk.LabelFrame(self.contenedor, text=" Datos para Creación de Cliente ", padx=15, pady=15,
                                           font=("Arial", 10, "bold"))
        self.lf_formulario.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
        # aqui le decimos que se acomodara a la izquierda, y tendra un tamaño de 10

        # Configuración de los campos
        tk.Label(self.lf_formulario, text="Tipo Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        # Aqui estamos creando un menu desplegable para que seleccione la opcion de tipo de cliente,
        # Facilita el proceso y lo hace mas amigable
        self.cmb_tipo = ttk.Combobox(self.lf_formulario, values=["individual", "empresarial"], width=19,
                                     state="readonly")
        # Aqui le estamos diciendo al sistema que muestre el valor 0 cuando el menu aun no esta desplegado
        self.cmb_tipo.current(0)
        # Aqui vamos a decirle al sistema donde queremos que aparezca el campo
        self.cmb_tipo.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        # label de formulario y entrada con texto para el usuario
        tk.Label(self.lf_formulario, text="Nombre / Empresa:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_nombre = tk.Entry(self.lf_formulario, width=30)
        self.ent_nombre.grid(row=1, column=1, pady=5, padx=5, sticky="w") # Creacion del margenes y posicion

        # Requerimiento, validacion de nit o cedula
        tk.Label(self.lf_formulario, text="Cc / Nit (Solo Números):").grid(row=2, column=0, sticky="w", pady=5)
        #Entrada de texto
        self.ent_rut = tk.Entry(self.lf_formulario, width=22)
        # Tamaño, columna, posicion
        self.ent_rut.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_formulario, text="Dirección Fiscal:").grid(row=3, column=0, sticky="w", pady=5)
        self.ent_dir_fiscal = tk.Entry(self.lf_formulario, width=30)
        self.ent_dir_fiscal.grid(row=3, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_formulario, text="Teléfono:").grid(row=4, column=0, sticky="w", pady=5)
        self.ent_telefono = tk.Entry(self.lf_formulario, width=22)
        self.ent_telefono.grid(row=4, column=1, pady=5, padx=5, sticky="w")

        # Validacion de email con @ y .
        tk.Label(self.lf_formulario, text="Correo Electrónico:").grid(row=5, column=0, sticky="w", pady=5)
        self.ent_email = tk.Entry(self.lf_formulario, width=30)
        self.ent_email.grid(row=5, column=1, pady=5, padx=5, sticky="w")

        tk.Label(self.lf_formulario, text="Persona Contacto:").grid(row=6, column=0, sticky="w", pady=5)
        self.ent_contacto = tk.Entry(self.lf_formulario, width=30)
        self.ent_contacto.grid(row=6, column=1, pady=5, padx=5, sticky="w")

        # aqui entra la gestion de imagenes
        self.frame_foto = tk.Frame(self.lf_formulario, width=110, height=90, relief="groove", borderwidth=2)
        self.frame_foto.grid(row=0, column=2, rowspan=4, padx=15, pady=5)
        self.frame_foto.pack_propagate(False) # para que no se pueda propagar la imagen

        #Aquí metemos una etiqueta limpia dentro del recuadro de la foto, le decimos que se estire para ocupar
        # el espacio que esta disponible y llamamos a la funcion que dibuja la imagen
        self.lbl_foto = tk.Label(self.frame_foto)
        self.lbl_foto.pack(fill="both", expand=True) # para que se expanda por todo el recuadro
        self.controller.actualizar_miniatura_foto(self.ruta_imagen_cargada) # aqui ponemos la imagen que cargamos en el __init__

        # aqui incluimos el boton para gestion de imagenes
        self.btn_cargar_foto = tk.Button(self.lf_formulario, text="Cargar Foto",
                                         command=self.controller.seleccionar_imagen_disco, font=("Arial", 9, "bold"), bg="#95A5A6")
        self.btn_cargar_foto.grid(row=4, column=2, padx=15, sticky="ew")

        # Botones de registrar y actualizar
        self.btn_guardar = tk.Button(
            self.lf_formulario, # llamamos al formulario
            text=" Registrar Cliente",
            command=self.controller.ejecutar_guardado_cliente,
            bg="#27AE60",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_guardar.grid(row=7, column=0, columnspan=2, pady=15, sticky="ew", padx=2)

        # Creacion de boton para actualizar cliente
        self.btn_actualizar = tk.Button(
            self.lf_formulario,
            text="Actualizar Cambios",
            command=self.controller.ejecutar_actualizacion_cliente,
            bg="#D35400",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_actualizar.grid(row=7, column=2, pady=15, sticky="ew", padx=2)

        #exportacion de pdf o excel
        frame_exportar_directo = tk.Frame(self.lf_formulario, pady=5) # llamamos al formulario
        frame_exportar_directo.grid(row=8, column=0, columnspan=3, sticky="ew") # ubicacion en ventana

        # boton exportacion excel
        self.btn_excel = tk.Button(frame_exportar_directo, text="Exportar a Excel",
                                   command=self.controller.exportar_excel_clientes, bg="#1E8449", fg="white",
                                   font=("Arial", 10, "bold"), width=15)
        self.btn_excel.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        # Boton de exportacion pdf
        self.btn_pdf = tk.Button(frame_exportar_directo, text="Exportar a PDF", command=self.controller.exportar_pdf_clientes,
                                 bg="#2471A3", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_pdf.pack(side=tk.LEFT, expand=True, padx=5, fill=tk.X)

        # Visualizacion de datos, estara a la derecha de donde registramos clientes
        self.lf_tabla = tk.LabelFrame(self.contenedor, text=" Clientes en Base de Datos ", padx=10, pady=10,
                                      font=("Arial", 10, "bold"))
        self.lf_tabla.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)
        # Aqui creamos la lista de clientes, por medio de listbox los mostramos hacia abajo
        self.listbox_clientes = tk.Listbox(self.lf_tabla, font=("Courier", 9), selectmode=tk.SINGLE)
        self.listbox_clientes.pack(expand=True, fill="both", pady=5)
        # bind lo usamos para conectar el mouse con la funcion del codigo, en este caso tenemos opciones del CRUD
        self.listbox_clientes.bind("<<ListboxSelect>>", self.controller.cargar_cliente_seleccionado_en_campos)
        # el listboxselect es para unir la seleccion del mouse con la data base

        # Boton para eliminar cliente
        self.btn_eliminar = tk.Button(
            self.lf_tabla,
            text="Eliminar Cliente Seleccionado",
            command=self.controller.ejecutar_eliminacion_cliente, # llamamos al comando para eliminar
            bg="#C0392B",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_eliminar.pack(fill=tk.X, pady=5)

if __name__ == '__main__':
    print("Pruebas")
    root = tk.Tk()
    root.title("Módulo Clientes")
    root.geometry("950x600")

    if os.path.exists("../imagenes/logitrans_ico.ico"): # Aqui es donde esta ubicado el archivo .ico
        root.iconbitmap("../imagenes/logitrans_ico.ico")

    contenedor_prueba = tk.Frame(root)
    contenedor_prueba.pack(fill="both", expand=True)

    app_test = ModuloCliente(contenedor_prueba, conexion_db=None)

    root.mainloop()

