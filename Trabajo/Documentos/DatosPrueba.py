from Modelo.Clientes import Cliente
from Modelo.Empleado import Empleado
from Modelo.Pedidos import Pedido
from Modelo.Productos import Producto
from Modelo.Tarjeta import TarjetaFidelidad
# Se importan las clases de los modelos principales.
# Cada clase tiene, además de los atributos de sus objetos,
# un método para cargar datos desde ficheros .txt.

# -------------------- CARGA DE DATOS DESDE FICHEROS --------------------
clientes_prueba = Cliente.cargar_desde_txt("Documentos/clientes.txt")
# Llama al método de clase 'cargar_desde_txt' de Cliente para leer todos los clientes
# desde el fichero 'Documentos/clientes.txt' y devuelve una lista de objetos Cliente.

empleados_prueba = Empleado.cargar_desde_txt("Documentos/empleados.txt")
# Lo mismo para empleados: devuelve una lista de objetos Empleado desde el .txt correspondiente.

productos_prueba = Producto.cargar_desde_txt("Documentos/productos.txt")
# Lee los productos desde el fichero de texto y devuelve una lista de objetos Producto.

tarjetas_prueba = TarjetaFidelidad.cargar_desde_txt("Documentos/tarjetas.txt")
# Lee las tarjetas de fidelidad desde el .txt y devuelve una lista de objetos TarjetaFidelidad.

pedidos_prueba = Pedido.cargar_desde_txt("Documentos/pedidos.txt")
# Lee los pedidos desde el fichero de texto y devuelve una lista de objetos Pedido.

# -------------------- ASIGNACIÓN A LISTAS GLOBALES --------------------
listadeclientes= clientes_prueba
listadeempleados = empleados_prueba
listadeproductos = productos_prueba
listadepedidos = pedidos_prueba
listadetarjeta = tarjetas_prueba
# Estas variables globales almacenan las listas cargadas desde los ficheros,
# y se usan luego para inicializar el controlador o para pruebas.