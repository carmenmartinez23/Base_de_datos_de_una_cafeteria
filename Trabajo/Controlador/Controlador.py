from tkinter import messagebox

from Documentos import DatosPrueba
from Documentos.DatosPrueba import listadeclientes, listadeempleados, listadeproductos


# Importa los datos de prueba (listas de clientes, empleados, productos, pedidos y tarjetas)
# desde el módulo 'Documentos/DatosPrueba.py'. Esto se usa para inicializar el controlador
# con datos de ejemplo sin necesidad de acceder a una base de datos.

class Controlador:
    # Clase principal que maneja la lógica de negocio y almacena todas las listas de objetos.

    def __init__(self):
        # Constructor del controlador. Inicializa todas las listas usando los datos de prueba.
        self.clientes = DatosPrueba.listadeclientes
        self.tarjetas = DatosPrueba.listadetarjeta
        self.productos = DatosPrueba.listadeproductos
        self.empleados = DatosPrueba.listadeempleados
        self.pedidos = DatosPrueba.listadepedidos

    # --------------------- CLIENTES ----------------------------
    def agregar_cliente(self, cliente):
        # Agrega un cliente a la lista si cumple ciertas condiciones.
        # Devuelve True si se agrega, False si falla alguna validación.

        # Validación: no puede haber campos vacíos en id, nombre o apellido
        if any(
                campo is None or campo == ""
                for campo in (
                        cliente.idCliente,
                        cliente.nombreCliente,
                        cliente.apellidoCliente
                )
        ):
            return False
        # Validación redundante: comprobar si idCliente ya existe
        # Si otro cliente tiene el mismo ID, email o telefono, error
        for campo in self.clientes:
            if (str(campo.idCliente) == str(cliente.idCliente) or
                campo.emailCliente == cliente.emailCliente or
                campo.telefonoCliente == cliente.telefonoCliente):
                    return False
        else:
            with open("Documentos/clientes.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"{cliente.idCliente};"
                    f"{cliente.nombreCliente};"
                    f"{cliente.apellidoCliente};"
                    f"{cliente.telefonoCliente};"
                    f"{cliente.emailCliente};"
                    f"{cliente.direccionCliente}\n"
                ) # Agrega el cliente a la lista del txt
                self.clientes.append(cliente)
            return True


    def modificar_cliente(self, cliente_modificado, idCliente_original):
        # Validación: campos obligatorios
        if any(
            campo  is None or campo == ""
            for campo in (
               cliente_modificado.idCliente,
               cliente_modificado.nombreCliente,
               cliente_modificado.apellidoCliente
            )
        ):
            return False

        # Validación redundante: comprobar si idCliente ya existe
        for cliente in self.clientes:

            # Si es el cliente que estamos modificando, saltar
            if str(cliente.idCliente) == str(idCliente_original):
                continue

            # Si otro cliente tiene el mismo ID, email o telefono, error
            if (str(cliente.idCliente) == str(cliente_modificado.idCliente) or
                    cliente.emailCliente == cliente_modificado.emailCliente or
                    cliente.telefonoCliente == cliente_modificado.telefonoCliente
            ):
                return False
        try:
            with open("Documentos/clientes.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()

            modificado = False

            with open("Documentos/clientes.txt", "w", encoding="utf-8") as f:
                for linea in lineas:
                    datos = linea.strip().split(";")

                    if datos[0].strip() == str(idCliente_original):
                        f.write(
                            f"{cliente_modificado.idCliente};"
                            f"{cliente_modificado.nombreCliente};"
                            f"{cliente_modificado.apellidoCliente};"
                            f"{cliente_modificado.telefonoCliente};"
                            f"{cliente_modificado.emailCliente};"
                            f"{cliente_modificado.direccionCliente}\n"
                        )
                        modificado = True
                    else:
                        f.write(linea)

            # Actualizar el objeto en la lista de clientes
            for i, cliente in enumerate(self.clientes):
                if str(cliente.idCliente) == str(idCliente_original):
                    self.clientes[i] = cliente_modificado
                    break

            return modificado

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar el cliente: {e}")
            return False

    def buscar_clientes(self):
        # Devuelve una lista de strings con información resumida de los clientes
        # para usar en combos o listados: "ID - Nombre Apellido"
        return [f"{cliente.idCliente} - {cliente.nombreCliente} {cliente.apellidoCliente}" for cliente in self.clientes]

    def buscar_cliente_por_email(self, emailCliente):
        """Busca un cliente por email en la lista"""
        for c in listadeclientes:
            if c.emailCliente == emailCliente:
                return c
        return None

    def buscar_cliente_por_telefono(self, telefonoCliente):
        """Busca un cliente por teléfono en la lista"""
        for c in listadeclientes:
            if c.telefonoCliente == telefonoCliente:
                return c
        return None


    def borrar_cliente(self, idCliente):
        # Elimina un cliente de la lista filtrando por su id
        for i, cliente in enumerate(self.clientes):
            if str(cliente.idCliente).strip() == str(idCliente).strip():
                del self.clientes[i]
                self.guardar_clientes()
                return True
        return False

    def guardar_clientes(self):
        with open("Documentos/clientes.txt", "w", encoding="utf-8") as f:
            for c in self.clientes:
                f.write(
                    f"{c.idCliente};{c.nombreCliente};{c.apellidoCliente};"
                    f"{c.telefonoCliente};{c.emailCliente};"
                    f"{c.direccionCliente};{c.idPedido}\n"
                )
    # --------------------- EMPLEADOS ----------------------------
    def agregar_empleado(self, empleado):
        # Agrega un empleado a la lista si cumple ciertas condiciones.
        # Devuelve True si se agrega, False si falla alguna validación.

        # Agrega un empleado si cumple las validaciones básicas
        if any(
                campo is None or campo == ""
                for campo in (
                        empleado.idEmpleado,
                        empleado.nombreEmpleado,
                        empleado.apellidoEmpleado
                )
        ):
            return False
        for campo in self.empleados:
            if (str(campo.idEmpleado) == str(empleado.idEmpleado) or
                campo.emailEmpleado == empleado.emailEmpleado or
                campo.telefonoEmpleado == empleado.telefonoEmpleado):
                return False
        else:
            with open("Documentos/empleados.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"{empleado.idEmpleado};"
                    f"{empleado.nombreEmpleado};"
                    f"{empleado.apellidoEmpleado};"
                    f"{empleado.telefonoEmpleado};"
                    f"{empleado.emailEmpleado};"
                    f"{empleado.direccionEmpleado};"
                    f"{empleado.salario};"
                    f"{empleado.rango}\n"
                ) # Agrega el empleado a la lista del txt
                self.empleados.append(empleado)
            return True

    def modificar_empleado(self, empleado_modificado, idEmpleado_original):
        # Modifica un empleado si cumple las validaciones básicas
        if any(
            campo is None or campo == ""
           for campo in (
                    empleado_modificado.idEmpleado,
                    empleado_modificado.nombreEmpleado,
                    empleado_modificado.apellidoEmpleado
           )
        ):
            return False

        # Validación redundante: comprobar si idEmpleado ya existe
        for empleado in self.empleados:

            # Si es el empleado que estamos modificando, saltar
            if str(empleado.idEmpleado) == str(idEmpleado_original):
                continue

            # Si otro empleado tiene el mismo ID, email o telefono, error
            if (str(empleado.idEmpleado) == str(empleado_modificado.idEmpleado) or
                    empleado.emailEmpleado == empleado_modificado.emailEmpleado or
                    empleado.telefonoEmpleado == empleado_modificado.telefonoEmpleado
            ):
                return False
        try:
            with open("Documentos/empleados.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()

            modificado = False

            with open("Documentos/empleados.txt", "w", encoding="utf-8") as f:
                for linea in lineas:
                    datos = linea.strip().split(";")

                    if datos[0].strip() == str(idEmpleado_original):
                        f.write(
                            f"{empleado_modificado.idEmpleado};"
                            f"{empleado_modificado.nombreEmpleado};"
                            f"{empleado_modificado.apellidoEmpleado};"
                            f"{empleado_modificado.telefonoEmpleado};"
                            f"{empleado_modificado.emailEmpleado};"
                            f"{empleado_modificado.direccionEmpleado};"
                            f"{empleado_modificado.salario};"
                            f"{empleado_modificado.rango}\n"
                        ) # Modifica el empleado de la lista del txt
                        modificado = True
                    else:
                        f.write(linea)
            # Actualizar el objeto en la lista de empleados
            for i, empleado in enumerate(self.empleados):
                if str(empleado.idEmpleado) == str(idEmpleado_original):
                    self.empleados[i] = empleado_modificado
                    break

            return modificado

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar el empleado: {e}")
            return False

    def buscar_empleados(self):
        # Devuelve un listado de empleados en formato "ID - Nombre Apellido"
        return [f"{empleado.idEmpleado} - {empleado.nombreEmpleado} {empleado.apellidoEmpleado}" for empleado in self.empleados]

    def buscar_empleado_por_email(self, emailEmpleado):
        """Busca un empleado por email en la lista"""
        for e in listadeempleados:
            if e.emailEmpleado == emailEmpleado:
                return e
        return None

    def buscar_empleado_por_telefono(self, telefonoEmpleado):
        """Busca un empleado por teléfono en la lista"""
        for e in listadeempleados:
            if e.telefonoEmpleado == telefonoEmpleado:
                return e
        return None

    def borrar_empleado(self, idEmpleado):
        # Elimina un empleado de la lista filtrando por su id
        for i, empleado in enumerate(self.empleados):
            if str(empleado.idEmpleado).strip() == str(idEmpleado).strip():
                del self.empleados[i]
                self.guardar_empleados()
                return True
        return False

    def guardar_empleados(self):
        with open("Documentos/empleados.txt", "w", encoding="utf-8") as f:
            for e in self.empleados:
                f.write(
                    f"{e.idEmpleado};{e.nombreEmpleado};{e.apellidoEmpleado};"
                    f"{e.telefonoEmpleado};{e.emailEmpleado};"
                    f"{e.direccionEmpleado};{e.salario};{e.rango}\n"
                )
    # --------------------- PRODUCTOS ----------------------------
    def agregar_producto(self, producto):
        # Agrega un producto a la lista si cumple validaciones básicas
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
        # Validar que no exista otro producto con el mismo ID o nombre
        for campo in self.productos:
            if (str(campo.idProducto) == str(producto.idProducto) or
                    campo.nombreProducto == producto.nombreProducto):
                return False
        else:
            with open("Documentos/productos.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"{producto.idProducto};"
                    f"{producto.nombreProducto};"
                    f"{producto.categoria};"
                    f"{producto.precio};"
                    f"{producto.stock}\n"
                ) # Agrega el producto a la lista del txt
                self.productos.append(producto)
            return True

    def modificar_producto(self, producto_modificado, idProducto_original):
        # Modificar un producto de la lista si cumple validaciones básicas

        # Validar que no haya campos vacíos
        if any(
                campo is None or campo == ""
                for campo in (
                        producto_modificado.idProducto,
                        producto_modificado.nombreProducto,
                        producto_modificado.categoria,
                        producto_modificado.precio,
                        producto_modificado.stock
                )
        ):
            return False

        # Validar que no exista OTRO producto con el mismo ID o nombre
        # (excluyendo el que estamos modificando por su ID original)
        for producto in self.productos:
            # Si es el producto que estamos modificando, saltar
            if str(producto.idProducto) == str(idProducto_original):
                continue

            # Si otro producto tiene el mismo ID o nombre, error
            if (str(producto.idProducto) == str(producto_modificado.idProducto) or
                    producto.nombreProducto == producto_modificado.nombreProducto
            ):
                return False
        try:
            with open("Documentos/productos.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()

            modificado = False

            with open("Documentos/productos.txt", "w", encoding="utf-8") as f:
                for linea in lineas:
                    datos = linea.strip().split(";")

                    # Buscar id antes de modificar
                    if datos[0].strip() == str(idProducto_original):
                        f.write(
                            f"{producto_modificado.idProducto};"
                            f"{producto_modificado.nombreProducto};"
                            f"{producto_modificado.categoria};"
                            f"{producto_modificado.precio};"
                            f"{producto_modificado.stock}\n"
                        )
                        modificado = True
                    else:
                        f.write(linea)

            # Actualizar el objeto en la lista de productos
            for i, producto in enumerate(self.productos):
                if str(producto.idProducto) == str(idProducto_original):
                    self.productos[i] = producto_modificado
                    break

            return modificado

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error al modificar el producto: {e}")
            return False

    def seleccionar_categoria(self, categoria):
        # Método para asignar categorías de productos según un valor entero
        categoria = 1

        match categoria:
            case 1:
                categoria = "Bebida"
            case 2:
                categoria = "Bollería"
            case 3:
                categoria = "Postre"
            case _:
                categoria = "Bebida"
        # Nota: actualmente el método no devuelve ni modifica nada fuera de su scope

    def buscar_por_nombre(self, nombreProducto):
        """Busca un producto por su nombre en la lista"""
        for p in listadeproductos:
            if p.nombreProducto == nombreProducto:
                return p
        return None

    def borrar_producto(self, idProducto):
        # Elimina un producto de la lista filtrando por su id
        for i, producto in enumerate(self.productos):
            if str(producto.idProducto).strip() == str(idProducto).strip():
                del self.productos[i]
                self.guardar_productos()
                return True
        return False

    def guardar_productos(self):
        with open("Documentos/productos.txt", "w", encoding="utf-8") as f:
            for p in self.productos:
                f.write(
                    f"{p.idProducto};{p.nombreProducto};{p.categoria};"
                    f"{p.precio};{p.stock}\n"
                )

    # --------------------- PEDIDOS ----------------------------
    def agregar_pedido(self, pedido):
        # Agrega un pedido a la lista si cumple validaciones
        if any(
                campo is None or campo == ""
                for campo in (
                        pedido.idPedido,
                        pedido.importe,
                        pedido.fecha,
                        pedido.cliente,
                        pedido.empleado
                )
        ):
            return False
        if any(
            campo.idPedido == pedido.idPedido
            and campo is not pedido
            for campo in self.pedidos
        ):
            return False
        else:
            with open("Documentos/pedidos.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"{pedido.idPedido};"
                    f"{pedido.numeroMesa};"
                    f"{pedido.cliente};"
                    f"{pedido.empleado};"
                    f"{pedido.fecha};"
                    f"{pedido.importe}\n"
                ) # Agrega el pedido a la lista del txt
                self.pedidos.append(pedido)
            return True

    def modificar_pedido(self, idPedido_original, pedido_modificado):
        # Modifica un pedido de la lista si cumple validaciones
        if any(
                campo is None or campo == ""
                for campo in (
                        pedido_modificado.idPedido,
                        pedido_modificado.numeroMesa,
                        pedido_modificado.importe,
                        pedido_modificado.fecha,
                        pedido_modificado.cliente,
                        pedido_modificado.empleado
                )
        ):
            return False

        # Validación redundante: comprobar si idPedido ya existe
        for pedido in self.pedidos:

            # Si es el pedido que estamos modificando, saltar
            if str(pedido.idPedido) == str(idPedido_original):
                continue

            # Si otro pedido tiene el mismo ID.
            if (str(pedido.idPedido) == str(pedido_modificado.idPedido)
            ):
                return False
        try:
            with open("Documentos/pedidos.txt", "r", encoding="utf-8") as f:
                lineas=f.readlines()

            modificado = False

            with open("Documentos/pedidos.txt", "w", encoding="utf-8") as f:
                for linea in lineas:
                    datos = linea.split(";")

                    if datos[0].strip() == str(idPedido_original):
                        f.write(
                            f"{pedido_modificado.idPedido};"
                            f"{pedido_modificado.numeroMesa};"
                            f"{pedido_modificado.cliente};"
                            f"{pedido_modificado.empleado};"
                            f"{pedido_modificado.fecha};"
                            f"{pedido_modificado.importe}\n"
                        ) # Modifica el pedido de la lista del txt
                        modificado = True
                    else:
                        f.write(linea)
            # Actualizar el objeto en la lista de pedidos
            for i, pedido in enumerate(self.pedidos):
                if str(pedido.idPedido) == str(idPedido_original):
                    self.pedidos[i] = pedido_modificado
                    break

            return modificado

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar el pedido: {e}")

    def buscar_pedido(self):
        # Devuelve lista de pedidos en formato "ID - Empleado"
        return [f"{pedido.idPedido} - {pedido.fecha}" for pedido in self.pedidos]

    def borrar_pedidos(self, idPedido):
        # Elimina un pedido de la lista filtrando por su id
        for i, pedido in enumerate(self.pedidos):
            if str(pedido.idPedido).strip() == str(idPedido).strip():
                del self.pedidos[i]
                self.guardar_pedidos()
                return True
        return False

    def guardar_pedidos(self):
        with open("Documentos/pedidos.txt", "w", encoding="utf-8") as f:
            for p in self.pedidos:
                f.write(
                    f"{p.idPedido};{p.numeroMesa};{p.cliente};"
                    f"{p.empleado};{p.fecha};{p.importe}\n"
                )

    # --------------------- TARJETA ----------------------------
    def agregar_tarjeta(self, tarjeta):
        # Agrega una tarjeta a la lista si cumple ciertas condiciones.
        # Devuelve True si se agrega, False si falla alguna validación.

        # Validación: no puede haber campos vacíos en numero, idCliente o puntos
        if any(
                campo is None or campo == ""
                for campo in (
                        tarjeta.numero,
                        tarjeta.idCliente,
                        tarjeta.puntos
                )
        ):
            return False
        # Validación redundante: comprobar si idCliente ya existe y el número de la tarjeta

        # Validación redundante: comprobar si idCliente ya existe
        # Si otro cliente tiene el mismo ID, email o telefono, error
        for campo in self.tarjetas:
            if (str(campo.numero) == str(tarjeta.numero) or
                    str(campo.idCliente) == str(tarjeta.idCliente)):
                return False
        else:
            with open("Documentos/tarjetas.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"{tarjeta.numero};"
                    f"{tarjeta.idCliente};"
                    f"{tarjeta.puntos}\n"
                ) # Agrega la tarjeta a la lista del txt
                self.tarjetas.append(tarjeta)
            return True


    def modificar_tarjetas(self, tarjeta_modificada, numero_original):
        # Validación: campos obligatorios
        if any(
                campo is None or campo == ""
                for campo in (
                        tarjeta_modificada.numero,
                        tarjeta_modificada.idCliente,
                        tarjeta_modificada.puntos
                )
        ):
            return False

        # Validar que no exista otra tarjeta con el mismo número o idCliente
        # (excluyendo la que estamos modificando por su número original)
        for tarjeta in self.tarjetas:
            # Si es la tarjeta que estamos modificando, saltar
            if str(tarjeta.numero) == str(numero_original):
                continue

            # Si otra tarjeta tiene el mismo número o idCliente, error
            if (str(tarjeta.numero) == str(tarjeta_modificada.numero) or
                    str(tarjeta.idCliente) == str(tarjeta_modificada.idCliente)):
                return False

        try:
            with open("Documentos/tarjetas.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()

            modificado = False

            with open("Documentos/tarjetas.txt", "w", encoding="utf-8") as f:
                for linea in lineas:
                    datos = linea.strip().split(";")  # Añadí .strip() aquí también

                    if datos and datos[0].strip() == str(numero_original):
                        f.write(
                            f"{tarjeta_modificada.numero};"
                            f"{tarjeta_modificada.idCliente};"
                            f"{tarjeta_modificada.puntos}\n"
                        )
                        modificado = True
                    else:
                        f.write(linea)

            # Actualizar el objeto en la lista de tarjetas
            for i, tarjeta in enumerate(self.tarjetas):
                if str(tarjeta.numero) == str(numero_original):
                    self.tarjetas[i] = tarjeta_modificada
                    break

            return modificado

        except Exception as e:
            print(f"Error al modificar la tarjeta: {e}")  # Cambié a print para debugging
            return False

    def borrar_tarjeta(self, numero):
        # Elimina un pedido de la lista filtrando por su id
        for i, tarjeta in enumerate(self.tarjetas):
            if str(tarjeta.numero).strip() == str(numero).strip():
                del self.tarjetas[i]
                self.guardar_tarjetas()
                return True
        return False

    def guardar_tarjetas(self):
        with open("Documentos/tarjetas.txt", "w", encoding="utf-8") as f:
            for t in self.tarjetas:
                f.write(
                    f"{t.numero};{t.idCliente};{t.puntos}\n"
                )

    # -------------------- Buscar tarjeta --------------------
    def buscar_tarjeta_por_id_cliente(self, id_cliente):
        for tarjeta in self.tarjetas:
            if tarjeta.idCliente == id_cliente:
                return tarjeta
        return None

    # -------------------- Buscar tarjeta usando email/telefono --------------------
    def buscar_tarjeta_por_email(self, email):
        cliente = self.buscar_cliente_por_email(email)
        if not cliente:
            return None
        return self.buscar_tarjeta_por_id_cliente(cliente.idCliente)

    def buscar_tarjeta_por_telefono(self, telefono):
        cliente = self.buscar_cliente_por_telefono(telefono)
        if not cliente:
            return None
        return self.buscar_tarjeta_por_id_cliente(cliente.idCliente)


# Instancia global del controlador para que todas las ventanas puedan usarla
controlador = Controlador()