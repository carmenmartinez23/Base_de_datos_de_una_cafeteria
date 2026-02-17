from customtkinter import *  # Importa CustomTkinter, versión moderna y estilizada de Tkinter
from tkinter import messagebox, ttk, Frame, Label  # Importa elementos básicos de Tkinter
import tkinter.font as tkFont

from Controlador.Controlador import controlador  # Importa tu controlador que maneja la lógica de datos
from Documentos.config import Config
from Modelo.Pedidos import Pedido  # Clase Pedido que representa un pedido


class PedidoVentana:
    def __init__(self, ventana_principal):
        # Crear una ventana hija (CTkToplevel) vinculada a la ventana principal
        self.principal = ventana_principal
        self.ventana = CTkToplevel()
        self.ventana.geometry('1200x600')  # Tamaño de la ventana
        self.ventana.title('Gestión de Pedidos')  # Título de la ventana
        self.ventana.focus_force()  # Fuerza que tenga el foco
        self.ventana.lift()   # La trae al frente

        # Guardar el controlador para manejar pedidos
        self.controlador = controlador

        # Configuracion que contiene funciones la funcion de abrir a fullscreen y cerrar
        self.configuracion = Config()
        self.configuracion.abrir_fullscreen(self.ventana)

        # Crear panel superior con título
        self.crear_titulo()

        # Cargar los pedidos existentes en el TreeView
        self.cargar_pedidos_en_tree()

        self.principal.withdraw() # oculta la ventana principal

    # -------------------- CARGAR PEDIDOS -----------------------
    def cargar_pedidos_en_tree(self):
        # Limpiar el TreeView antes de llenarlo
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todos los pedidos de la lista del controlador
        for pedido in self.controlador.pedidos:
            self.tree.insert('', 'end', values=(
                pedido.idPedido,
                pedido.numeroMesa,
                pedido.importe,
                pedido.fecha,
                pedido.cliente,
                pedido.empleado
            ))

        font = tkFont.Font(font=self.configuracion.texto_treeview)
        for col in self.tree["columns"]:
            max_width = font.measure(col)

            for item in self.tree.get_children():
                texto = self.tree.set(item, col)
                max_width = max(max_width, font.measure(texto))

            self.tree.column(col, width=max_width + 20)

    # -------------------- PANEL SUPERIOR Y PRINCIPAL -----------------------
    def crear_titulo(self):
        # Panel superior con color de fondo
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(fill="x")

        # Etiqueta grande con el título
        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Pedidos",
            font=self.configuracion.texto_head,
            fg="white",
            justify="right",
            bg="Sienna")
        self.etiqueta_titulo.pack(side="top", expand=YES)

        # Frame principal donde van formulario y TreeView
        self.frame_principal = CTkFrame(self.ventana, fg_color="Sienna", bg_color="Sienna")
        self.frame_principal.pack(fill="both", padx=20, pady=30)

        # Crear columna izquierda (formulario)
        self.crear_formulario()

        # Crear columna derecha (lista de pedidos)
        self.crear_lista_pedidos()


    # -------------------- FORMULARIO -----------------------
    def crear_formulario(self):
        # Frame donde estarán los campos
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Configuración del grid del frame principal
        self.frame_principal.grid_columnconfigure(1, weight=1)

        # Título del formulario
        CTkLabel(
            self.frame_formulario,
            text="Datos del Pedidos",
            font=self.configuracion.texto_form_heading
        ).grid(row=0, column=0, columnspan=2, pady=30)

        # Campos del formulario con sus nombres para acceder después
        campos = [
            ("ID Pedido:", "id_entry"),
            ("Numero de mesa:", "numeroMesa_entry"),
            ("Importe:", "importe_entry")
        ]
        self.entries = {}

        for i, (label_text, entry_name) in enumerate(campos, start=1):
                # Crear cada Label y Entry
            CTkLabel(
                self.frame_formulario,
                text=label_text,
                font=self.configuracion.texto_form
            ).grid(row=i, column=0, padx=15, pady=10, sticky="e")
            entry = CTkEntry(
                self.frame_formulario,
                width=self.configuracion.anchura_entry_form,
                font=self.configuracion.texto_form
            )
            entry.grid(row=i, column=1, padx=8, pady=8, sticky="w")
            self.entries[entry_name] = entry

        # Calendario para seleccionar fecha
        CTkLabel(self.frame_formulario, text="Fecha:", font=self.configuracion.texto_form
                 ).grid(row=4, column=0, padx=15, pady=10, sticky="e")
        self.fecha_entry = self.configuracion.crear_calendario(self.frame_formulario)

        # Combobox para seleccionar cliente
        CTkLabel(self.frame_formulario, text="ID del Cliente:", font=self.configuracion.texto_form
                 ).grid(row=5, column=0, padx=15, pady=10, sticky="e")
        self.cliente_combo = ttk.Combobox(
            self.frame_formulario,
            values=self.controlador.buscar_clientes(),
            font=self.configuracion.texto_form_combo,
            width=23
        )

        self.cliente_combo.grid(row=5, column=1, padx=10, pady=8, sticky="w")

        # Combobox para seleccionar empleado
        CTkLabel(self.frame_formulario, text="ID del Empleado:", font=self.configuracion.texto_form
                 ).grid(row=6, column=0, padx=15, pady=8, sticky="e")

        self.empleado_combo = ttk.Combobox(
            self.frame_formulario,
            state="normal",
            values=self.controlador.buscar_empleados(),
            font=self.configuracion.texto_form_combo,
            width=23)

        self.empleado_combo.grid(row=6, column=1, padx=10, pady=8, sticky="w")

        # -------------------- BOTONES -----------------------
        botones = [
            ("Agregar", self.agregar_pedido, "Gainsboro"),
            ("Modificar", self.modificar_pedido, "Gainsboro"),
            ("Eliminar", self.eliminar_pedido, "Gainsboro"),
            ("Limpiar", self.limpiar_campos, "Gainsboro"),
            ("Salir", self.salir, "Gainsboro")
        ]
        self.frame_botones = self.configuracion.crear_botones(self.ventana, botones)

    def obtener_id_empleado_seleccionado(self):
        texto = self.empleado_combo.get()
        id_empleado = int(texto.split("-")[0].strip())
        return id_empleado

    def obtener_id_cliente_seleccionado(self):
        texto = self.cliente_combo.get()
        id_cliente = int(texto.split("-")[0].strip())
        return id_cliente


    # -------------------- TREEVIEW (LISTA DE PEDIDOS) -----------------------
    def crear_lista_pedidos(self):
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Frame contenedor para TreeView y scrollbars
        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview",
                        font=self.configuracion.texto_treeview,
                        rowheight=self.configuracion.anchura_linea_treeview)
        style.configure("Treeview.Heading", font=self.configuracion.texto_treeview)

        # Scrollbars
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical", takefocus=True)
        scrollbary.pack(side="right", fill="y")
        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # Treeview para mostrar los pedidos
        columns = ("ID", "Mesa", "Importe", "Fecha", "Cliente", "Empleado")
        self.tree = ttk.Treeview(
            frame_tree,
            columns=columns,
            show="headings",
            height=18,
            yscrollcommand=scrollbary.set,
            xscrollcommand=scrollbarx.set
        )
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

        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_pedido)  # Evento de selección

    def ordenar_columnas(self, columna, descendente):
        """
        Ordena el TreeView por la columna especificada.
        Alterna entre orden ascendente y descendente.
        """
        # Obtener todos los datos del TreeView
        datos = [(self.tree.set(item, columna), item) for item in self.tree.get_children('')]

        # Intentar ordenar como números si es posible, sino como texto
        try:
            #Numericamente
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

    # -------------------- MÉTODOS CRUD -----------------------
    def agregar_pedido(self):
        # self.cargar_pedidos_en_tree()
        """
        Toma los datos del formulario, crea un pedido y lo agrega a la lista y TreeView.
        Valida que no haya campos vacíos usando el controlador.
        """
        try:
            pedido = Pedido(
                idPedido=self.entries['id_entry'].get(),
                numeroMesa=self.entries['numeroMesa_entry'].get(),
                importe=self.entries['importe_entry'].get(),
                fecha=self.fecha_entry.get(),
                cliente=self.obtener_id_cliente_seleccionado(),
                empleado=self.obtener_id_empleado_seleccionado()
            )

            if not self.controlador.agregar_pedido(pedido):
                messagebox.showwarning(
                    "Advertencia",
                    "ID, Importe, Fecha, cliente y empleado son obligatorios.\n"
                            "El ID debe ser único."
                                       )
                self.ventana.focus_force()
            else:
                self.tree.insert('', 'end', values=(
                    pedido.idPedido,
                    pedido.numeroMesa,
                    pedido.importe,
                    pedido.fecha,
                    pedido.cliente,
                    pedido.empleado
                ))
                messagebox.showinfo("Éxito", "Pedido agregado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar pedido: {str(e)}")
            self.ventana.focus_force()


    def modificar_pedido(self):
        """
        Permite modificar el pedido seleccionado en el TreeView.
        Actualiza tanto la lista del controlador como la vista.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia",
                                   "Seleccione un pedido para modificar")
            self.ventana.focus_force()
            return

        try:
            item = self.tree.item(seleccion[0])
            idPedido_original = item['values'][0]

            pedido_modificado = Pedido(
                # Actualizar datos
                idPedido = self.entries['id_entry'].get(),
                numeroMesa = self.entries['numeroMesa_entry'].get(),
                importe = self.entries['importe_entry'].get(),
                fecha = self.fecha_entry.get(),
                cliente = self.obtener_id_cliente_seleccionado(),
                empleado = self.obtener_id_empleado_seleccionado()
            )
            if not self.controlador.modificar_pedido(idPedido_original, pedido_modificado):
                messagebox.showwarning(
                    "Advertencia",
                    "ID, Importe, Fecha, cliente y empleado son obligatorios.\n"
                    "El ID debe ser único."
                )
                return

            # Actualizar TreeView
            self.tree.item(seleccion[0], values=(
                pedido_modificado.idPedido,
                pedido_modificado.numeroMesa,
                pedido_modificado.importe,
                pedido_modificado.fecha,
                pedido_modificado.cliente,
                pedido_modificado.empleado
            ))

            messagebox.showinfo("Éxito",
                                "Pedido modificado correctamente")
            self.ventana.focus_force()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error al modificar pedido: {str(e)}")
            self.ventana.focus_force()


    def eliminar_pedido(self):
        """
        Elimina el pedido seleccionado después de confirmar.
        Borra de la lista del controlador y del TreeView.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia",
                                   "Seleccione un pedido para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar",
                               "¿Está seguro de eliminar este pedido?"):
            try:
                item = self.tree.item(seleccion[0])
                idPedido = item['values'][0]

                # Eliminar del controlador
                self.controlador.borrar_pedidos(idPedido)

                # Eliminar del TreeView
                self.tree.delete(seleccion[0])

                messagebox.showinfo("Éxito",
                                    "Pedido eliminado correctamente")
                self.limpiar_campos()

            except Exception as e:
                messagebox.showerror("Error",
                                     f"Error al eliminar pedido: {str(e)}")


    def seleccionar_pedido(self, event):
        """
        Cuando se selecciona un pedido en el TreeView, llena los campos del formulario con sus datos.
        """
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            self.entries['id_entry'].configure(state="normal")  # por si estaba bloqueado antes
            self.entries['id_entry'].delete(0, 'end')
            self.entries['id_entry'].insert(0, valores[0])
            self.entries['id_entry'].configure(state="disabled")

            self.entries['numeroMesa_entry'].delete(0, 'end')
            self.entries['numeroMesa_entry'].insert(0, valores[1])

            self.entries['importe_entry'].delete(0, 'end')
            self.entries['importe_entry'].insert(0, valores[2])

            self.fecha_entry.set_date(valores[3])

            self.cliente_combo.set(valores[4])

            self.empleado_combo.set(valores[5])


    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries.values():
            entry.delete(0, 'end')

        for key, entry in self.entries.items():
            entry.configure(state="normal")  # habilitar por si estaba bloqueado
            entry.delete(0, 'end')

        for cliente in self.cliente_combo.get():
            self.cliente_combo.set("")

        for empleado in self.empleado_combo.get():
            self.empleado_combo.set("")
    def salir(self):
        """Cierra la ventana y vuelve a mostrar la principal"""
        self.ventana.destroy()
        self.principal.deiconify()

