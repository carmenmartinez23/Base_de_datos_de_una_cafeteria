from customtkinter import *
from tkinter import messagebox, ttk, Frame, Label

from Controlador.Controlador import controlador
from Modelo.Clientes import Cliente


class ClienteVentana:
    def __init__(self, parent):
        self.ventana = CTkToplevel(parent) #Esta ventana depende de Principal
        self.ventana.geometry('1200x600')
        self.ventana.title('Gestión de Clientes')
        self.ventana.transient(parent)  # La vincula a la ventana principal
        self.ventana.focus_force()  # Fuerza el foco
        self.ventana.lift()   # La trae al frente

        #cargar lista de clientes de prueba
        self.controlador = controlador

        self.crear_titulo()

        # Cargar los datos en el TreeView
        self.cargar_clientes_en_tree()


# -------------------- CARGAR CLIENTES -----------------------
    def cargar_clientes_en_tree(self):
        # Limpiar el TreeView primero
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todos los clientes
        for cliente in self.controlador.clientes:
            self.tree.insert('', 'end', values=(
                cliente.idCliente,
                cliente.nombreCliente,
                cliente.apellidoCliente,
                cliente.telefonoCliente,
                cliente.emailCliente,
                cliente.direccionCliente,
                cliente.idPedido
            ))

    def crear_titulo(self):
        #-------------- PANEL SUPERIOR ------------------
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(side="top", expand=YES, fill="both")

        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Clientes",
            font=("Britannic Bold", 52),
            fg="white",
            justify="right",
            bg="Sienna")

        self.etiqueta_titulo.pack(side="top", expand=YES, fill="both")

        # Frame principal dividido en dos columnas
        self.frame_principal = CTkFrame(self.ventana, fg_color="Sienna", bg_color="Sienna")
        self.frame_principal.pack(fill="both", padx=20, pady=30)

        # COLUMNA IZQUIERDA - Formulario
        self.crear_formulario()

        # COLUMNA DERECHA - Lista de clientes
        self.crear_lista_clientes()

        # Botones de acción
        self.crear_botones()

