class Pedido:

    listadepedidos= []

    def __init__(self, idPedido, numeroMesa, cliente, empleado, fecha, importe):
        self.idPedido = idPedido
        self.numeroMesa = numeroMesa
        self.cliente = cliente
        self.empleado = empleado
        self.fecha = fecha
        self.importe = importe

    def __str__(self):
        return f"{self.idPedido} - {self.empleado}"
