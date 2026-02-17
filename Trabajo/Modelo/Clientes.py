class Cliente:
    # Clase que representa un cliente con sus datos personales y su pedido asociado.

    def __init__(self, idCliente, nombreCliente, apellidoCliente, telefonoCliente, emailCliente, direccionCliente):
        # Método constructor de la clase Cliente. Recibe todos los atributos necesarios para crear un cliente.
        self.idCliente = idCliente                  # ID único del cliente
        self.nombreCliente = nombreCliente          # Nombre del cliente
        self.apellidoCliente = apellidoCliente      # Apellidos del cliente
        self.telefonoCliente = telefonoCliente      # Teléfono de contacto
        self.emailCliente = emailCliente            # Correo electrónico
        self.direccionCliente = direccionCliente    # Dirección física

    def __str__(self):
        # Método especial que define cómo se representa un objeto Cliente como cadena.
        # Útil para mostrar en listas o logs.
        return f"{self.idCliente} - {self.nombreCliente} {self.apellidoCliente}"

    @classmethod
    def cargar_desde_txt(cls, ruta):
        # Método de clase que permite cargar múltiples clientes desde un fichero de texto.
        # Devuelve una lista de objetos Cliente.

        clientes = []  # Lista donde se guardarán los objetos Cliente

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                # Abrimos el fichero en modo lectura con codificación UTF-8
                for linea in f:
                    # Recorremos línea por línea
                    datos = linea.strip().split(";")  # Eliminamos espacios y separamos por ';'
                    if len(datos) == 6:
                        # Si la línea tiene los 7 campos esperados, creamos un objeto Cliente
                        cliente = cls(*datos)   # *datos pasa los 7 valores al constructor
                        clientes.append(cliente) # Añadimos el cliente a la lista

        except FileNotFoundError:
            # Si no existe el fichero, se muestra un mensaje de error
            print(f"No se encontró el fichero {ruta}")

        return clientes  # Devolvemos la lista de clientes creados