# -------------------- FORMULARIO -----------------------
    def crear_formulario(self):
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar grid
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=2)

        # Título del formulario
        CTkLabel(
            self.frame_formulario,
            text="Datos del Cliente",
            font=("Goudy Old Style", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos del formulario
        campos = [
            ("ID Cliente:", "id_entry"),
            ("Nombre:", "nombre_entry"),
            ("Apellido:", "apellido_entry"),
            ("Teléfono:", "telefono_entry"),
            ("Email:", "email_entry"),
            ("Dirección:", "direccion_entry"),
            ("Pedido:", None)
        ]

        self.entries = {}

        row = 1
        for label, key in campos:
            if key is None:
                # --- ID Pedido ---
                CTkLabel(
                    self.frame_formulario,
                    text="Pedido:",
                    font=("Goudy Old Style", 18)
                ).grid(row=row, column=0, padx=10, pady=8, sticky="e")
                self.pedido_combo = ttk.Combobox(
                    self.frame_formulario,
                    state="readonly",
                    values=self.controlador.buscar_pedido(),
                    font=("Goudy Old Style", 16),
                    justify="center"
                )
                self.pedido_combo.grid(row=row, column=1, padx=10, pady=8, sticky="w")
                self.pedido_combo.current(0)
            else:
                CTkLabel(
                    self.frame_formulario,
                    text=label,
                    font=("Goudy Old Style", 18)
                ).grid(row=row, column=0, padx=10, pady=8, sticky="e")

                entry = CTkEntry(
                    self.frame_formulario,
                    width=200,
                    font=("Goudy Old Style", 18)
                )
                entry.grid(row=row, column=1, padx=10, pady=8, sticky="w")
                self.entries[key] = entry

            row += 1

    # -------------------- LISTA DE CLIENTES -----------------------
    def crear_lista_clientes(self):
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título
        CTkLabel(
            self.frame_lista,
            text="Lista de Clientes",
            font=("Goudy Old Style", 20, "bold")
        ).pack(pady=10)
        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame contenedor para TreeView y Scrollbars
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Goudy Old Style", 13), #fuente de las filas
                        rowheight=20,
                        ) #Altura de filas
        style.configure("Treeview.Heading",
                        font=("Goudy Old Style", 13, "bold"))

        # Scrollbars (PRIMERO las scrollbars)
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical", takefocus=True)
        scrollbary.pack(side="right", fill="y")

        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # Treeview nombres
        columns = ("ID",
                   "Nombre",
                   "Apellido",
                   "Teléfono",
                   "Email",
                   "Dirección",
                   "Pedido")
        self.tree = ttk.Treeview(
            frame_tree,
            columns=columns,
            show="headings",
            height=15,
            yscrollcommand=scrollbary.set,
            xscrollcommand=scrollbarx.set
        )

        # Configurar las scrollbars para que controlen el TreeView
        scrollbary.config(command=self.tree.yview, orient="vertical")
        scrollbarx.config(command=self.tree.xview, orient="horizontal")

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Hacer aparecer los datos en el TreeView
        self.tree.pack(side="left", fill="both", expand=True)

        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_cliente)

    def crear_botones(self):
        self.frame_botones = CTkFrame(self.ventana, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        botones = [
            ("Agregar", self.agregar_cliente, "Gainsboro"),
            ("Modificar", self.modificar_cliente, "Gainsboro"),
            ("Eliminar", self.eliminar_cliente, "Gainsboro"),
            ("Limpiar", self.limpiar_campos, "Gainsboro"),
            ("Salir", self.salir, "Gainsboro")
        ]

        for texto, comando, color in botones:
            CTkButton(
                self.frame_botones,
                text=texto,
                command=comando,
                font=("Goudy Old Style", 20, "bold"),
                fg_color="Gainsboro",
                text_color="black",
                hover_color="white",
                border_width=2,
                border_color="Gainsboro",
                width=100,
                height=50,
                corner_radius=32
            ).pack(side="left", padx=5)


# -------------------- AGREGAR CLIENTES -----------------------
    def agregar_cliente(self):
        try:
        # Obtener valores
            cliente = Cliente(
                idCliente=self.entries['id_entry'].get(),
                nombreCliente=self.entries['nombre_entry'].get(),
                apellidoCliente=self.entries['apellido_entry'].get(),
                telefonoCliente=self.entries['telefono_entry'].get(),
                emailCliente=self.entries['email_entry'].get(),
                direccionCliente=self.entries['direccion_entry'].get(),
                idPedido=self.pedido_combo.get()
            )
            # Agregar a la lista y validar que no estén vacíos
            if not self.controlador.agregar_cliente(cliente):
                    messagebox.showwarning("Advertencia", "ID, Nombre y Apellido son obligatorios y el ID no se puede repetir")
                    self.ventana.focus_force()
            else:
                # Agregar al treeview
                self.tree.insert('', 'end', values=(
                    cliente.idCliente,
                    cliente.nombreCliente,
                    cliente.apellidoCliente,
                    cliente.telefonoCliente,
                    cliente.emailCliente,
                    cliente.direccionCliente,
                    cliente.idPedido
                ))

                messagebox.showinfo("Éxito", "Cliente agregado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar cliente: {str(e)}")
            self.ventana.focus_force()

# -------------------- MODIFICAR CLIENTES -----------------------
    def modificar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar")
            self.ventana.focus_force()
            return

        try:
            item = self.tree.item(seleccion[0])
            idCliente = item['values'][0]

            # Buscar cliente en la lista
            for i, cliente in enumerate(self.controlador.clientes):
                if cliente.idCliente == idCliente:
                    # Actualizar datos
                    cliente.nombreCliente = self.entries['nombre_entry'].get()
                    cliente.apellidoCliente = self.entries['apellido_entry'].get()
                    cliente.telefonoCliente = self.entries['telefono_entry'].get()
                    cliente.emailCliente = self.entries['email_entry'].get()
                    cliente.direccionCliente = self.entries['direccion_entry'].get()
                    cliente.idPedido = self.pedido_combo.get()

                    # Actualizar treeview
                    self.tree.item(seleccion[0], values=(
                        cliente.idCliente,
                        cliente.nombreCliente,
                        cliente.apellidoCliente,
                        cliente.telefonoCliente,
                        cliente.emailCliente,
                        cliente.direccionCliente,
                        cliente.idPedido
                    ))

                    messagebox.showinfo("Éxito", "Cliente modificado correctamente")
                    self.ventana.focus_force()
                    self.limpiar_campos()
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar cliente: {str(e)}")
            self.ventana.focus_force()

# -------------------- ELIMINAR CLIENTES -----------------------
    def eliminar_cliente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            try:
                item = self.tree.item(seleccion[0])
                idCliente = item['values'][0]

                # Eliminar de la lista
                self.controlador.borrar_cliente(idCliente)
                self.cargar_clientes_en_tree() #volver a recargar

                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")

            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")

    def seleccionar_cliente(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            # Llenar campos
            self.entries['id_entry'].delete(0, 'end')
            self.entries['id_entry'].insert(0, valores[0])

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

            self.pedido_combo.set(valores[6])

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')

    def salir(self):
        self.ventana.destroy()