from customtkinter import *
from tkinter import messagebox, ttk, Frame, Label

from Controlador.Controlador import controlador
from Modelo.Productos import Producto

class ProductoVentana:
    def __init__(self, parent):
        self.ventana = CTkToplevel(parent)
        self.ventana.geometry('1200x600')
        self.ventana.title('Gestión de Productos')
        self.ventana.transient(parent)
        self.ventana.focus_force()
        self.ventana.lift()

        # Cargar empleados de prueba
        self.controlador = controlador

        self.crear_titulo()

        # Cargar los datos en el TreeView
        self.cargar_producto_en_tree()

# -------------------- CARGAR PRODUCTOS -----------------------
    def cargar_producto_en_tree(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar productos actuales
        for producto in self.controlador.productos:
            self.tree.insert('', 'end', values=(
                producto.idProducto,
                producto.nombreProducto,
                producto.categoria,
                producto.precio,
                producto.stock
            ))

    # -------------------- CREAR INTERFAZ -----------------------
    def crear_titulo(self):
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(side="top", expand=YES, fill="both")

        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Productos",
            font=("Britannic Bold", 52),
            fg="white",
            justify="right",
            bg="Sienna"
        )
        self.etiqueta_titulo.pack(side="top", expand=YES, fill="both")

        self.frame_principal = CTkFrame(self.ventana, fg_color="Sienna", bg_color="Sienna")
        self.frame_principal.pack(fill="both", padx=20, pady=30)

        self.crear_formulario()
        self.crear_lista_productos()
        self.crear_botones()

    # -------------------- FORMULARIO -----------------------
    def crear_formulario(self):
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=2)

        CTkLabel(self.frame_formulario,
                 text="Datos del Producto",
                 font=("Goudy Old Style", 20, "bold")).grid(
                 row=0, column=0, columnspan=2, pady=10)

        self.entries = {}
        campos = [
            ("ID Producto:", "id_entry"),
            ("Nombre:", "nombre_entry"),
            ("categoria", None),
            ("Precio:", "precio_entry"),
            ("Stock:", "stock_entry"),
        ]

        row = 1

        for label, key in campos:
            if key is None:
                # --- Categoría ---
                CTkLabel(
                    self.frame_formulario,
                    text="Categoría:",
                    font=("Goudy Old Style", 18)
                ).grid(row=row, column=0, padx=10, pady=8, sticky="e")
                self.categoria_combo = ttk.Combobox(
                    self.frame_formulario,
                    state="readonly",
                    values=("Bebida", "Bollería", "Postre"),
                    font=("Goudy Old Style", 16),
                    justify="center",
                )
                self.categoria_combo.grid(row=row, column=1, padx=10, pady=8, sticky="w")
                self.categoria_combo.current(0)
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
    # -------------------- TREEVIEW -----------------------
    def crear_lista_productos(self):
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        CTkLabel(self.frame_lista, text="Lista de Productos",
                 font=("Goudy Old Style", 20, "bold")
                 ).pack(pady=10)

        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Goudy Old Style", 13),
                        rowheight=20)
        style.configure("Treeview.Heading",
                        font=("Goudy Old Style", 13, "bold"))

        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical")
        scrollbary.pack(side="right", fill="y")

        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        columns = ("ID", "Nombre", "Categoria", "Precio", "Stock")
        self.tree = ttk.Treeview(
            frame_tree,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbary.set,
            xscrollcommand=scrollbarx.set,
            height=15)

        scrollbary.config(command=self.tree.yview, orient="vertical")
        scrollbarx.config(command=self.tree.xview)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(side="right", fill="both", expand=True)

        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_producto)

    # -------------------- BOTONES -----------------------
    def crear_botones(self):
        self.frame_botones = CTkFrame(self.ventana, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        botones = [
            ("Agregar", self.agregar_producto, "Gainsboro"),
            ("Modificar", self.modificar_producto, "Gainsboro"),
            ("Eliminar", self.eliminar_producto, "Gainsboro"),
            ("Limpiar", self.limpiar_campos, "Gainsboro"),
            ("Salir", self.salir, "Gainsboro")
        ]

        for texto, comando, color in botones:
            CTkButton(
                self.frame_botones,
                text=texto,
                command=comando,
                font=("Goudy Old Style", 20, "bold"),
                fg_color=color,
                text_color="black",
                hover_color="white",
                border_width=2,
                border_color=color,
                width=100,
                height=50,
                corner_radius=32
            ).pack(side="left", padx=5)

# -------------------- AGREGAR PRODUCTO -----------------------
    def agregar_producto(self):
        try:
            producto = Producto(
                idProducto=self.entries['id_entry'].get(),
                nombreProducto=self.entries['nombre_entry'].get(),
                categoria=self.categoria_combo.get(),
                precio=self.entries['precio_entry'].get(),
                stock=self.entries['stock_entry'].get()
            )

            self.controlador.agregar_producto(producto)

            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# -------------------- MODIFICAR PRODUCTO -----------------------
    def modificar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            self.ventana.focus_force()
            return
        try:
            item = self.tree.item(seleccion[0])
            idProducto = item['values'][0]

            # Buscar producto en la lista
            for p, producto in enumerate(self.controlador.productos):
                if producto.idProducto == idProducto:
                    producto.nombreProducto = self.entries['nombre_entry'].get()
                    producto.categoria = self.categoria_combo.get()
                    producto.precio = self.entries['precio_entry'].get()
                    producto.stock = self.entries['stock_entry'].get()

                    self.tree.item(seleccion[0], values = (
                        producto.nombreProducto,
                        producto.categoria,
                        producto.precio,
                        producto.stock
                    ))

                messagebox.showinfo("Éxito", "Producto modificado correctamente")

                self.ventana.focus_force()
                self.limpiar_campos()
                break

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar empleado: {str(e)}")
            self.ventana.focus_force()

# -------------------- ELIMINAR PRODUCTO -----------------------
    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                item = self.tree.item(seleccion[0])
                idProducto = item['values'][0]

                self.controlador.borrar_productos(idProducto)

                self.cargar_producto_en_tree() #volver a recargar

                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")

            except Exception as e: (
                messagebox.showerror("Error", f"Error al eliminar empleado: {str(e)}"))

    # -------------------- SELECCIÓN Y LIMPIEZA -----------------------
    def seleccionar_producto(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            self.entries['id_entry'].delete(0, 'end')
            self.entries['id_entry'].insert(0, valores[0])

            self.entries['nombre_entry'].delete(0, 'end')
            self.entries['nombre_entry'].insert(0, valores[1])

            self.categoria_combo.set(valores[2])

            self.entries['precio_entry'].delete(0, 'end')
            self.entries['precio_entry'].insert(0, valores[3])

            self.entries['stock_entry'].delete(0, 'end')
            self.entries['stock_entry'].insert(0, valores[4])

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')

    def salir(self):
        self.ventana.destroy()
