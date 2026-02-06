class Producto:

    listadeproductos = []

    def __init__(self, idProducto,nombreProducto, categoria, precio, stock):
        self.idProducto = idProducto
        self.nombreProducto = nombreProducto
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"{self.nombreProducto} ({self.idProducto})"
