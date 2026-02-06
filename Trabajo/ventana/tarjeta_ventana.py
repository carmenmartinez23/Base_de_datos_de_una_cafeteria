from customtkinter import *
from tkinter import messagebox, ttk, Frame, Label

from Controlador.Controlador import controlador
from Modelo.Tarjeta import TarjetaFidelidad


class TarjetaVentana:
    def __init__(self, parent):

        self.ventana = CTkToplevel(parent) #Esta ventana depende de Principal
        self.ventana.geometry('1200x600')
        self.ventana.title('Gestión de tarjeta')
        self.ventana.transient(parent)  # La vincula a la ventana principal
        self.ventana.focus_force()  # Fuerza el foco
        self.ventana.lift()   # La trae al frente

        # Cargar Tarjetas de prueba
        self.controlador = controlador

        self.crear_titulo()

        # Cargar los datos en el TreeView
        self.cargar_tarjetas_en_tree()


    #Cargar tarjetas
    def cargar_tarjetas_en_tree(self):
        #Carga todos los tarjetas de la lista al TreeView
        # Limpiar el TreeView primero
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todas las tarjetas
        for tarjeta in self.controlador.tarjeta:
            self.tree.insert('', 'end', values=(
                tarjeta.numero,
                tarjeta.idCliente,
                tarjeta.puntos
            ))

    def crear_titulo(self):
        #-------------- PANEL SUPERIOR ------------------
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(side="top", expand=YES, fill="both")

        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Tarjetas",
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

        # COLUMNA DERECHA - Lista de tarjetas
        self.crear_lista_tarjetas()

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
            text="Datos del Tarjetas",
            font=("Goudy Old Style", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos del formulario
        campos = [
            ("Numero Tarjeta:", "numero_entry"),
            ("idCliente:", None),
            ("puntos:", "puntos_entry")
        ]

        self.entries = {}

        row = 1

        for label, key in campos:
            if key is None:
                # --- Cliente ---
                CTkLabel(
                    self.frame_formulario,
                    text="Cliente:",
                    font=("Goudy Old Style", 18)
                ).grid(row=row, column=0, padx=10, pady=8, sticky="e")
                self.cliente_combo = ttk.Combobox(
                    self.frame_formulario,
                    state="readonly",
                    values=controlador.buscar_clientes(),
                    font=("Goudy Old Style", 16),
                    justify="center",
                )
                self.cliente_combo.grid(row=row, column=1, padx=10, pady=8, sticky="w")
                self.cliente_combo.current(0)
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

    # -------------------- LISTA DE EMPLEADOS -----------------------
    def crear_lista_tarjetas(self):
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título
        CTkLabel(
            self.frame_lista,
            text="Lista de Tarjetas",
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
        columns = ("Numero", "Cliente", "Puntos")
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
        scrollbarx.config(command=self.tree.xview)

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Empaquetar TreeView (al final)
        self.tree.pack(side="left", fill="both", expand=True)

        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_tarjeta)

    def crear_botones(self):
        self.frame_botones = CTkFrame(self.ventana, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        botones = [
            ("Agregar", self.agregar_tarjeta, "Gainsboro"),
            ("Modificar", self.modificar_tarjeta, "Gainsboro"),
            ("Eliminar", self.eliminar_tarjeta, "Gainsboro"),
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


    # -------------------- AGREGAR TARJETA -----------------------
    def agregar_tarjeta(self):
        try:
            # Obtener valores
            tarjeta = TarjetaFidelidad(
                numero=self.entries['numero_entry'].get(),
                idCliente=self.cliente_combo.get(),
                puntos=self.entries['puntos_entry'].get()
            )

            # Validar que no estén vacíos y agregar tarjeta
            if not self.controlador.agregar_tarjeta(tarjeta):
                messagebox.showwarning("Advertencia", "ID, Nombre y Apellido son obligatorios")
                self.ventana.focus_force()
            else:
                # Agregar al treeview
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

    # -------------------- MODIFICAR TARJETA -----------------------
    def modificar_tarjeta(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una tarjeta para modificar")
            self.ventana.focus_force()
            return

        try:
            item = self.tree.item(seleccion[0])
            numero = item['values'][0]

            # Buscar tarjeta en la lista
            for t, tarjeta in enumerate(self.controlador.tarjeta):
                if tarjeta.numero == numero:
                    # Actualizar datos
                    tarjeta.numero = self.entries['numero_entry'].get()
                    tarjeta.idCliente = self.cliente_combo.get()
                    tarjeta.puntos = self.entries['puntos_entry'].get()

                    # Actualizar treeview
                    self.tree.item(seleccion[0], values=(
                        tarjeta.numero,
                        tarjeta.idCliente,
                        tarjeta.puntos
                    ))

                    messagebox.showinfo("Éxito", "Tarjeta modificada correctamente")
                    self.ventana.focus_force()
                    self.limpiar_campos()
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar tarjeta: {str(e)}")
            self.ventana.focus_force()

    # -------------------- ELIMINAR TARJETA -----------------------
    def eliminar_tarjeta(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una tarjeta para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta tarjeta?"):
            try:
                item = self.tree.item(seleccion[0])
                numero = item['values'][0]

                # Eliminar de la lista
                self.controlador.borrar_tarjeta(numero)

                # Eliminar del treeview
                self.tree.delete(seleccion[0])

                messagebox.showinfo("Éxito", "Tarjeta eliminada correctamente")
                self.limpiar_campos()

            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar tarjeta: {str(e)}")

    def seleccionar_tarjeta(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            # Llenar campos
            self.entries['numero_entry'].delete(0, 'end')
            self.entries['numero_entry'].insert(0, valores[0])

            self.cliente_combo.set(valores[1])

            self.entries['puntos_entry'].delete(0, 'end')
            self.entries['puntos_entry'].insert(0, valores[2])

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')

    def salir(self):
        self.ventana.destroy()