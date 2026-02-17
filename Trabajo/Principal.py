from customtkinter import *
from PIL import Image, ImageTk
from tkinter import Label, Frame

from ventana.cliente_ventana import ClienteVentana
from ventana.empleado_ventana import EmpleadoVentana
from ventana.pedidos_ventana import PedidoVentana
from ventana.productos_ventana import ProductoVentana
from ventana.tarjeta_ventana import TarjetaVentana
from Documentos.config import Config

class Principal:
    def __init__(self):
        #Iniciar CustomTkinter
        self.aplicacion = CTk()
        self.aplicacion.title('Base de datos de mi cafetería')

        self.configuracion = Config()
        self.configuracion.abrir_fullscreen(self.aplicacion)

        self.crear_titulo()
        self.crear_frame()
        self.crear_botones() #Llama al método que crea los botones del panel

    def crear_titulo(self):
        #-------------- PANEL SUPERIOR ------------------
        self.panel_superior = Frame(self.aplicacion, background='white')
        self.panel_superior.pack(fill="x")

        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Bienvenido",
            font=self.configuracion.texto_head,
            fg="Sienna",
            anchor="center",
            bg="white")

        self.etiqueta_titulo.pack(pady=10)

    def crear_frame(self):  # Método que crea el frame principal con imagen de fondo y botones
        #-------------- IMAGEN DE FONDO -----------------
        self.imagen_fondo = Image.open('Documentos/wallpaper_cafeteria.jpg')  # Carga la imagen
        self.imagen_fondo = self.imagen_fondo.resize((1920, 930))  # Redimensiona la imagen al tamaño deseado
        self.imagen_fondo_tk = ImageTk.PhotoImage(self.imagen_fondo)  # Convierte a formato compatible con Tkinter

        self.label_fondo = Label(self.aplicacion, image=self.imagen_fondo_tk, background="White")
        # Label usado solo para mostrar la imagen de fondo
        self.label_fondo.pack(fill="both", expand=True)  # Posiciona la imagen, ocupa todo el frame

    #-------------- BOTONES -------------------------
    def crear_botones(self):  # Método que crea los botones principales de navegación
        self.panel_botones = CTkFrame(self.label_fondo,
                                      fg_color="White",
                                      corner_radius=32)  # Frame para los botones
        self.panel_botones.place(relx=0.5, rely=0.2, anchor="n")  # Posición y padding

        self.panel_botones = CTkFrame(
            self.label_fondo,
            fg_color="White",
            corner_radius=32
        )
    # Centrar el panel
        self.panel_botones.place(relx=0.5, rely=0.2, anchor="n")

        # Crear botones principales
        botones_config = [
            ('Clientes', lambda: ClienteVentana(self.aplicacion)),
            ('Tarjeta de Fidelidad', lambda: TarjetaVentana(self.aplicacion)),
            ('Pedidos', lambda: PedidoVentana(self.aplicacion)),
            ('Productos', lambda: ProductoVentana(self.aplicacion)),
            ('Empleados', lambda: EmpleadoVentana(self.aplicacion))
        ]

        for indice, (nombre_boton, comando) in enumerate(botones_config):
            boton = CTkButton(
                master=self.panel_botones,
                text=nombre_boton,
                font=self.configuracion.texto_boton,
                fg_color="Gainsboro",
                text_color="black",
                hover_color="white",
                border_color="Gainsboro",
                border_width=2,
                width=self.configuracion.anchura_boton,
                height=self.configuracion.altura_boton,
                corner_radius=32,
                command=comando
            )
            # Colocamos los botones uno debajo del otro
            boton.grid(row=indice, column=0, pady=15, padx=20)

        # Botón Salir debajo de todos
        boton_salir = CTkButton(
            master=self.panel_botones,
            text="Salir",
            font=self.configuracion.texto_boton,
            fg_color="Gainsboro",
            text_color="black",
            hover_color="white",
            border_width=2,
            border_color="Gainsboro",
            width=self.configuracion.anchura_boton,
            height=self.configuracion.altura_boton,
            corner_radius=32,
            command=self.aplicacion.destroy
        )
        # Lo colocamos en la fila siguiente
        boton_salir.grid(row=len(botones_config), column=0, pady=(20,15), padx=20)

# Ejecutar aplicación
if __name__ == "__main__":  # Si se ejecuta directamente este archivo
    app = Principal()  # Crea la instancia de la clase principal
    app.aplicacion.mainloop()  # Lanza el bucle principal de la aplicación
