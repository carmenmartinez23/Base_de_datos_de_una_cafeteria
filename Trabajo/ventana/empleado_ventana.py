from customtkinter import *
from tkinter import messagebox, ttk, Frame, Label

from Controlador.Controlador import controlador
from Modelo.Empleado import Empleado

class EmpleadoVentana:
    def __init__(self, parent):
        self.ventana = CTkToplevel(parent) #Esta ventana depende de Principal
        self.ventana.geometry('1200x700')
        self.ventana.title('Gestión de Empleados')
        self.ventana.transient(parent)  # La vincula a la ventana principal
        self.ventana.focus_force()  # Fuerza el foco
        self.ventana.lift()   # La trae al frente

        # Cargar empleados de prueba
        self.controlador = controlador

        self.crear_titulo()

        # Cargar los datos en el TreeView
        self.cargar_empleados_en_tree()


    #Cargar empleados
    def cargar_empleados_en_tree(self):
        # Limpiar el TreeView primero
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todos los empleados
        for empleado in self.controlador.empleados:
            self.tree.insert('', 'end', values=(
                empleado.idEmpleado,
                empleado.nombreEmpleado,
                empleado.apellidoEmpleado,
                empleado.telefonoEmpleado,
                empleado.emailEmpleado,
                empleado.direccionEmpleado,
                empleado.salario,
                empleado.rango
            ))

