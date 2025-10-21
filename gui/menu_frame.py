import customtkinter as ctk
from CTkSeparator import CTkSeparator
from PIL import Image

class MenuFrame(ctk.CTkFrame):
    """Barra de menú superior, modular y reutilizable."""

    def __init__(self, master, user, permisos_user, callbacks: dict, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.permisos_user = permisos_user
        self.callbacks = callbacks  # Diccionario de funciones para cada botón

        self.configure(height=50, fg_color="#242423", corner_radius=0, border_width=0)
        self.pack(side="top", fill="x", padx=0, pady=0)

        # --- Definición de botones ---
        self.inicio_button = ctk.CTkButton(
            self, text="INICIO", height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2",
            command=self.callbacks.get("inicio")
        )

        self.clientes_button = ctk.CTkButton(
            self, text="CLIENTES", height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2",
            command=self.callbacks.get("clientes")
        )

        self.soporte_button = ctk.CTkButton(
            self, text="SOPORTE", height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2",
            command=self.callbacks.get("soporte")
        )

        self.empleados_button = ctk.CTkButton(
            self, text="EMPLEADOS", height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2",
            command=self.callbacks.get("empleados")
        )

        self.pago_button = ctk.CTkButton(
            self, text="PAGO", height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2",
            command=self.callbacks.get("pago")
        )

        self.equipos_button = ctk.CTkButton(
            self, text="EQUIPOS", height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2",
            command=self.callbacks.get("equipos")
        )

        self.account_button = ctk.CTkButton(
            self, text=str(self.user[2]).upper(), height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2"
        )

        self.log_out_image = ctk.CTkImage(
            light_image=Image.open("gui\\images\\log_out.png"),
            dark_image=Image.open("gui\\images\\log_out.png"),
            size=(30, 25)
        )

        self.log_out_button = ctk.CTkButton(
            self, text="", height=35, width=0,
            fg_color="#242423", hover_color="#4E4E4E", text_color="white",
            font=('Lato Light', 20), corner_radius=0, cursor="hand2",
            image=self.log_out_image,
            command=self.callbacks.get("log_out")
        )

        # --- Lógica de permisos ---
        self.opciones_disponibles = [self.inicio_button]

        if self.permisos_user[2] == 1:
            self.opciones_disponibles.append(self.clientes_button)
        if self.permisos_user[3] == 1:
            self.opciones_disponibles.append(self.soporte_button)
        if self.permisos_user[4] == 1:
            self.opciones_disponibles.append(self.empleados_button)
        if self.permisos_user[5] == 1:
            self.opciones_disponibles.append(self.pago_button)
        if self.permisos_user[6] == 1:
            self.opciones_disponibles.append(self.equipos_button)

        # --- Grid dinámico ---
        col = 0
        for i, boton in enumerate(self.opciones_disponibles):
            boton.grid(row=0, column=col, padx=(25 if i == 0 else 0, 0), pady=7)
            col += 1
            if i < len(self.opciones_disponibles) - 1:
                CTkSeparator(
                    self, orientation="vertical", length=35,
                    fg_color="white", line_weight=2,
                ).grid(row=0, column=col, padx=25)
                col += 1

        # --- Spacer para empujar account/log_out a la derecha ---
        spacer = ctk.CTkLabel(self, text="")
        spacer.grid(row=0, column=col, sticky="ew")
        self.grid_columnconfigure(col, weight=1)

        # --- Botones account / log out ---
        self.account_button.grid(row=0, column=col + 1, sticky="e", padx=(0, 25), pady=7)
        self.log_out_button.grid(row=0, column=col + 2, sticky="e", padx=(0, 25), pady=7)
