from customtkinter import CTkFrame, CTkButton
from tkcalendar import DateEntry


class Config:
    texto_head=("Britannic Bold", 84)
    texto_form_heading=("Palatino Linotype", 40, "bold")
    texto_form=("Palatino Linotype", 25)
    texto_form_combo=("Palatino Linotype", 20)
    texto_treeview=("Palatino Linotype", 18)
    texto_treeview_head=("Palatino Linotype", 19, "bold")
    texto_boton=("Times New Roman", 40)
    anchura_boton=220
    altura_boton=50
    anchura_linea_treeview=35
    anchura_entry_form=350



    def abrir_fullscreen(self, aplicacion):
        ancho_ventana = 1600
        alto_ventana = 900
        ancho_pantalla = aplicacion.winfo_screenwidth()
        alto_pantalla = aplicacion.winfo_screenheight()
        x = (ancho_pantalla - ancho_ventana) // 2.2
        y = (alto_pantalla - alto_ventana) // 2.2
        aplicacion.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        aplicacion.attributes("-fullscreen", True)

        # Salir con ESC
        aplicacion.bind("<Escape>", lambda e: aplicacion.attributes("-fullscreen", False))
        #lambda pasa un e de evento y le manda el comando fullcreen true
        aplicacion.bind("<F11>", lambda e: aplicacion.attributes("-fullscreen", True))

    def crear_botones(self, ventana, botones):
        """
        Crea un frame de botones en la ventana dada.
        """
        frame_botones = CTkFrame(ventana, fg_color="transparent")
        frame_botones.pack(pady=20)

        for texto, comando, color in botones:
            CTkButton(
                frame_botones,
                text=texto,
                command=comando,
                font=self.texto_boton,
                fg_color=color,
                text_color="black",
                hover_color="white",
                border_width=2,
                border_color="Gainsboro",
                width=self.anchura_boton,
                height=self.altura_boton,
                corner_radius=32
            ).pack(side="left", padx=20)

        return frame_botones

    def crear_botones_buscar(self, contenedor, botones_buscar):
        frame_botones = CTkFrame(contenedor, fg_color="transparent")
        for i, (texto, comando, color) in enumerate(botones_buscar):
            CTkButton(
                frame_botones,
                text=texto,
                command=comando,
                font=("Times New Roman", 30),
                fg_color=color,
                text_color="black",
                hover_color="white",
                border_width=2,
                border_color="white",
                width=self.anchura_boton,
                height=self.altura_boton,
                corner_radius=32
            ).grid(row=i, column=0, padx=10, pady=15)
        return frame_botones


    def crear_calendario(self, frame_formulario):
        calendario = DateEntry(
            frame_formulario,
            date_pattern="yyyy/mm/dd",
            locale="en_US",
            width=23,
            font=self.texto_form_combo,
            justify="center",
            background="Sienna",
            headersbackground="Sienna",
            headersforeground="White",
            weekendbackground="gray",
            weekendforeground="gray30",
            othermonthbackground="gray",
            othermonthforeground="gray30",
            normalbackground="White",
            normalforeground="Black",
            selectbackground="Sienna"
        )
        calendario.grid(row=4, column=1, padx=10, pady=8, sticky="w")
        original_drop_down = calendario.drop_down

        def agrandar_calendario():
            original_drop_down()
            try:
                # Acceder al toplevel del calendario
                top = calendario._top_cal

                # Hacer el toplevel más grande
                top.geometry("")  # Auto-resize

                # Aumentar tamaño de fuente del calendario interno
                cal = calendario._calendar

                # Cambiar texto de las flechas por símbolos más grandes
                cal._l_year.config(text='  ◄◄  ')
                cal._l_month.config(text='  ◄  ')
                cal._r_month.config(text='  ►  ')
                cal._r_year.config(text='  ►►  ')

            except Exception as e:
                print(f"Error al configurar calendario: {e}")

        calendario.drop_down = agrandar_calendario

        return calendario