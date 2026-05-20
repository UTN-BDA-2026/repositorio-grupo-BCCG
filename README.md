Sistema de Inventario de Tienda (Inventario)

DESCRIPCION DEL PROYECTO
Este proyecto consiste en el desarrollo de un Sistema de Inventario de Tienda, cuyo objetivo es gestionar productos, categorias y ventas de manera eficiente.

El sistema utiliza un modelo hibrido de bases de datos, combinando una base de datos relacional para la gestion estructurada de los datos y una base de datos no relacional para almacenar los registros historicos del sistema, los dos tipos de bases de datos que usaremos son:
 - SQLite3 para almacenar los datos estructurados del inventario
 - MongoDB para almacenar el historial de movimientos 
La base relacional permite mantener la integridad de los datos y las relaciones entre entidades, mientras que la base no relacional ofrece flexibilidad para almacenar informacion del movimiento del sistema

OBJETIVOS DEL PROYECTO
- Gestionar productos y categorias de una tienda
- Registrar ventas realizadas
- Controlar el stock disponible
- Registrar historial de movimientos del inventario
- Aplicar indaxacion para mejorar el rendimiento de consultas
- Realizar respaldo(backup) y restauracion (restore) de la base de datos

TECNOLOGIAS UTILIZADAS
- Python 
- SQLite3
- MongoDB
- pymongo

ARQUITECTURA DEL SISTEMA 
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

MODELO DE DATOS RELACIONAL
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

RELACIONES 
- una categoria puede tener muchos productos
- una venta puede tener muchos productos
- un producto puede aparecer en muchas ventas

Integrantes: 
* Batista Martina
* Cabeza Florencia
* Carbajal Agustin
* Guajardo Luana


Descargar DB Browser for SQLite para poder visualizar la base de datos relacional o en extensiones buscar SQLlite Editor
Descargar MongoBD Compass 
pip install pymongo en terminal


instalar PySide6 (es parecido a PyQt6 solo que para versiones nuevas de Python)
terminal: pip install PySide6
- para abrir el diseñador desde la terminal 
pyside6-designer

para ingresar al login
te ubicas en el archivo app.py 
en la terminal pones python app.py

en el login poner estos datos 
usuario: admin
contraseña: admin123

cree carpeta data y models
models: representa la estructura de los datos(la entidad)
data: es la capa que habla con la base de datos

Acciones que puede hacer segun el rol:
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
VENDEDOR:
-Busca productos
-Registrar una venta
-Ver stock actual

ADMINISTRADOR:
-Busca productos
-Registrar una venta
-Ver stock actual
-Cambiar precios
- Borrar productos 
- Ver ganacias totales
- Crear otros usuarios


nos enfocamos en venta simple - tabla de productos - gestion de usuarios



