from customtkinter import *  # Importa todos los widgets de CustomTkinter (CTk, CTkFrame, CTkButton, CTkEntry, etc.)
from tkinter import messagebox, ttk, Frame, Label  # Importa widgets y herramientas de Tkinter
from Controlador.Controlador import controlador  # Importa el controlador de la aplicación (gestiona los datos)
from Documentos.config import Config
from Modelo.Productos import Producto  # Importa la clase que representa un producto


class ProductoVentana:
    """Clase que crea y maneja la ventana de gestión de productos"""

    def __init__(self, ventana_principal):
        self.ventana = CTkToplevel()  # Ventana secundaria dependiente de la ventana principal
        self.ventana.geometry('1200x600')  # Tamaño de la ventana
        self.ventana.title('Gestión de productos')  # Título de la ventana
        self.ventana.focus_force()  # Fuerza que tenga el foco
        self.ventana.lift()  # Trae la ventana al frente

        self.controlador = controlador  # Referencia al controlador para manejar los productos

        # Configuracion que contiene funciones la funcion de abrir a fullscreen y cerrar
        self.principal = ventana_principal
        self.configuracion = Config()
        self.configuracion.abrir_fullscreen(self.ventana)
        self.principal.withdraw() # oculta la ventana principal



        self.crear_titulo()  # Crea el panel superior y el layout principal
        self.cargar_productos_en_tree()  # Carga los datos iniciales en el TreeView

    def cargar_productos_en_tree(self):
        """Carga todos los productos en el TreeView"""
        # Limpiar el TreeView antes de cargar
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todos los productos desde el controlador
        for producto in self.controlador.productos:
            self.tree.insert('', 'end', values=(
                producto.idProducto,
                producto.nombreProducto,
                producto.categoria,
                producto.precio,
                producto.stock
            ))

    def crear_titulo(self):
        """Crea el panel superior, título, layout de columnas y llama a los métodos de formulario, lista y botones"""
        # Panel superior
        self.panel_superior = Frame(self.ventana, bg='Sienna')  # Frame de color Sienna
        self.panel_superior.pack(fill="x")  # Se expande horizontal y verticalmente

        # Etiqueta del título
        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de productos",  # Texto del título
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
        self.crear_lista_productos()  # Columna derecha: lista de productos

    def crear_formulario(self):
        """Crea el formulario para agregar o modificar productos"""
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Grid en columna izquierda

        # Configuración de columnas para ajustar tamaños
        self.frame_principal.grid_columnconfigure(1, weight=1)

        # Título del formulario
        CTkLabel(
            self.frame_formulario,
            text="Datos de productos",
            font=self.configuracion.texto_form_heading
        ).grid(row=0, column=0, columnspan=2, pady=30)

        # Campos del formulario
        campos = [
            ("ID del producto:", "id_entry"),
            ("Nombre:", "nombre_entry"),
            ("Categoria:", None),
            ("Precio:", "precio_entry"),
            ("Stock:", "stock_entry"),
        ]

        self.entries = {}  # Diccionario para almacenar los entries

        row = 1
        for label, key in campos:
            if key is None:  # Campo Categoria: ComboBox
                CTkLabel(
                    self.frame_formulario,
                    text="Categoría:",
                    font=self.configuracion.texto_form
                ).grid(row=row, column=0, padx=15, pady=10, sticky="e")

                self.categoria_combo = ttk.Combobox(
                    self.frame_formulario,
                    state="readonly",
                    values=["Bebida", "Bollería", "Postre"],  # Lista de categoria
                    font=self.configuracion.texto_form_combo,
                    justify="center",
                    width=23
                )
                self.categoria_combo.grid(row=row, column=1, padx=8, pady=8, sticky="w")
                self.categoria_combo.current(0)  # Selecciona la primera categoria por defecto
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

        botones_buscar=[
            ("Buscar por nombre", self.buscar_nombre, "Gainsboro")
        ]
        frame_boton_buscar = self.configuracion.crear_botones_buscar(self.frame_formulario,botones_buscar)
        frame_boton_buscar.grid(row=9, column=0, columnspan=2, pady=10, sticky="s")

    # -------------------- BOTONES -----------------------
        botones = [
            ("Agregar", self.agregar_producto, "Gainsboro"),
            ("Modificar", self.modificar_producto, "Gainsboro"),
            ("Eliminar", self.eliminar_producto, "Gainsboro"),
            ("Limpiar", self.limpiar_campos, "Gainsboro"),
            ("Salir", self.salir, "Gainsboro")
        ]

        self.frame_botones = self.configuracion.crear_botones(self.ventana, botones)

    def crear_lista_productos(self):
        """Crea la lista de productos con TreeView y scrollbars"""
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Columna derecha

        # Contenedor para TreeView y Scrollbars
        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Estilo del TreeView
        style = ttk.Style()
        style.configure("Treeview", font=self.configuracion.texto_treeview,
                        rowheight=self.configuracion.anchura_linea_treeview)
        style.configure("Treeview.Heading", font=self.configuracion.texto_treeview)

        # Scrollbars
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical", takefocus=True)
        scrollbary.pack(side="right", fill="y")

        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # TreeView
        columns = ("ID Producto", "Nombre", "Categoría", "Pecio", "Stock")
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

        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)  # Evento de selección

    def ordenar_columnas(self, columna, descendente):
        """
        Ordena el TreeView por la columna especificada.
        Alterna entre orden ascendente y descendente.
        """
        # Obtener todos los datos del TreeView
        datos = [(self.tree.set(item, columna), item) for item in self.tree.get_children('')]

        # Intentar ordenar como números si es posible, si no como texto
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

    # -------------------- MÉTODOS DE ACCIÓN -----------------------
    def buscar_nombre(self):
        nombre = self.entries['nombre_entry'].get()
        producto = controlador.buscar_por_nombre(nombre)  # Llamamos al controlador
        if producto:
            self.limpiar_campos()

            self.entries['id_entry'].insert(0, producto.idProducto)
            self.entries['nombre_entry'].insert(0, producto.nombreProducto)
            self.categoria_combo.set(producto.categoria)
            self.entries['precio_entry'].insert(0, producto.precio)
            self.entries['stock_entry'].insert(0, producto.stock)
        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún cliente con ese email.")

    def agregar_producto(self):
        """Agrega un nuevo producto al controlador y al TreeView"""
        try:
            producto = Producto(
                idProducto=self.entries['id_entry'].get(),
                nombreProducto=self.entries['nombre_entry'].get(),
                categoria=self.categoria_combo.get(),
                precio=self.entries['precio_entry'].get(),
                stock=self.entries['stock_entry'].get()
            )

            if not self.controlador.agregar_producto(producto):
                messagebox.showwarning("Advertencia",
                                       "Todos los datos son obligatorios.\n"
                                       "El ID no se puede repetir.\n"
                                       "El nombre del producto debe ser único."
                                       )
                self.ventana.focus_force()
            else:
                self.tree.insert('', 'end', values=(
                    producto.idProducto,
                    producto.nombreProducto,
                    producto.categoria,
                    producto.precio,
                    producto.stock
                ))
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
            print(f"{str(e)}")
            self.ventana.focus_force()

    def modificar_producto(self):
        """Modifica los datos del producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia",
                                   "Seleccione un producto para modificar")
            self.ventana.focus_force()
            return

        try:
            item = self.tree.item(seleccion[0])
            idProducto_original = str(item['values'][0])  # Guardamos el ID original

            # Crear un nuevo objeto Producto con los valores modificados
            producto_modificado = Producto(
                idProducto=self.entries['id_entry'].get(),
                nombreProducto=self.entries['nombre_entry'].get(),
                categoria=self.categoria_combo.get(),
                precio=self.entries['precio_entry'].get(),
                stock=self.entries['stock_entry'].get()
            )

            # Llamar al método del controlador pasando el ID original
            if self.controlador.modificar_producto(producto_modificado, idProducto_original):
                # Actualizar el TreeView
                self.tree.item(seleccion[0], values=(
                    producto_modificado.idProducto,
                    producto_modificado.nombreProducto,
                    producto_modificado.categoria,
                    producto_modificado.precio,
                    producto_modificado.stock
                ))
                messagebox.showinfo("Éxito",
                                    "Producto modificado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()
            else:
                messagebox.showwarning("Advertencia",
                                       "Todos los datos son obligatorios.\n"
                                      "El ID no se puede repetir.\n"
                                      "El nombre del producto debe ser único.")
                self.ventana.focus_force()

        except Exception as e:
            messagebox.showerror("Error",
            f"Error al modificar producto: {str(e)}")
            self.ventana.focus_force()

    def eliminar_producto(self):
        """Elimina el producto seleccionado del controlador y del TreeView"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:

                item = self.tree.item(seleccion[0])
                idProducto = item['values'][0]
                # Eliminar de la lista del controlador
                self.controlador.borrar_producto(idProducto)  # Elimina del controlador
                self.tree.delete(seleccion[0])  # Elimina del TreeView
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")

    def seleccionar_producto(self, event):
        """Llena los campos del formulario con los datos del producto seleccionado"""
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

            self.categoria_combo.set(valores[2])

            self.entries['precio_entry'].delete(0, 'end')
            self.entries['precio_entry'].insert(0, valores[3])

            self.entries['stock_entry'].delete(0, 'end')
            self.entries['stock_entry'].insert(0, valores[4])

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries.values():
            entry.delete(0, 'end')

        for categoria in self.categoria_combo.get():
            self.categoria_combo.set("")

        for key, entry in self.entries.items():
            entry.configure(state="normal")  # habilitar por si estaba bloqueado
            entry.delete(0, 'end')

    def salir(self):
        """Cierra la ventana"""
        self.ventana.destroy()
        self.principal.deiconify()

