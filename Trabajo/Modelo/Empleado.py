class Empleado:
    # Clase que representa un empleado con sus datos personales, salario y rango laboral.

    def __init__(self, idEmpleado, nombreEmpleado, apellidoEmpleado,
                 telefonoEmpleado, emailEmpleado, direccionEmpleado, salario, rango):
        # Método constructor de la clase Empleado. Recibe todos los atributos necesarios para crear un empleado.
        self.idEmpleado = idEmpleado                  # ID único del empleado
        self.nombreEmpleado = nombreEmpleado          # Nombre del empleado
        self.apellidoEmpleado = apellidoEmpleado      # Apellidos del empleado
        self.telefonoEmpleado = telefonoEmpleado      # Teléfono de contacto
        self.emailEmpleado = emailEmpleado            # Correo electrónico
        self.direccionEmpleado = direccionEmpleado    # Dirección física
        self.salario = salario                        # Salario del empleado
        self.rango = rango                            # Rango o cargo del empleado (Camarero, Encargado, etc.)

    def __str__(self):
        # Método especial que define cómo se representa un objeto Empleado como cadena.
        # Útil para mostrar en listas o logs.
        return f"{self.idEmpleado} - {self.nombreEmpleado} {self.apellidoEmpleado}"

    @classmethod
    def cargar_desde_txt(cls, ruta):
        # Método de clase que permite cargar múltiples empleados desde un fichero de texto.
        # Devuelve una lista de objetos Empleado.

        empleados = []  # Lista donde se guardarán los objetos Empleado

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                # Abrimos el fichero en modo lectura con codificación UTF-8
                for linea in f:
                    # Recorremos línea por línea
                    datos = linea.strip().split(";")  # Eliminamos espacios y separamos por ';'
                    if len(datos) == 8:
                        # Si la línea tiene los 8 campos esperados, creamos un objeto Empleado
                        empleado = cls(*datos)   # *datos pasa los 8 valores al constructor
                        empleados.append(empleado) # Añadimos el empleado a la lista

        except FileNotFoundError:
            # Si no existe el fichero, se muestra un mensaje de error
            print(f"No se encontró el fichero {ruta}")

        return empleados  # Devolvemos la lista de empleados creados
