from customtkinter import *  # Importa todos los widgets de CustomTkinter (CTk, CTkFrame, CTkButton, CTkEntry, etc.)
from tkinter import messagebox, ttk, Frame, Label  # Importa widgets y herramientas de Tkinter
from Controlador.Controlador import controlador  # Importa el controlador de la aplicación (gestiona los datos)
from Documentos.config import Config
from Modelo.Tarjeta import TarjetaFidelidad  # Importa la clase que representa una tarjeta de fidelidad


class TarjetaVentana():
    """Clase que crea y maneja la ventana de gestión de Tarjetas de Fidelidad"""

    def __init__(self, ventana_principal):
        self.principal = ventana_principal
        self.ventana = CTkToplevel()  # Ventana secundaria dependiente de la ventana principal
        self.ventana.title('Gestión de tarjeta')  # Título de la ventana
        self.ventana.focus_force()  # Fuerza que tenga el foco
        self.ventana.lift()  # Trae la ventana al frente

        self.controlador = controlador  # Referencia al controlador para manejar las tarjetas

        # Configuracion que contiene funciones la funcion de abrir a fullscreen y cerrar

        self.configuracion = Config()
        self.configuracion.abrir_fullscreen(self.ventana)

        self.crear_titulo()  # Crea el panel superior y el layout principal
        self.cargar_tarjetas_en_tree()  # Carga los datos iniciales en el TreeView

        self.principal.withdraw() # oculta la ventana principal

    def cargar_tarjetas_en_tree(self):
        """Carga todas las tarjetas en el TreeView"""
        # Limpiar el TreeView antes de cargar
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todas las tarjetas desde el controlador
        for tarjeta in self.controlador.tarjetas:
            self.tree.insert('', 'end', values=(
                tarjeta.numero,
                tarjeta.idCliente,
                tarjeta.puntos
            ))

    def crear_titulo(self):
        """Crea el panel superior, título, layout de columnas y llama a los métodos de formulario, lista y botones"""
        # Panel superior
        self.panel_superior = Frame(self.ventana, bg="Sienna")  # Frame de color Sienna
        self.panel_superior.pack(fill="x")  # Se expande horizontal y verticalmente

        # Etiqueta del título
        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Tarjetas",  # Texto del título
            font=self.configuracion.texto_head,  # Fuente grande
            fg="white",  # Color del texto
            justify="right",  # Justificación a la derecha
            bg="Sienna"  # Fondo igual al panel
        )
        self.etiqueta_titulo.pack(side="top", expand=YES)  # Empaquetar el título

        # Frame principal dividido en dos columnas
        self.frame_principal = CTkFrame(self.ventana, fg_color="Sienna", bg_color="Sienna")
        self.frame_principal.pack(fill="both", padx=20, pady=30)  # Padding alrededor

        self.crear_formulario()  # Columna izquierda: formulario
        self.crear_lista_tarjetas()  # Columna derecha: lista de tarjetas

    def crear_formulario(self):
        """Crea el formulario para agregar o modificar tarjetas"""
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")  # Grid en columna izquierda

        # Configuración de columnas para ajustar tamaños
        self.frame_principal.grid_columnconfigure(1, weight=1)

        # Título del formulario
        CTkLabel(
            self.frame_formulario,
            text="Datos de las Tarjetas",
            font=self.configuracion.texto_form_heading
        ).grid(row=0, column=0, columnspan=2, pady=30)

        # Campos del formulario
        campos = [
            ("Numero Tarjeta:", "numero_entry"),
            ("idCliente:", None),  # Este se maneja con ComboBox
            ("puntos:", "puntos_entry")
        ]

        self.entries = {}  # Diccionario para almacenar los entries

        row = 1
        for label, key in campos:
            if key is None:  # Campo Cliente: ComboBox
                CTkLabel(
                    self.frame_formulario,
                    text="Cliente:",
                    font=self.configuracion.texto_form
                ).grid(row=row, column=0, padx=15, pady=10, sticky="e")

                self.cliente_combo = ttk.Combobox(
                    self.frame_formulario,
                    state="readonly",
                    values=controlador.buscar_clientes(),  # Lista de clientes
                    font=self.configuracion.texto_form_combo,
                    justify="center",
                    width=23
                )
                self.cliente_combo.grid(row=row, column=1, padx=8, pady=8, sticky="w")
            else:  # Campos normales: Entry
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

        # ------------------Campos Buscar-----------------------
            campos_buscar=[
                ("Email:", "email_entry"),
                ("Telefono:", "telefono_entry")
            ]
            self.entries_buscar = {}  # Diccionario para almacenar los entries

            row_b = 4
            for label, key in campos_buscar:
                CTkLabel(
                    self.frame_formulario,
                    text=label,
                    font=self.configuracion.texto_form
                ).grid(row=row_b, column=0, padx=15, pady=10, sticky="e")

                entry = CTkEntry(
                    self.frame_formulario,
                    width=self.configuracion.anchura_entry_form,
                    font=self.configuracion.texto_form
                )
                entry.grid(row=row_b, column=1, padx=10, pady=8, sticky="w")
                CTkLabel(
                    self.frame_formulario,
                    text=label,
                    font=self.configuracion.texto_form
                ).grid(row=row_b, column=0, padx=15, pady=10, sticky="e")
                entry = CTkEntry(
                    self.frame_formulario,
                    width=self.configuracion.anchura_entry_form,
                    font=self.configuracion.texto_form
                )
                entry.grid(row=row_b, column=1, padx=10, pady=8, sticky="w")
                self.entries_buscar[key] = entry  # Guardar entry en el diccionario
                row_b += 1

        botones_buscar=[
            ("Buscar por email", self.buscar_por_email, "Gainsboro"),
            ("Buscar por telefono", self.buscar_por_telefono, "Gainsboro")
            ]
        frame_botones_buscar=self.configuracion.crear_botones_buscar(self.frame_formulario,botones_buscar)
        frame_botones_buscar.grid(row=9, column=0, columnspan=2, pady=1, sticky="s")


    # -------------------- BOTONES -----------------------
        botones = [
            ("Agregar", self.agregar_tarjeta, "Gainsboro"),
            ("Modificar", self.modificar_tarjeta, "Gainsboro"),
            ("Eliminar", self.eliminar_tarjeta, "Gainsboro"),
            ("Limpiar", self.limpiar_campos, "Gainsboro"),
            ("Salir", self.salir, "Gainsboro")
        ]

        self.frame_botones = self.configuracion.crear_botones(self.ventana, botones)


    def obtener_id_cliente_seleccionado(self):
        texto = self.cliente_combo.get()
        id_cliente = int(texto.split("-")[0])
        return id_cliente

