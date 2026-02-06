class Cliente:

    def __init__(self, idCliente, nombreCliente, apellidoCliente, telefonoCliente, emailCliente, direccionCliente, idPedido):
        self.idCliente = idCliente
        self.nombreCliente = nombreCliente
        self.apellidoCliente = apellidoCliente
        self.telefonoCliente = telefonoCliente
        self.emailCliente = emailCliente
        self.direccionCliente = direccionCliente
        self.idPedido = idPedido

    def __str__(self):
        return f"{self.idCliente} - {self.nombreCliente} {self.apellidoCliente}"
