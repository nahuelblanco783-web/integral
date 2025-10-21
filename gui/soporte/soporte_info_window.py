import customtkinter as ctk

class TicketInfo(ctk.CTkToplevel):
    def __init__(self, id_ticket, **kwargs):
        super().__init__(**kwargs)
        self.id_ticket = id_ticket
        
        self.attributes('-topmost', True)
        