from Documentos import DatosPrueba

class Controlador:
    def __init__(self):
        self.clientes = DatosPrueba.listadeclientes
        self.tarjeta = DatosPrueba.listadetarjeta
        self.productos = DatosPrueba.listadeproductos
        self.empleados = DatosPrueba.listadeempleados
        self.pedidos = DatosPrueba.listadepedidos

    def buscar_clientes(self):
        return [f"{cliente.idCliente} - {cliente.nombreCliente} {cliente.apellidoCliente}" for cliente in self.clientes]

    def buscar_empleados(self):
         return [f"{empleado.idEmpleado} - {empleado.nombreEmpleado} {empleado.apellidoEmpleado}" for empleado in self.empleados]

    def buscar_pedido(self):
        return [f"{pedido.idPedido} - {pedido.empleado}" for pedido in self.pedidos]

    def seleccionar_categoria(self, categoria):
        valor = 1

        match valor:
            case 1:
                categoria = "Bebida"
            case 2:
                categoria = "Bollería"
            case 3:
                categoria = "Postre"
            case _:
                categoria = "Bebida"

    def borrar_cliente(self, idCliente):
        self.clientes = [c for c in self.clientes if c.idCliente != idCliente]

    def borrar_pedido(self, idPedido):
        self.pedidos = [p for p in self.pedidos if p.idPedido != idPedido]

    def borrar_productos(self, idProducto):
        self.productos = [p for p in self.productos if p.idProducto != idProducto]

    def borrar_empleado(self, idEmpleado):
        self.empleados = [e for e in self.empleados if e.idEmpleado != idEmpleado]

    def borrar_tarjeta(self, numero):
        self.tarjeta = [t for t in self.tarjeta if t.numero != numero]

    def agregar_cliente(self, cliente):
        if cliente.idCliente is None or cliente.idCliente == "":
            return False

        if any(
                campo is None or campo == ""
                for campo in (
                    cliente.idCliente,
                    cliente.nombreCliente,
                    cliente.apellidoCliente
                )
        ):
            return False
        elif any(
                campo == cliente.idCliente
                for campo in (
                    cliente.idCliente
                )
        ):
            return False
        else:
            self.clientes.append(cliente)
            return True

    def agregar_empleado(self, empleado):
        if empleado.idEmpleado is None or empleado.idEmpleado == "":
                return False

        if any(
                campo is None or campo == ""
                for campo in (
                    empleado.idEmpleado,
                    empleado.nombreEmpleado,
                    empleado.apellidoEmpleado
                )
        ):
            return False
        else:
            self.empleados.append(empleado)
            return True

    def agregar_producto(self, producto):
        if producto.idProducto is None or producto.idProducto == "":
            return False

        if any(
                campo is None or campo == ""
                for campo in (
                    producto.idProducto,
                    producto.nombreProducto,
                    producto.categoria,
                    producto.precio,
                    producto.stock
                )
        ):
            return False
        else:
            self.productos.append(producto)
            return True

    def agregar_pedido(self, pedido):
        if pedido.idPedido is None or pedido.idPedido == "":
            return False

        if any(
                campo is None or campo == ""
                for campo in (
                        pedido.idPedido,
                        pedido.numeroMesa,
                        pedido.cliente,
                        pedido.empleado,
                        pedido.fecha
                )
        ):
            return False
        else:
            self.pedidos.append(pedido)
            return True

    def agregar_tarjeta(self, tarjeta):
        if tarjeta.numero is None or tarjeta.numero == "":
            return False

        if any(
                campo is None or campo == ""
                for campo in (
                        tarjeta.numero,
                        tarjeta.puntos
                )
        ):
            return False
        else:
            self.tarjeta.append(tarjeta)
            return True

controlador = Controlador()