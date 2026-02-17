class TarjetaFidelidad:
    # Clase que representa una tarjeta de fidelidad asociada a un cliente.

    def __init__(self, numero, idCliente, puntos=0):
        # Constructor que inicializa la tarjeta con su número, cliente y puntos acumulados.
        self.numero = numero          # Número único de la tarjeta
        self.idCliente = idCliente    # Referencia al cliente (puede ser objeto Cliente o solo ID)
        self.puntos = puntos          # Puntos acumulados en la tarjeta, por defecto 0

    @classmethod
    def cargar_desde_txt(cls, ruta):
        # Método de clase para cargar tarjetas desde un archivo de texto.
        # Devuelve una lista de objetos TarjetaFidelidad.

        tarjetas = []  # Lista donde se almacenarán las tarjetas cargadas

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                # Abrimos el archivo en modo lectura con codificación UTF-8
                for linea in f:
                    # Recorremos cada línea del fichero
                    datos = linea.strip().split(";")  # Separamos los campos por ';'
                    if len(datos) == 3:
                        # Solo procesamos líneas con 3 campos (numero, idCliente, puntos)
                        tarjeta = cls(*datos)   # Creamos el objeto TarjetaFidelidad con los datos
                        tarjetas.append(tarjeta)  # Añadimos la tarjeta a la lista

        except FileNotFoundError:
            # Si no se encuentra el archivo, se muestra un mensaje de error
            print(f"No se encontró el fichero {ruta}")

        return tarjetas  # Devolvemos la lista de tarjetas cargadas
