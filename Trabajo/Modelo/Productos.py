class Producto:
    # Clase que representa un producto disponible en la cafetería.
    def __init__(self, idProducto, nombreProducto, categoria, precio, stock):
        # Constructor que inicializa un producto con sus datos.
        self.idProducto = idProducto      # ID único del producto
        self.nombreProducto = nombreProducto  # Nombre del producto
        self.categoria = categoria        # Categoría del producto (Bebida, Bollería, Postre, etc.)
        self.precio = precio              # Precio del producto
        self.stock = stock                # Stock disponible del producto

    def __str__(self):
        # Método especial que devuelve una representación en cadena del producto.
        # Útil para mostrar en listas o logs.
        return f"{self.nombreProducto} ({self.idProducto})"

    @classmethod
    def cargar_desde_txt(cls, ruta):
        # Método de clase que permite crear objetos Producto desde un archivo de texto.
        # Devuelve una lista de objetos Producto.

        productos = []  # Lista donde se almacenarán los productos cargados

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                # Abrimos el archivo en modo lectura con codificación UTF-8
                for linea in f:
                    # Recorremos cada línea del fichero
                    datos = linea.strip().split(";")  # Eliminamos espacios y separamos los campos por ';'
                    if len(datos) == 5:
                        # Solo procesamos líneas con 5 campos (idProducto, nombreProducto, categoria, precio, stock)
                        producto = cls(*datos)   # Creamos el objeto Producto pasando los datos al constructor
                        productos.append(producto)  # Añadimos el producto a la lista

        except FileNotFoundError:
            # Si no existe el archivo, imprimimos un mensaje de error
            print(f"No se encontró el fichero {ruta}")

        return productos  # Devolvemos la lista de productos creados