#---------------------- PANEL SUPERIOR -------------------------
    def crear_titulo(self):
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(side="top", expand=YES, fill="both") # both para que rellene tanto titulo como frame

        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Empleados",
            font=("Britannic Bold", 52),
            fg="white",
            justify="right",
            bg="Sienna")

        self.etiqueta_titulo.pack(side="top", expand=YES)

        # Frame principal dividido en dos columnas
        self.frame_principal = CTkFrame(self.ventana, fg_color="Sienna", bg_color="Sienna")
        self.frame_principal.pack(fill="both", padx=20, pady=30)

        # COLUMNA IZQUIERDA - Formulario
        self.crear_formulario()

        # COLUMNA DERECHA - Lista de empleados
        self.crear_lista_empleados()

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
            text="Datos del Empleados",
            font=("Goudy Old Style", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos del formulario
        campos = [
            ("ID Empleado:", "id_entry"),
            ("Nombre:", "nombre_entry"),
            ("Apellido:", "apellido_entry"),
            ("Teléfono:", "telefono_entry"),
            ("Email:", "email_entry"),
            ("Dirección:", "direccion_entry"),
            ("Salario:", "salario_entry"),
            ("Rango:", "rango_entry")
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

    # -------------------- LISTA DE EMPLEADOS -----------------------
    def crear_lista_empleados(self):
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título
        CTkLabel(
            self.frame_lista,
            text="Lista de Empleados",
            font=("Goudy Old Style", 20, "bold")
        ).pack(pady=10)

        # Frame contenedor para TreeView y Scrollbars
        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame contenedor para TreeView y Scrollbars
        style = ttk.Style()
        style.configure("Treeview.Heading",
                        font=("Goudy Old Style", 13, "bold"))
        style.configure("Treeview",
                        font=("Goudy Old Style", 13), #fuente de las filas
                        rowheight=20) #Altura de filas

        # Scrollbars
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical")
        scrollbary.pack(side="right", fill="y")

        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # Treeview (DESPUÉS del scrollbar, vinculado a ellas)
        columns = ("ID", "Nombre", "Apellido", "Teléfono", "Email", "Dirección", "Salario", "Rango")
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
        self.tree.pack(side="right", fill="both", expand=True)

        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_empleado)

    # -------------------- BOTONES -----------------------
    def crear_botones(self):
        self.frame_botones = CTkFrame(self.ventana, fg_color="transparent")
        self.frame_botones.pack(pady=20)

        botones = [
            ("Agregar", self.agregar_empleado, "Gainsboro"),
            ("Modificar", self.modificar_empleado, "Gainsboro"),
            ("Eliminar", self.eliminar_empleado, "Gainsboro"),
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
    def agregar_empleado(self):
        try:
            # Obtener valores
            empleado = Empleado(
                idEmpleado=self.entries['id_entry'].get(),
                nombreEmpleado=self.entries['nombre_entry'].get(),
                apellidoEmpleado=self.entries['apellido_entry'].get(),
                telefonoEmpleado=self.entries['telefono_entry'].get(),
                emailEmpleado=self.entries['email_entry'].get(),
                direccionEmpleado=self.entries['direccion_entry'].get(),
                salario=self.entries['salario_entry'].get(),
                rango=self.entries['rango_entry'].get()
            )

            # Validar que no estén vacíos y agregar a la lista
            if not self.controlador.empleados.append(empleado):
                messagebox.showwarning("Advertencia", "ID, Nombre y Apellido son obligatorios")
                self.ventana.focus_force()
            else:
                # Agregar al treeview
                self.tree.insert('', 'end', values=(
                    empleado.idEmpleado,
                    empleado.nombreEmpleado,
                    empleado.apellidoEmpleado,
                    empleado.telefonoEmpleado,
                    empleado.emailEmpleado,
                    empleado.direccionEmpleado,
                    empleado.salario,
                    empleado.rango
                ))

                messagebox.showinfo("Éxito", "Empleado agregado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar empleado: {str(e)}")
            self.ventana.focus_force()

# -------------------- MODIFICAR EMPLEADOS -----------------------
    def modificar_empleado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para modificar")
            self.ventana.focus_force()
            return

        try:
            item = self.tree.item(seleccion[0])
            idEmpleado = item['values'][0]

            # Buscar empleado en la lista
            for i, empleado in enumerate(self.controlador.empleados):
                if empleado.idEmpleado == idEmpleado:
                    # Actualizar datos
                    empleado.nombreEmpleado = self.entries['nombre_entry'].get()
                    empleado.apellidoEmpleado = self.entries['apellido_entry'].get()
                    empleado.telefonoEmpleado = self.entries['telefono_entry'].get()
                    empleado.emailEmpleado = self.entries['email_entry'].get()
                    empleado.direccionEmpleado = self.entries['direccion_entry'].get()
                    empleado.salario = self.entries['salario_entry'].get()
                    empleado.rango = self.entries['rango_entry'].get()

                    # Actualizar treeview
                    self.tree.item(seleccion[0], values=(
                        empleado.idEmpleado,
                        empleado.nombreEmpleado,
                        empleado.apellidoEmpleado,
                        empleado.telefonoEmpleado,
                        empleado.emailEmpleado,
                        empleado.direccionEmpleado,
                        empleado.salario,
                        empleado.rango
                    ))

                    messagebox.showinfo("Éxito", "Empleado modificado correctamente")
                    self.ventana.focus_force()
                    self.limpiar_campos()
                    break

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar empleado: {str(e)}")
            self.ventana.focus_force()

    # -------------------- ELIMINAR EMPLEADOS -----------------------
    def eliminar_empleado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este empleado?"):
            try:
                item = self.tree.item(seleccion[0])
                idEmpleado = item['values'][0]

                # Eliminar de la lista
                self.controlador.borrar_empleado(idEmpleado)

                # Eliminar del treeview
                self.tree.delete(seleccion[0])

                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
                self.limpiar_campos()

            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar empleado: {str(e)}")

    # -------------------- SELECCIÓN Y LIMPIEZA -----------------------
    def seleccionar_empleado(self, event):
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

            self.entries['salario_entry'].delete(0, 'end')
            self.entries['salario_entry'].insert(0, valores[6])

            self.entries['rango_entry'].delete(0, 'end')
            self.entries['rango_entry'].insert(0, valores[7])

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')

    def salir(self):
        self.ventana.destroy()