"""
Tema escuro para a aplicação Pricing Assistant
"""

import tkinter as tk
from tkinter import ttk


class DarkTheme:
    """Tema escuro moderno"""

    def __init__(self):
        self.colors = {
            "primary": "#BB86FC",
            "secondary": "#03DAC6",
            "accent": "#CF6679",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#CF6679",
            "background": "#121212",
            "surface": "#1E1E1E",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B0B0B0",
        }

    def apply(self, root):
        """Aplica o tema escuro à aplicação"""
        style = ttk.Style()

        # Configurar tema escuro
        style.theme_use("clam")

        # Configurar cores para tema escuro
        style.configure(
            ".",
            background=self.colors["background"],
            foreground=self.colors["text_primary"],
            fieldbackground=self.colors["surface"],
            selectbackground=self.colors["primary"],
        )

        # Configurar widgets específicos
        style.configure("TFrame", background=self.colors["background"])
        style.configure("TLabel", background=self.colors["background"])
        style.configure("TButton", padding=(10, 5))
        style.configure("Accent.TButton", background=self.colors["accent"])

        # Configurar a janela principal
        root.configure(background=self.colors["background"])