# -------------------- LISTA DE TARJETAS -----------------------
    def crear_lista_tarjetas(self):
        """Crea la lista de tarjetas con TreeView y scrollbars"""
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Columna derecha

        # Contenedor para TreeView y Scrollbars
        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Estilo del TreeView
        style = ttk.Style()
        style.configure("Treeview", font=self.configuracion.texto_treeview, rowheight=self.configuracion.anchura_linea_treeview)
        style.configure("Treeview.Heading", font=self.configuracion.texto_treeview)

        # Scrollbars
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical", takefocus=True)
        scrollbary.pack(side="right", fill="y")

        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # TreeView
        columns = ("Numero", "Cliente", "Puntos")
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

        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_tarjeta)  # Evento de selección

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
        for col in self.tree['columns']:
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


    # -------------------- MÉTODOS DE ACCIÓN -----------------------
    def buscar_por_email(self):
        email = self.entries_buscar['email_entry'].get()
        tarjeta = controlador.buscar_tarjeta_por_email(email)  # Llamamos al controlador
        if tarjeta:
            self.entries['numero_entry'].insert(0, tarjeta.numero)
            self.entries['puntos_entry'].insert(0, tarjeta.puntos)
            # Buscar el cliente completo para mostrarlo en el Combobox
            cliente = controlador.buscar_cliente_por_email(email)
            if cliente:
                valor_combo = f"{cliente.idCliente} - {cliente.nombreCliente} {cliente.apellidoCliente}"
                self.cliente_combo.set(valor_combo)
            else:
                self.cliente_combo.set("")
        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún cliente con ese email.")

    def buscar_por_telefono(self):
        telefono = self.entries_buscar['telefono_entry'].get()
        tarjeta = controlador.buscar_tarjeta_por_telefono(telefono)  # Llamamos al controlador
        if tarjeta:
            self.entries['numero_entry'].insert(0, tarjeta.numero)
            self.entries['puntos_entry'].insert(0, tarjeta.puntos)
            # Buscar el cliente completo para mostrarlo en el Combobox
            cliente = controlador.buscar_cliente_por_telefono(telefono)
            if cliente:
                valor_combo = f"{cliente.idCliente} - {cliente.nombreCliente} {cliente.apellidoCliente}"
                self.cliente_combo.set(valor_combo)
            else:
                self.cliente_combo.set("")
        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún cliente con ese teléfono.")


    def agregar_tarjeta(self):
        """Agrega una nueva tarjeta al controlador y al TreeView"""
        try:
            # Crear objeto Tarjeta con los datos del formulario
            tarjeta = TarjetaFidelidad(
                numero=self.entries['numero_entry'].get(),
                idCliente=self.obtener_id_cliente_seleccionado(),
                puntos=self.entries['puntos_entry'].get()
            )
            # Intentar agregar tarjeta mediante el controlador
            if not self.controlador.agregar_tarjeta(tarjeta):
                messagebox.showwarning(
                    "Advertencia",
                    "Numero, Cliente y puntos son obligatorios\n"
                    "Los números de las tarjetas deben ser únicos.\n"
                    "Cada cliente tiene solo una tarjeta."

                                       )
                self.ventana.focus_force()
            else:
                # Insertar tarjeta TreeView
                self.tree.insert('', 'end', values=(
                    tarjeta.numero,
                    tarjeta.idCliente,
                    tarjeta.puntos
                ))
                messagebox.showinfo("Éxito", "Tarjeta agregada correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar tarjeta: {str(e)}")
            print(f"{str(e)}")
            self.ventana.focus_force()

    def modificar_tarjeta(self):
        """Modifica los datos de la tarjeta seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia",
                                   "Seleccione una tarjeta para modificar")
            self.ventana.focus_force()
            return
        try:
            item = self.tree.item(seleccion[0])
            numero_original = str(item['values'][0])

            # Actualizar datos con lo ingresado en formulario
            tarjeta_modificada = TarjetaFidelidad(
                numero = self.entries['numero_entry'].get(),
                idCliente = self.obtener_id_cliente_seleccionado(),
                puntos = self.entries['puntos_entry'].get()
            )
            if self.controlador.modificar_tarjetas(tarjeta_modificada, numero_original):
                # Actualizar Treeview
                self.tree.item(seleccion[0], values=(
                    tarjeta_modificada.numero,
                    tarjeta_modificada.idCliente,
                    tarjeta_modificada.puntos
                ))
                messagebox.showinfo("Éxito",
                                      "Tarjeta modificada correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()

            else:
                messagebox.showwarning("Advertencia",
                                   "Numero, Cliente y puntos son obligatorios\n"
                                   "Los números tienen que ser unicos.\n"
                                   "Cada cliente tiene solo una tarjeta."
                                   )
                self.ventana.focus_force()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al modificar tarjeta: {str(e)}")
            self.ventana.focus_force()

    def eliminar_tarjeta(self):
        """Elimina la tarjeta seleccionada del controlador y del TreeView"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una tarjeta para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta tarjeta?"):
            try:
                item = self.tree.item(seleccion[0])
                numero = item['values'][0]

                self.controlador.borrar_tarjeta(numero)  # Elimina del controlador
                self.tree.delete(seleccion[0])  # Elimina del TreeView
                messagebox.showinfo("Éxito", "Tarjeta eliminada correctamente")
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar tarjeta: {str(e)}")

    def seleccionar_tarjeta(self, event):
        """Llena los campos del formulario con los datos de la tarjeta seleccionada"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            self.entries['numero_entry'].configure(state="normal")  # por si estaba bloqueado antes
            self.entries['numero_entry'].delete(0, 'end')
            self.entries['numero_entry'].insert(0, valores[0])
            self.entries['numero_entry'].configure(state="disabled")

            self.cliente_combo.set(valores[1])

            self.entries['puntos_entry'].delete(0, 'end')
            self.entries['puntos_entry'].insert(0, valores[2])

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries.values():
            entry.delete(0, 'end')

        for cliente in self.cliente_combo.get():
            self.cliente_combo.set("")

        for key, entry in self.entries.items():
            entry.configure(state="normal")  # habilitar por si estaba bloqueado
            entry.delete(0, 'end')

    def salir(self):
        """Cierra la ventana"""
        self.ventana.destroy()
        self.principal.deiconify()

