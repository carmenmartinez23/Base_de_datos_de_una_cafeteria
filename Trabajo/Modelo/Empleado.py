class Empleado:

    def __init__(self, idEmpleado, nombreEmpleado, apellidoEmpleado,
                 telefonoEmpleado, emailEmpleado, direccionEmpleado, salario, rango):
        self.idEmpleado = idEmpleado
        self.nombreEmpleado = nombreEmpleado
        self.apellidoEmpleado = apellidoEmpleado
        self.telefonoEmpleado = telefonoEmpleado
        self.emailEmpleado = emailEmpleado
        self.direccionEmpleado = direccionEmpleado
        self.salario = salario
        self.rango = rango

    def __str__(self):
        return f"{self.idEmpleado} - {self.nombreEmpleado} {self.apellidoEmpleado}"

