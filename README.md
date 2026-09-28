# **LOGITRANS**
*Este es el software modular que diseñé en Python para automatizar, controlar y auditar la operación de una empresa de transportes y despachos viales en vivo (CRUD).*

*El sistema está conectado de forma real a una base de datos relacional en MySQL y está estructurado bajo la arquitectura profesional MVC (Modelo,Vista,Controlador). Está dividido en un sistema de carpetas y paquetes independientes para garantizar mantenibilidad y trazabilidad del sistema.*

## **requerimientos**
**Gestión Comercial de Clientes:** CRUD completo (Crear, Leer, Actualizar y Eliminar) conectado a MySQL mediante Stored Procedures. Genera códigos de cliente automáticos y valida que el NIT/Cédula no reciba letras.
**Registro Inteligente de Envíos:** Implementa un calendario interactivo flotante (tkcalendar) para las fechas. Calcula la tarifa real de despacho automáticamente (\$4.000 por Kg base y \$800 extra por Kg si la dimensión pasa de 50x50).
**Control de Flota y Asignaciones:** Vinculación Many-to-Many entre conductores y camiones de la empresa, este modulo tambien contiene la funcion de datetime para recibir el parametro en tiempo real.
**Reporte de Emergencias en Ruta:** Línea crítica para siniestros. Bloquea campos vacíos y despacha alertas con coordenadas GPS calculadas en caliente, tambien cuenta con la funcion datetime.
**Manejo de Imágenes con Pillow:** Cuadros visuales en los formularios que cargan, validan formatos (PNG, JPG, GIF) y redimensionan las fotos viales en limpio.
**Reportes locales:** Todos los módulos exportan datos. Cada pestaña genera reportes tabulares independientes a Excel (openpyxl) y reportes profesionales con formato corporativo a PDF (reportlab) aplicando filtros automáticos.
**Boton de Apariencia Dinámico:** boton en la barra superior para intercambiar la interfaz completa entre Tema Claro y Tema Oscuro.
**Identidad Corporativa:** Ventanas personalizadas con el Favicon oficial de la empresa (imagenes/logitrans_ico.ico).

## **Arquitectura del Sistema (MVC)**
El proyecto se encuentra organizado de la siguiente manera para separar responsabilidades y facilitar el mantenimiento:
*   **`models`**: Contiene la capa de datos y el conector a la base de datos (`conexion.py`).
*   **`views`**: Contiene las interfaces gráficas y layouts modulares de las ventanas creadas con Tkinter.(ej modulo_cliente)
*   **`controllers`**: Contiene los controladores encargados de procesar la operacion, validaciones estrictas y la lógica de los botones.(ej cliente_controller)
*   **`imagenes`**: Contiene la parte grafica del sistema.
*   en la raiz del sistema tenemos el Main, el readme y el script de mysql con el fin de que sea de facil arranque.

## **Herramientas y Librerías Utilizadas**
Para correr este proyecto necesitas tener instalado Python, un motor que permita ejecutar script de bases de datos y las siguientes librerías:
```bash
pip install mysql-connector-python pillow tkcalendar openpyxl reportlab
```

## **Cómo poner a correr el Software**
*Ejecutar el script SQL en MySQL Workbench para levantar las tablas y los Stored Procedures. posteriormente Abrir el proyecto en PyCharm.*

Se puede probar una pantalla sola de forma aislada, en la carpeta **`views`**,clic derecho en run y se puede probar cada archivo independiente (ej. `modulo_cliente.py`).

**Para abrir el sistema unificado completo, dale Run al archivo principal ubicado en la raíz:**
```bash
python main.py
```

    ```
