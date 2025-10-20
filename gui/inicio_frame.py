import customtkinter as ctk
from PIL import Image

class InicioFrame(ctk.CTkFrame):
    """Frame de inicio del programa / main window"""
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)  # solo master y kwargs
        self.user = user  # guardo user en self
        self.configure(corner_radius=0,border_width=0, fg_color='white')
        self.pack(fill='both',expand=True)
                
        integral_image = ctk.CTkImage(
            light_image=Image.open("gui\\images\\integral.png"),
            dark_image=Image.open("gui\\images\\integral.png"),
            size=(300, 475)
        )
        
        ctk.CTkLabel(
            master=self,
            image=integral_image,
            text=''
        ).grid(row=0, column=0, sticky='nsew')
        
        ctk.CTkLabel(
            master=self,
            text='Bienvenid@, '+self.user[2],
            text_color='black',
            font=('Lato Light', 32)
        ).grid(row=1, column=0)

