from customtkinter import *
from tkinter import messagebox, ttk, Frame, Label
import tkinter.font as tkFont

from Controlador.Controlador import controlador
from Documentos.config import Config
from Modelo.Clientes import Cliente


class ClienteVentana:
    def __init__(self, ventana_principal):
        # Crear ventana secundaria dependiente de la ventana principal
        self.principal = ventana_principal
        self.ventana = CTkToplevel(self.principal)
        self.ventana.geometry('1200x600')  # Tamaño de la ventana
        self.ventana.title('Gestión de Clientes')
        self.ventana.focus_force()  # Fuerza el foco a esta ventana
        self.ventana.lift()  # La trae al frente

        # Controlador que contiene la lista de clientes y demás datos
        self.controlador = controlador

        # Configuracion que contiene funciones para abrir a fullscreen y cerrarlo
        self.configuracion = Config()
        self.configuracion.abrir_fullscreen(self.ventana)

        # Crear título de la ventana
        self.crear_titulo()

        # Cargar los datos de los clientes en el TreeView
        self.cargar_clientes_en_tree()

        self.principal.withdraw()  # oculta la ventana principal

    # -------------------- CARGAR CLIENTES -----------------------
    def cargar_clientes_en_tree(self):
        # Elimina todos los elementos existentes del TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Inserta cada cliente en el TreeView
        for cliente in self.controlador.clientes:
            self.tree.insert('', 'end', values=(
                cliente.idCliente,
                cliente.nombreCliente,
                cliente.apellidoCliente,
                cliente.telefonoCliente,
                cliente.emailCliente,
                cliente.direccionCliente
            ))

        # Ajustar las columnas
        font = tkFont.Font(font=self.configuracion.texto_treeview)

        for col in self.tree["columns"]:
            max_width = font.measure(col + "▼▲")

            for item in self.tree.get_children():
                texto = self.tree.set(item, col)
                max_width = max(max_width, font.measure(texto))

            self.tree.column(col, width=max_width + 20)

    def crear_titulo(self):
        # ---------------- PANEL SUPERIOR ----------------
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(fill="x")

        # Etiqueta del título principal
        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Clientes",
            font=self.configuracion.texto_head,
            fg="white",
            justify="right",
            bg="Sienna")
        self.etiqueta_titulo.pack(side="top", expand=YES)

        # Frame principal dividido en columnas: izquierdo formulario, derecha lista
        self.frame_principal = CTkFrame(self.ventana, fg_color="Sienna", bg_color="Sienna")
        self.frame_principal.pack(fill="both", padx=20, pady=30)

        # Columna izquierda: formulario de cliente
        self.crear_formulario()

        # Columna derecha: lista de clientes
        self.crear_lista_clientes()

    # -------------------- FORMULARIO -----------------------
    def crear_formulario(self):
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Configurar la distribución de columnas
        self.frame_principal.grid_columnconfigure(1, weight=1)

        # Título del formulario
        CTkLabel(
            self.frame_formulario,
            text="Datos del Cliente",
            font=self.configuracion.texto_form_heading
        ).grid(row=0, column=0, columnspan=2, pady=30)

        # Campos del formulario: ID, nombre, apellido, teléfono, email, dirección y pedido
        campos = [
            ("ID Cliente:", "id_entry"),
            ("Nombre:", "nombre_entry"),
            ("Apellido:", "apellido_entry"),
            ("Teléfono:", "telefono_entry"),
            ("Email:", "email_entry"),
            ("Dirección:", "direccion_entry")
        ]

        self.entries = {}  # Diccionario para almacenar los widgets de entrada

        row = 1
        for label, key in campos:
            # Crear etiqueta y entry para los campos de cliente
            CTkLabel(
                self.frame_formulario,
                text=label,
                font=self.configuracion.texto_form
            ).grid(row=row, column=0, padx=15, pady=10, sticky="e")

            entry = CTkEntry(
                self.frame_formulario,
                width=self.configuracion.anchura_entry_form,
                font=self.configuracion.texto_form
            )
            entry.grid(row=row, column=1, padx=10, pady=8, sticky="w")
            self.entries[key] = entry  # Guardar entry en el diccionario

            row += 1
        botones_buscar=[
        ("Buscar por email", self.buscar_email, "Gainsboro"),
        ("Buscar por telefono", self.buscar_telefono, "Gainsboro")
        ]
        frame_botones_buscar=self.configuracion.crear_botones_buscar(self.frame_formulario,botones_buscar)
        frame_botones_buscar.grid(row=9, column=0, columnspan=2, pady=30, sticky="s")

        # -------------------- BOTONES -----------------------
        botones = [
            ("Agregar", self.agregar_cliente, "Gainsboro"),
            ("Modificar", self.modificar_cliente, "Gainsboro"),
            ("Eliminar", self.eliminar_cliente, "Gainsboro"),
            ("Limpiar", self.limpiar_campos, "Gainsboro"),
            ("Salir", self.salir, "Gainsboro")
        ]
        self.frame_botones = self.configuracion.crear_botones(self.ventana, botones)

    # -------------------- LISTA DE CLIENTES -----------------------
    def crear_lista_clientes(self):
        font = tkFont.Font(font=self.configuracion.texto_treeview)

        # Frame contenedor de la lista de clientes
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Estilo para TreeView
        style = ttk.Style()
        style.configure("Treeview",
                        font=self.configuracion.texto_treeview,
                        rowheight=self.configuracion.anchura_linea_treeview,
                        textwrap=1
                        )
        style.configure("Treeview.Heading", font=self.configuracion.texto_treeview)

        # Scrollbars vertical y horizontal
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical", takefocus=True)
        scrollbary.pack(side="right", fill="y")
        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # Configurar columnas del TreeView
        columns = ("ID", "Nombre", "Apellido", "Teléfono", "Email", "Dirección")
        self.tree = ttk.Treeview(
            frame_tree,
            columns=columns,
            show="headings",
            height=18,
            yscrollcommand=scrollbary.set,
            xscrollcommand=scrollbarx.set
        )

        # Asociar scrollbars al TreeView
        scrollbary.config(command=self.tree.yview, orient="vertical")
        scrollbarx.config(command=self.tree.xview, orient="horizontal")

        self.orden_columnas = {}

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col,
                              command=lambda col=col: self.ordenar_columnas(col, False))
            self.tree.column(col, width=100, anchor="center")
            self.orden_columnas[col] = False

        self.tree.pack(side="left", fill="both", expand=True)  # Empaquetar TreeView

        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_cliente)  # Evento de selección

    def ordenar_columnas(self, columna, descendente):
        """
        Ordena el TreeView por la columna especificada.
        Alterna entre orden ascendente y descendente.
        """
        # Obtener todos los datos del TreeView
        datos = [(self.tree.set(item, columna), item) for item in self.tree.get_children('')]

        # Intentar ordenar como números si es posible, sino como texto
        try:
            # Numericamente
            datos.sort(key=lambda x: float(x[0]), reverse=descendente)
        except ValueError:
            # Si falla, ordenar alfabéticamente
            datos.sort(key=lambda x: x[0].lower(), reverse=descendente)

        # Reordenar los items en el TreeView
        for index, (valor, item) in enumerate(datos):
            self.tree.move(item, '', index)

        # Limpiar flechas de todos los encabezados
        for col in self.tree["columns"]:
            # Obtener el texto sin flechas
            texto_limpio = col.replace(" ▲", "").replace(" ▼", "")
            self.tree.heading(col, text=texto_limpio)

        # Agregar flecha al encabezado de la columna ordenada
        flecha = " ▼" if descendente else " ▲"
        self.tree.heading(columna, text=columna + flecha)

        # Alternar el orden para el próximo clic
        self.orden_columnas[columna] = not descendente

        # Actualizar el comando del heading para el próximo clic
        self.tree.heading(
            columna,
            command=lambda: self.ordenar_columnas(columna, self.orden_columnas[columna])
        )

    # -------------------- AGREGAR CLIENTE -----------------------
    def buscar_email(self):
        email = self.entries['email_entry'].get()
        cliente = controlador.buscar_cliente_por_email(email)  # Llamamos al controlador
        if cliente:
            self.limpiar_campos()

            self.entries['id_entry'].insert(0, cliente.idCliente)
            self.entries['nombre_entry'].insert(0, cliente.nombreCliente)
            self.entries['apellido_entry'].insert(0, cliente.apellidoCliente)
            self.entries['email_entry'].insert(0, cliente.emailCliente)
            self.entries['telefono_entry'].insert(0, cliente.telefonoCliente)
            self.entries['direccion_entry'].insert(0, cliente.direccionCliente)

        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún cliente con ese email.")

    def buscar_telefono(self):
        telefono = self.entries['telefono_entry'].get()
        cliente = controlador.buscar_cliente_por_telefono(telefono)  # Llamamos al controlador
        if cliente:
            self.limpiar_campos()

            self.entries['id_entry'].insert(0, cliente.idCliente)
            self.entries['nombre_entry'].insert(0, cliente.nombreCliente)
            self.entries['apellido_entry'].insert(0, cliente.apellidoCliente)
            self.entries['email_entry'].insert(0, cliente.emailCliente)
            self.entries['telefono_entry'].insert(0, cliente.telefonoCliente)
            self.entries['direccion_entry'].insert(0, cliente.direccionCliente)
        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún cliente con ese teléfono.")

    def agregar_cliente(self):
        """Agrega un nuevo cliente al controlador y al TreeView"""
        try:
            # Crear objeto Cliente con los datos del formulario
            cliente = Cliente(
                idCliente=self.entries['id_entry'].get(),
                nombreCliente=self.entries['nombre_entry'].get(),
                apellidoCliente=self.entries['apellido_entry'].get(),
                telefonoCliente=self.entries['telefono_entry'].get(),
                emailCliente=self.entries['email_entry'].get(),
                direccionCliente=self.entries['direccion_entry'].get()
            )
            # Agregar cliente mediante el controlador
            if not self.controlador.agregar_cliente(cliente):
                messagebox.showwarning(
                    "Advertencia",
                    "ID, Nombre y Apellido son obligatorios.\n"
                    "El ID, el teléfono y el email no se pueden repetir"
                )
                self.ventana.focus_force()
            else:
                # Insertar cliente en TreeView
                self.tree.insert('', 'end', values=(
                    cliente.idCliente,
                    cliente.nombreCliente,
                    cliente.apellidoCliente,
                    cliente.telefonoCliente,
                    cliente.emailCliente,
                    cliente.direccionCliente
                ))
                messagebox.showinfo("Éxito",
                                    "Cliente agregado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error al agregar cliente: {str(e)}")
            self.ventana.focus_force()

    # -------------------- MODIFICAR CLIENTE -----------------------
    def modificar_cliente(self):
        """
        Permite modificar el cliente seleccionado en el TreeView.
        Actualiza tanto la lista del controlador como la vista.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia",
                                   "Seleccione un cliente para modificar")
            return

        try:
            item = self.tree.item(seleccion[0])
            idCliente_original = item['values'][0]

            cliente_modificado = Cliente(
                # Actualizar datos desde el formulario
                idCliente=self.entries['id_entry'].get(),
                nombreCliente = self.entries['nombre_entry'].get(),
                apellidoCliente = self.entries['apellido_entry'].get(),
                telefonoCliente = self.entries['telefono_entry'].get(),
                emailCliente = self.entries['email_entry'].get(),
                direccionCliente = self.entries['direccion_entry'].get()
            )

            # Llamar al controlador
            if self.controlador.modificar_cliente(cliente_modificado, idCliente_original):
                # Actualizar TreeView
                self.tree.item(seleccion[0], values=(
                    cliente_modificado.idCliente,
                    cliente_modificado.nombreCliente,
                    cliente_modificado.apellidoCliente,
                    cliente_modificado.telefonoCliente,
                    cliente_modificado.emailCliente,
                    cliente_modificado.direccionCliente
                ))
                messagebox.showinfo("Éxito",
                                    "Cliente modificado correctamente")
                self.limpiar_campos()
                self.ventana.focus_force()
            else:
                messagebox.showwarning(
                    "Advertencia",
                    "ID, Nombre y Apellido son obligatorios.\n"
                    "El ID y el teléfono no se pueden repetir"
                )
                self.ventana.focus_force()

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error al modificar cliente: {e}")
            self.ventana.focus_force()

    # -------------------- ELIMINAR CLIENTE -----------------------
    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia",
                                   "Seleccione un cliente para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar",
                               "¿Está seguro de eliminar este cliente?"):
            try:
                item = self.tree.item(seleccion[0])
                idCliente = item['values'][0]

                # Eliminar de la lista del controlador
                self.controlador.borrar_cliente(idCliente)

                # Elimina del TreeView
                self.tree.delete(seleccion[0])

                messagebox.showinfo("Éxito",
                                    "Cliente eliminado correctamente")
                self.limpiar_campos()

            except Exception as e:
                messagebox.showerror("Error",
                                     f"Error al eliminar cliente: {str(e)}")

    # -------------------- SELECCIONAR CLIENTE -----------------------
    def seleccionar_cliente(self, event):
        # Cuando se selecciona un cliente del TreeView, llenar los campos del formulario
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            self.entries['id_entry'].configure(state="normal")  # por si estaba bloqueado antes
            self.entries['id_entry'].delete(0, 'end')
            self.entries['id_entry'].insert(0, valores[0])
            self.entries['id_entry'].configure(state="disabled")

            self.entries['nombre_entry'].delete(0, 'end')
            self.entries['nombre_entry'].insert(0, valores[1])

            self.entries['apellido_entry'].delete(0, 'end')
            self.entries['apellido_entry'].insert(0, valores[2])

            self.entries['telefono_entry'].delete(0, 'end')
            self.entries['telefono_entry'].insert(0, valores[3])

            self.entries['email_entry'].delete(0, 'end')
            self.entries['email_entry'].insert(0, valores[4])

            self.entries['direccion_entry'].delete(0, 'end')
            self.entries['direccion_entry'].insert(0, valores[5])

    # -------------------- LIMPIAR CAMPOS -----------------------
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries.values():
            entry.delete(0, 'end')

        for key, entry in self.entries.items():
            entry.configure(state="normal")  # habilitar por si estaba bloqueado
            entry.delete(0, 'end')

    # -------------------- SALIR -----------------------
    def salir(self):
        """Cierra la ventana"""
        self.ventana.destroy()
        self.principal.deiconify()
