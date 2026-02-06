from customtkinter import *
from PIL import Image, ImageTk
from tkinter import Label, Frame

from ventana.cliente_ventana import ClienteVentana
from ventana.empleado_ventana import EmpleadoVentana
from ventana.pedidos_ventana import PedidoVentana
from ventana.productos_ventana import ProductoVentana
from ventana.tarjeta_ventana import TarjetaVentana


class Principal:
    def __init__(self):
        #Iniciar CustomTkinter
        self.aplicacion = CTk()
        self.aplicacion.resizable(False, False)
        self.aplicacion.geometry('1020x630')
        self.aplicacion.title('Base de datos de mi cafetería')

        self.crear_titulo()
        self.crear_frame()


    def crear_titulo(self):
 #-------------- PANEL SUPERIOR ------------------
        self.panel_superior = Frame(self.aplicacion, background='Sienna')
        self.panel_superior.pack(side="top")

        self.etiqueta_titulo = Label(
            self.panel_superior,
            text="Menú",
            font=("Britannic Bold", 52),
            fg="white",
            anchor="center",
            justify="center",
            bg="Sienna")

        self.etiqueta_titulo.grid(padx=560, pady=10, sticky="nsew")  #Padding en el eje X y padding en el eje Y

    def crear_frame(self):
#-------------- IMAGEN DE FONDO -----------------
        self.imagen_fondo = Image.open('Documentos/wallpaper_cafeteria.jpg')
        self.imagen_fondo = self.imagen_fondo.resize((1320, 830))
        self.imagen_fondo_tk = ImageTk.PhotoImage(self.imagen_fondo)

        # Usamos Label clásico solo para la imagen
        self.label_fondo = Label(self.aplicacion, image=self.imagen_fondo_tk, background='Sienna')
        self.label_fondo.place(x=0, y=80, relwidth=1, relheight=1)

# -------------- PANEL BOTONES -------------------
        self.panel_botones = CTkFrame(self.label_fondo,
                                      fg_color="Sienna",
                                      corner_radius=32)
        self.panel_botones.grid(row=0, column=0, padx=400, pady=100, sticky="ew")  # x= 10 y= 10 ancho y alto

        self.crear_botones()

        self.frame_salir = CTkFrame(
            self.label_fondo,
            fg_color="Sienna",
            corner_radius=32
        )
        self.frame_salir.place(x=400, y=400) #Posicion 400 x 400

        self.quit = CTkButton(
            self.frame_salir,
            text="Salir",
            font=("Goudy Old Style", 24, "bold"),
            fg_color="Gainsboro",
            text_color="black",
            hover_color="white",
            border_width=2,
            border_color="Gainsboro",
            width=100,
            height=50,
            corner_radius=32,
            command=self.aplicacion.destroy
        )
        self.quit.pack(padx=78, pady=40)

        # Traer el botón al frente (encima de la imagen)
        self.frame_salir.lift()

#-------------- BOTONES -------------------------
    def crear_botones(self):
        botones_config = [('Clientes',lambda: ClienteVentana(self.aplicacion)), # le damos autoridad a la ventana nueva con self.aplicacion
                          ('Tarjeta de Fidelidad', lambda: TarjetaVentana(self.aplicacion)),
                          ('Pedidos', lambda: PedidoVentana(self.aplicacion)),
                          ('Productos', lambda: ProductoVentana(self.aplicacion)),
                          ('Empleados', lambda: EmpleadoVentana(self.aplicacion))
                          ]
        for indice, (nombre_boton, comando) in enumerate(botones_config):
            boton = CTkButton(
                master=self.panel_botones,
                text=nombre_boton,
                font=("Goudy Old Style", 24, "bold"),
                fg_color="Gainsboro",  # color del botón
                text_color="black",  # color del texto
                hover_color="white",  # color del botón al pasar el ratón
                border_color="Gainsboro",
                border_width=2,
                width=220,
                height=50,
                corner_radius=32,
                command= comando
            )
            boton.grid(row=indice, column=0, padx=5, pady=5)

# Ejecutar aplicación
if __name__ == "__main__":
    app = Principal()
    app.aplicacion.mainloop()