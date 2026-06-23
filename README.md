Sistema de Gestión de Stock e Inventario 

DESCRIPCION DEL PROYECTO:
Este proyecto consiste en el desarrollo de un Sistema de Inventario de Tienda, cuyo objetivo es gestionar productos, categorias y ventas de manera eficiente.

El sistema utiliza un modelo hibrido de bases de datos, combinando una base de datos relacional para la gestion estructurada de los datos y una base de datos no relacional para almacenar los registros historicos del sistema, los dos tipos de bases de datos que usaremos son:
 - SQLite3 para almacenar los datos estructurados del inventario
 - MongoDB para almacenar el historial de movimientos 
La base relacional permite mantener la integridad de los datos y las relaciones entre entidades, mientras que la base no relacional ofrece flexibilidad para almacenar informacion del movimiento del sistema
Nos enfocamos en venta simple - tabla de productos - gestion de usuarios.

OBJETIVOS DEL PROYECTO:
- Gestionar productos y categorias de una tienda
- Registrar ventas realizadas
- Controlar el stock disponible
- Registrar historial de movimientos del inventario
- Aplicar indaxacion para mejorar el rendimiento de consultas
- Realizar respaldo(backup) y restauracion (restore) de la base de datos

TECNOLOGIAS UTILIZADAS:
- Lenguaje: Python 
- Interfaz gráfica: PySide6 (Qt para Python)
- Base de Datos estructurada: SQLite3
- Base de Datos No Relacional: MongoDB
- Conector NoSQL: pymongo

ARQUITECTURA DEL SISTEMA:
El sistema se divide en dos componentes principales: 
Relacional (SQLite3)
 - productos
 - categorias
 - ventas
 - detalle_venta
No Relacional (MongoDB)
 - movimientos_stock
 - logs_sistema
Cada vez que se realiza una operación importante (como una venta o modificación de stock), el sistema registra el cambio tanto en la base relacional como en la base no relacional.

MODELO DE DATOS RELACIONAL:
Tabla: categorias
 - id
 - nombre
Tabla: productos
 - id
 - nombre
 - precio
 - stock
 - categoria_id
Tabla: ventas
 - id
 - fecha
 - total
Tabla: detalle_venta
 - id
 - venta_id
 - producto_id
 - cantidad
 - precio

RELACIONES:
- una categoria puede tener muchos productos
- una venta puede tener muchos productos
- un producto puede aparecer en muchas ventas

ROLES DEL SISTEMA: El sistema cuenta con un control de acceso basado en dos perfiles diferenciados:

1. Administrador (Dueño/Gerente)
Tiene el control total. Su objetivo es gestionar el negocio y ver si es rentable 
- Gestion de usuarios: Puede crear nuevos usuarios (ej: dar de alta a un vendedor nuevo) o despedirlos (borrarlos)
- Control de Inventario: Es el unico que puede modificar el precio de los productos o eliminar articulos del sistema
- Carga de Stock: Recibe la mercaderia de los camiones y actualiza las cantidades
- Reporte de ventas: Puede ver cuanto se vendio en total, que productos se estan agotando y quien es el vendedor que mas factura

2. Vendedor (Empleado de caja)
No puede tocar la configuracion del sistema
- Realizar Ventas: Su pantalla principal es el "punto de venta" (buscar producto, sumar al carrito y cobrar)
- Consultar de Stock: Puede ver si hay un producto, pero no puede cambiar la cantidad manualmente; el stock solo baja cuando hace una venta
- Consulta de Precios: puede ver cuanto cuesta algo, pero no puede editar el precio 
- Perfil Propio: Puede ver sus propias ventas del dia, pero no las de sus compañeros

En resumen: 

1. ADMINISTRADOR:
- Busca productos
- Registrar una venta
- Ver stock actual
- Cambiar precios
- Borrar productos 
- Ver ganacias totales
- Crear otros usuarios

2. VENDEDOR:
- Busca productos
- Registrar una venta
- Ver stock actual

ARQUITECTURA DEL SISTEMA Y CARPETAS:
El proyecto está estructurado de forma modular y organizada en capas independientes para separar la interfaz gráfica de la lógica de datos:

- bases_de_datos: Contiene los archivos físicos de almacenamiento del sistema, como el archivo local de SQLite3 (.db) y scripts iniciales de base de datos.

- model: Capa de Entidades: representa la estructura de los datos del sistema, define Objeto, Producto, Categoría o Venta dentro del código Python.

- data: Capa de Persistencia (Acceso a Datos): contiene los archivos que interactuan directamente con las bases de datos. Se ejecutan las consultas SQL (SQLite3) y las inserciones de documentos de auditoría (MongoDB).

- gui: Capa de Interfaz Gráfica: guarda los archivos visuales generados por pyside6-designer (archivos .ui), los estilos de diseño generales de las pantallas y y la lógica que controla las ventanas de PySide6.

- services: Capa de Lógica de Negocio: es el puente entre las ventanas (gui) y la base de datos (data). Aquí se procesan las reglas del sistema.

- tickets: almacena de forma organizada los archivos de texto, PDFs o comprobantes generados automáticamente por el sistema al concretar una venta.

- venv: carpeta del entorno virtual de python, contiene las librerías aisladas del proyecto.

GUÍA DE INSTALACIÓN Y PASO A PASO: 
Sigan estos pasos detallados para clonar, configurar y ejecutar el proyecto en su entorno local de desarrollo:

Requisitos previos:
1. DB Browser for SQLite (o la extensión SQLite Editor en VS Code) para visualizar la base de datos relacional.
2. MongoDB para interactuar de forma visual con los registros de stock.

Comandos para ejecutar nuestro sistema:

- Ejecutar el siguiente bloque de comandos en su terminal de forma secuencial:

 1. Clonar el repositorio e ingresar a la carpeta del proyecto
git clone <url-del-repositorio>
cd Inventario

2. Crear el entorno virtual 
python -m venv .venv

3. Activar el entorno virtual en Windows (PowerShell)
.venv\Scripts\Activate.ps1

4. Instalar todas las librerías necesarias (PySide6, pymongo, etc.)
pip install -r requirements.txt

5. Ejecutar la aplicación e iniciar el sistema
python app.py

Integrantes: 
* Batista Martina
* Cabeza Florencia
* Guajardo Luana