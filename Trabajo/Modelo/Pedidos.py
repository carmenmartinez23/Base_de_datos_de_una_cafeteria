class Pedido:
    # Clase que representa un pedido realizado en la cafetería.

    listadepedidos = []
    # Lista estática que podría usarse para almacenar todos los pedidos creados (no es estrictamente necesaria si usamos cargar desde txt).

    def __init__(self, idPedido, numeroMesa, cliente, empleado, fecha, importe):
        # Constructor que inicializa los datos de un pedido.
        self.idPedido = idPedido      # ID único del pedido
        self.numeroMesa = numeroMesa  # Número de la mesa asociada al pedido
        self.cliente = cliente        # Cliente que realiza el pedido
        self.empleado = empleado      # Empleado que toma el pedido
        self.fecha = fecha            # Fecha del pedido
        self.importe = importe        # Importe total del pedido

    def __str__(self):
        # Método especial que devuelve una representación en cadena del pedido.
        # Útil para mostrar en listas o logs.
        return f"{self.idPedido} - {self.empleado} - {self.fecha} - {self.importe}"

    @classmethod
    def cargar_desde_txt(cls, ruta):
        # Método de clase que permite crear objetos Pedido desde un archivo de texto.
        # Devuelve una lista de objetos Pedido.

        pedidos = []  # Lista donde se almacenarán los pedidos cargados

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                # Abrimos el archivo en modo lectura con codificación UTF-8
                for linea in f:
                    # Recorremos cada línea del fichero
                    datos = linea.strip().split(";")  # Eliminamos espacios y separamos los campos por ';'
                    if len(datos) == 6:
                        # Solo procesamos líneas con 6 campos (idPedido, numeroMesa, cliente, empleado, fecha, importe)
                        pedido = cls(*datos)  # Creamos el objeto Pedido pasando los datos al constructor
                        pedidos.append(pedido) # Añadimos el pedido a la lista

        except FileNotFoundError:
            # Si no existe el archivo, imprimimos un mensaje de error
            print(f"No se encontró el fichero {ruta}")

        return pedidos  # Devolvemos la lista de pedidos creados
