from customtkinter import *
from tkinter import messagebox, ttk, Frame, Label
import tkinter.font as tkFont

from Controlador.Controlador import controlador
from Documentos.config import Config
from Modelo.Empleado import Empleado

class EmpleadoVentana:
    def __init__(self, ventana_principal):
        # Crear ventana secundaria dependiente de la principal
        self.principal = ventana_principal
        self.ventana = CTkToplevel()
        self.ventana.geometry('1200x700')  # Tamaño de la ventana
        self.ventana.title('Gestión de Empleados')
        self.ventana.focus_force()          # Fuerza que tenga el foco
        self.ventana.lift()                 # La trae al frente

        # Controlador que maneja la lista de empleados y operaciones
        self.controlador = controlador

        # Configuracion que contiene funciones la funcion de abrir a fullscreen y cerrar
        self.configuracion = Config()
        self.configuracion.abrir_fullscreen(self.ventana)

        # Crear el panel superior con título
        self.crear_titulo()

        # Cargar los empleados en el TreeView
        self.cargar_empleados_en_tree()

        self.principal.withdraw() # oculta la ventana principal
    # -------------------- CARGAR EMPLEADOS -----------------------
    def cargar_empleados_en_tree(self):
        # Vacía primero todos los elementos existentes en el TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar todos los empleados desde el controlador
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

        #Ajustar las columnas
        font = tkFont.Font(font=self.configuracion.texto_treeview)

        for col in self.tree["columns"]:
            max_width = font.measure(col + "▼▲")

            for item in self.tree.get_children():
                texto = self.tree.set(item, col)
                max_width = max(max_width, font.measure(texto))

            self.tree.column(col, width=max_width + 20)
    # -------------------- PANEL SUPERIOR -------------------------
    def crear_titulo(self):
        # Panel superior con fondo Sienna
        self.panel_superior = Frame(self.ventana, bg='Sienna')
        self.panel_superior.pack(fill="x")

        # Etiqueta del título
        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Informe de Empleados",
            font=self.configuracion.texto_head,
            fg="white",
            justify="right",
            bg="Sienna")
        self.etiqueta_titulo.pack(side="top", expand=YES)

        # Frame principal donde van el formulario y la lista
        self.frame_principal = CTkFrame(
            self.ventana,
            fg_color="Sienna",
            bg_color="Sienna"
        )
        self.frame_principal.pack(fill="both", padx=20, pady=30)

        # Crear columna izquierda: formulario
        self.crear_formulario()

        # Crear columna derecha: lista de empleados
        self.crear_lista_empleados()

    # -------------------- FORMULARIO -----------------------
    def crear_formulario(self):
        self.frame_formulario = CTkFrame(self.frame_principal)
        self.frame_formulario.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Configurar distribución de columnas
        self.frame_principal.grid_columnconfigure(1, weight=1)

        # Título del formulario
        CTkLabel(
            self.frame_formulario,
            text="Datos del Empleados",
            font=self.configuracion.texto_form_heading
        ).grid(row=0, column=0, columnspan=2, pady=30)

        # Campos del formulario: ID, nombre, apellido, teléfono, email, dirección, salario, rango
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

        self.entries = {}  # Diccionario donde guardamos cada entry

        for i, (label_text, entry_name) in enumerate(campos, start=1):
            # Crear etiqueta
            CTkLabel(
                self.frame_formulario,
                text=label_text,
                font=self.configuracion.texto_form
            ).grid(row=i, column=0, padx=15, pady=10, sticky="e")

            # Crear campo de entrada
            entry = CTkEntry(
                self.frame_formulario,
                width=self.configuracion.anchura_entry_form,
                font=self.configuracion.texto_form
            )
            entry.grid(row=i, column=1, padx=5, pady=10, sticky="w")
            self.entries[entry_name] = entry  # Guardar entry en el diccionario

        botones_buscar=[
            ("Buscar por email", self.buscar_email, "Gainsboro"),
            ("Buscar por telefono", self.buscar_telefono, "Gainsboro")
        ]
        frame_botones_buscar=self.configuracion.crear_botones_buscar(self.frame_formulario,botones_buscar)
        frame_botones_buscar.grid(row=9, column=0, columnspan=2, pady=1, sticky="s")

        # -------------------- BOTONES -----------------------
        botones = [
            ("Agregar", self.agregar_empleado, "Gainsboro"),
            ("Modificar", self.modificar_empleado, "Gainsboro"),
            ("Eliminar", self.eliminar_empleado, "Gainsboro"),
            ("Limpiar", self.limpiar_campos, "Gainsboro"),
            ("Salir", self.salir, "Gainsboro")
        ]
        self.frame_botones = self.configuracion.crear_botones(self.ventana, botones)

    # -------------------- LISTA DE EMPLEADOS -----------------------
    def crear_lista_empleados(self):
        # Frame contenedor de la lista
        self.frame_lista = CTkFrame(self.frame_principal)
        self.frame_lista.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Frame para el TreeView y scrollbars
        frame_tree = Frame(self.frame_lista)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Estilo del TreeView
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.configuracion.texto_treeview)
        style.configure("Treeview",
                        font=self.configuracion.texto_treeview,
                        rowheight=self.configuracion.anchura_linea_treeview)

        # Scrollbars
        scrollbary = ttk.Scrollbar(frame_tree, orient="vertical")
        scrollbary.pack(side="right", fill="y")
        scrollbarx = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        # TreeView con columnas
        columns = ("ID", "Nombre", "Apellido", "Teléfono", "Email", "Dirección", "Salario", "Rango")
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
        scrollbarx.config(command=self.tree.xview)

        self.orden_columnas = {}

        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col,
                              command=lambda col=col: self.ordenar_columnas(col, False))
            self.tree.column(col, width=100, anchor="center")
            self.orden_columnas[col] = False

        self.tree.pack(side="left", fill="both", expand=True)  # Empaquetar TreeView

        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_empleado)  # Evento de selección

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

    # -------------------- AGREGAR EMPLEADOS -----------------------
    def buscar_email(self):
        email = self.entries['email_entry'].get()
        empleado = controlador.buscar_empleado_por_email(email)  # Llamamos al controlador

        if empleado:
            # Actualizar TreeView
            if empleado:
                self.entries['id_entry'].insert(0, empleado.idEmpleado)
                self.entries['nombre_entry'].insert(0, empleado.nombreEmpleado)
                self.entries['apellido_entry'].insert(0, empleado.apellidoEmpleado)
                self.entries['telefono_entry'].insert(0, empleado.telefonoEmpleado)
                self.entries['direccion_entry'].insert(0, empleado.direccionEmpleado)
                self.entries['salario_entry'].insert(0, empleado.salario)
                self.entries['rango_entry'].insert(0, empleado.rango)
        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún cliente con ese email.")

    def buscar_telefono(self):
        telefono = self.entries['telefono_entry'].get()
        empleado = controlador.buscar_empleado_por_telefono(telefono)  # Llamamos al controlador
        if empleado:
            self.entries['id_entry'].insert(0, empleado.idEmpleado)
            self.entries['nombre_entry'].insert(0, empleado.nombreEmpleado)
            self.entries['apellido_entry'].insert(0, empleado.apellidoEmpleado)
            self.entries['email_entry'].insert(0, empleado.emailEmpleado)
            self.entries['direccion_entry'].insert(0, empleado.direccionEmpleado)
            self.entries['salario_entry'].insert(0, empleado.salario)
            self.entries['rango_entry'].insert(0, empleado.rango)
        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún cliente con ese teléfono.")

    def agregar_empleado(self):
        """Agrega un nuevo empleado al controlador y al TreeView"""
        try:
            # Crear objeto Empleado con los datos del formulario
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
            # Agregar a la lista de empleados
            if not self.controlador.agregar_empleado(empleado):
                messagebox.showwarning(
                    "Advertencia",
                    "ID, Nombre y Apellido son obligatorios.\n"
                    "El ID, el teléfono y el email no se pueden repetir."
                )
                self.ventana.focus_force()
            else:
                # Insertar en TreeView
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
                messagebox.showinfo("Éxito",
                                    "Empleado agregado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error al agregar empleado: {str(e)}")
            self.ventana.focus_force()

    # -------------------- MODIFICAR EMPLEADOS -----------------------
    def modificar_empleado(self):
        """
        Permite modificar el empleado seleccionado en el TreeView.
        Actualiza tanto la lista del controlador como la vista.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia",
                                   "Seleccione un empleado para modificar")
            return

        try:
            item = self.tree.item(seleccion[0])
            idEmpleado_original = item['values'][0]

            # Actualizar los datos con el formulario
            empleado_modificado = Empleado(
                idEmpleado = self.entries['id_entry'].get(),
                nombreEmpleado = self.entries['nombre_entry'].get(),
                apellidoEmpleado = self.entries['apellido_entry'].get(),
                telefonoEmpleado = self.entries['telefono_entry'].get(),
                emailEmpleado = self.entries['email_entry'].get(),
                direccionEmpleado = self.entries['direccion_entry'].get(),
                salario = self.entries['salario_entry'].get(),
                rango = self.entries['rango_entry'].get()
            )

            # Llamar al controlador
            if self.controlador.modificar_empleado(empleado_modificado, idEmpleado_original):
                # Actualizar TreeView
                self.tree.item(seleccion[0], values=(
                    empleado_modificado.idEmpleado,
                    empleado_modificado.nombreEmpleado,
                    empleado_modificado.apellidoEmpleado,
                    empleado_modificado.telefonoEmpleado,
                    empleado_modificado.emailEmpleado,
                    empleado_modificado.direccionEmpleado,
                    empleado_modificado.salario,
                    empleado_modificado.rango
                ))
                messagebox.showinfo("Éxito",
                                    "Empleado modificado correctamente")
                self.ventana.focus_force()
                self.limpiar_campos()
            else:
                messagebox.showwarning(
                    "Advertencia",
                    "El ID, el nombre y el apellido son obligatorios.\n"
                    "El ID, el teléfono y el email no se pueden repetir."
                )
                self.ventana.focus_force()

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Error al modificar empleado: {str(e)}")
            self.ventana.focus_force()

    # -------------------- ELIMINAR EMPLEADOS -----------------------
    def eliminar_empleado(self):
        """
        Elimina el empleado seleccionado después de confirmar.
        Borra de la lista del controlador y del TreeView.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")
            self.ventana.focus_force()
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este empleado?"):
            try:
                item = self.tree.item(seleccion[0])
                idEmpleado = item['values'][0]

                # Eliminar del controlador
                self.controlador.borrar_empleado(idEmpleado)

                # Eliminar del TreeView
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

            # Llenar los campos del formulario con los datos seleccionados
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

            self.entries['salario_entry'].delete(0, 'end')
            self.entries['salario_entry'].insert(0, valores[6])

            self.entries['rango_entry'].delete(0, 'end')
            self.entries['rango_entry'].insert(0, valores[7])

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for entry in self.entries.values():
            entry.delete(0, 'end')

        for key, entry in self.entries.items():
            entry.configure(state="normal")  # habilitar por si estaba bloqueado
            entry.delete(0, 'end')

    def salir(self):
        """Cierra la ventana y vuelve a mostrar la principal"""
        self.ventana.destroy()
        self.principal.deiconify()

