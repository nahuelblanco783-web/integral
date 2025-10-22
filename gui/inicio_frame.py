import customtkinter as ctk
from PIL import Image

class InicioFrame(ctk.CTkFrame):
    """Frame de inicio del programa / main window"""
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.configure(corner_radius=0, border_width=0, fg_color='white')
        self.pack(fill='both', expand=True)

        # Cargar imagen base (una sola vez)
        self.original_image = Image.open("gui/images/integral.png")

        # Crear objeto CTkImage (con tamaño inicial)
        self.integral_image = ctk.CTkImage(
            light_image=self.original_image,
            dark_image=self.original_image,
            size=(350, 350)
        )

        # Frame central para centrar todo
        center_frame = ctk.CTkFrame(self, fg_color="white")
        center_frame.pack(expand=True)

        # Label de imagen
        self.image_label = ctk.CTkLabel(center_frame, image=self.integral_image, text="")
        self.image_label.pack(pady=(0, 20))

        # Label de texto
        self.text_label = ctk.CTkLabel(
            center_frame,
            text=f"Bienvenid@, {self.user[2]}",
            text_color='black',
            font=('Lato Light', 32)
        )
        self.text_label.pack()

        # Vincular evento de redimensionado
        self.bind("<Configure>", self._resize_image)

    def _resize_image(self, event):
        """Escala la imagen según el tamaño del frame."""
        # Calcular un tamaño proporcional al ancho del frame
        new_size = min(event.width // 3, event.height // 3)
        new_size = max(150, new_size)  # evita que se haga demasiado chica

        # Actualizar el objeto CTkImage con el nuevo tamaño
        self.integral_image.configure(size=(new_size, new_size))

        # Actualizar la etiqueta para redibujar
        self.image_label.configure(image=self.integral_image)
