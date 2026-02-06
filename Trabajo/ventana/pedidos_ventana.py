from customtkinter import *
from tkinter import messagebox, ttk, Frame, Label

from Controlador.Controlador import controlador
from Documentos.DatosPrueba import clientes_prueba
from Modelo.Pedidos import Pedido

class PedidoVentana:
    def __init__(self, parent):
        self.ventana = CTkToplevel(parent) #Esta ventana depende de Principal
        self.ventana.geometry('1200x600')
        self.ventana.title('Gestión de Pedidos')
        self.ventana.transient(parent)  # La vincula a la ventana principal
        self.ventana.focus_force()  # Fuerza el foco
        self.ventana.lift()   # La trae al frente

        # Cargar pedidos de prueba
        self.controlador = controlador

        self.crear_titulo()

        # Cargar los datos en el TreeView
        self.cargar_pedidos_en_tree()


    #Cargar pedidos
    def cargar_pedidos_en_tree(self):
        #Carga todos los pedidos de la lista al TreeView
        # Limpiar el TreeView primero
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todos los pedidos
        for pedido in self.controlador.pedidos:
            self.tree.insert('', 'end', values=(
                pedido.idPedido,
                pedido.numeroMesa,
                pedido.fecha,
                pedido.importe,
                pedido.cliente,
                pedido.empleado
            ))

    def crear_titulo(self):
        #-------------- PANEL SUPERIOR ------------------
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(side="top", expand=YES, fill="both")

        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Pedidos",
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

        # COLUMNA DERECHA - Lista de pedidos
        self.crear_lista_pedidos()

        # Botones de acción
        self.crear_botones()

    # -------------------- FORMULARIO -----------------------
    def crear_formulario(self):
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar grid - Estudiar
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=2)

        # Título del formulario
        CTkLabel(
            self.frame_formulario,
            text="Datos del Pedidos",
            font=("Goudy Old Style", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos del formulario
        campos = [
            ("ID Pedido:", "id_entry"),
            ("Numero de mesa:", "numeroMesa_entry"),
            ("Fecha:", "fecha_entry"),
            ("Importe:", "importe_entry")
        ]

        self.entries = {}

        for i, (label_text, entry_name) in enumerate(campos, start=1):
            # Label
            CTkLabel(
                self.frame_formulario,
                text=label_text,
                font=("Goudy Old Style", 18)
            ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

            # Entry
            entry = CTkEntry(
                self.frame_formulario,
                width=200,
                font=("Goudy Old Style", 18)
            )
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")
            self.entries[entry_name] = entry

            # -------- Fila 3: Buscar cliente por id --------
            CTkLabel(self.frame_formulario, text="ID del Cliente:", font=("Goudy Old Style", 18)
                     ).grid(row=5, column=0, padx=10, pady=8, sticky="e")
            self.cliente_combo = ttk.Combobox(
                self.frame_formulario,
                state="readonly",
                values=self.controlador.buscar_clientes(),
                font=("Goudy Old Style", 16))
            self.cliente_combo.grid(row=5, column=1, padx=10, pady=8, sticky="w")

            if self.cliente_combo["values"]:
                self.cliente_combo.current(0)

            # -------- Fila 4: Buscar empleado por id --------
            CTkLabel(self.frame_formulario, text="ID del Empleado:", font=("Goudy Old Style", 18)
                     ).grid(row=6, column=0, padx=10, pady=8, sticky="e")
            self.empleado_combo = ttk.Combobox(
                self.frame_formulario,
                state="readonly",
                values=self.controlador.buscar_empleados(),
                font=("Goudy Old Style", 16))
            self.empleado_combo.grid(row=6, column=1, padx=10, pady=8, sticky="w")

            if self.empleado_combo["values"]:
                self.empleado_combo.current(0)



    # -------------------- LISTA DE EMPLEADOS -----------------------
    def crear_lista_pedidos(self):
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título
        CTkLabel(
            self.frame_lista,
            text="Lista de Pedidos",
            font=("Goudy Old Style", 20, "bold")
        ).pack(pady=10)

        # Frame contenedor para TreeView y Scrollbars
        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame contenedor para TreeView y Scrollbars
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Goudy Old Style", 13), #fuente de las filas
                        rowheight=20) #Altura de filas
        style.configure("Treeview.Heading",
                        font=("Goudy Old Style", 13, "bold"))

        # Scrollbars
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical", takefocus=True)
        scrollbary.pack(side="right", fill="y")

        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # Treeview (DESPUÉS del scrollbar, vinculado a ellas)
        columns = ("ID",
                   "Mesa",
                   "fecha",
                   "Importe",
                   "Cliente",
                   "Empleado"
                   )
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

        # Empaquetar TreeView (al final)
        self.tree.pack(side="left", fill="both", expand=True)

        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_pedido)

    def crear_botones(self):
        self.frame_botones = CTkFrame(self.ventana, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        botones = [
            ("Agregar", self.agregar_pedido, "Gainsboro"),
            ("Modificar", self.modificar_pedido, "Gainsboro"),
            ("Eliminar", self.eliminar_pedido, "Gainsboro"),
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


    # -------------------- AGREGAR EMPLEADOS -----------------------
    def agregar_pedido(self):
        try:
            # Obtener valores
            pedido = Pedido(
                idPedido=self.entries['id_entry'].get(),
                numeroMesa=self.entries['numeroMesa_entry'].get(),
                fecha=self.entries['fecha_entry'].get(),
                importe=self.entries['importe_entry'].get(),
                cliente=self.cliente_combo.get(),
                empleado=self.empleado_combo.get()
            )

            # Validar que no estén vacíos
            if not self.controlador.agregar_pedido(pedido):
                messagebox.showwarning("Advertencia", "Todos los datos son obligatorios")
                self.ventana.focus_force()
                return

            # Agregar al treeview
            self.tree.insert('', 'end', values=(
                pedido.idPedido,
                pedido.numeroMesa,
                pedido.fecha,
                pedido.importe,
                pedido.cliente,
                pedido.empleado
            ))

            messagebox.showinfo("Éxito", "Pedido agregado correctamente")
            self.ventana.focus_force()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar pedido: {str(e)}")
            self.ventana.focus_force()

    # -------------------- MODIFICAR EMPLEADOS -----------------------
    def modificar_pedido(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un pedido para modificar")
            self.ventana.focus_force()
            return

        try:
            item = self.tree.item(seleccion[0])
            idPedido = item['values'][0]

            # Buscar pedido en la lista
            for p, pedido in enumerate(self.controlador.pedidos):
                if pedido.idPedido == idPedido:
                    # Actualizar datos
                    pedido.idPedido = self.entries['id_entry'].get()
                    pedido.numeroMesa = self.entries['numeroMesa_entry'].get()
                    pedido.fecha = self.entries['fecha_entry'].get()
                    pedido.importe = self.entries['importe_entry'].get()
                    pedido.cliente = self.cliente_combo.get()
                    pedido.empleado = self.empleado_combo.get()


                    # Actualizar treeview
                    self.tree.item(seleccion[0], values=(
                        pedido.idPedido,
                        pedido.numeroMesa,
                        pedido.fecha,
                        pedido.importe,
                        pedido.cliente,
                        pedido.empleado
                    ))

                    messagebox.showinfo("Éxito", "Pedido modificado correctamente")
                    self.ventana.focus_force()
                    self.limpiar_campos()
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar pedido: {str(e)}")
            self.ventana.focus_force()

    # -------------------- ELIMINAR EMPLEADOS -----------------------
    def eliminar_pedido(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un pedido para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este pedido?"):
            try:
                item = self.tree.item(seleccion[0])
                idPedido = item['values'][0]

                # Eliminar de la lista
                self.controlador.borrar_pedido(idPedido)

                # Eliminar del treeview
                self.tree.delete(seleccion[0])

                messagebox.showinfo("Éxito", "Pedido eliminado correctamente")
                self.limpiar_campos()

            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar pedido: {str(e)}")

    def seleccionar_pedido(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            # Llenar campos
            self.entries['id_entry'].delete(0, 'end')
            self.entries['id_entry'].insert(0, valores[0])

            self.entries['numeroMesa_entry'].delete(0, 'end')
            self.entries['numeroMesa_entry'].insert(0, valores[1])

            self.entries['fecha_entry'].delete(0, 'end')
            self.entries['fecha_entry'].insert(0, valores[2])

            self.entries['importe_entry'].delete(0, 'end')
            self.entries['importe_entry'].insert(0, valores[3])

            self.cliente_combo.set(valores[4])

            self.empleado_combo.set(valores[5])


    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')

    def salir(self):
        self.ventana.destroy()