"""
Tema claro para a aplicação Pricing Assistant
"""

import tkinter as tk
from tkinter import ttk


class LightTheme:
    """Tema claro moderno"""

    def __init__(self):
        self.colors = {
            "primary": "#2C3E50",
            "secondary": "#34495E",
            "accent": "#3498DB",
            "success": "#27AE60",
            "warning": "#F39C12",
            "error": "#E74C3C",
            "background": "#ECF0F1",
            "surface": "#FFFFFF",
            "text_primary": "#2C3E50",
            "text_secondary": "#7F8C8D",
        }

    def apply(self, root):
        """Aplica o tema claro à aplicação"""
        style = ttk.Style()

        # Configurar tema
        style.theme_use("clam")

        # Configurar cores
        style.configure(
            ".",
            background=self.colors["background"],
            foreground=self.colors["text_primary"],
            fieldbackground=self.colors["surface"],
        )

        # Configurar widgets específicos
        style.configure("TFrame", background=self.colors["background"])
        style.configure("TLabel", background=self.colors["background"])
        style.configure("TButton", padding=(10, 5))
        style.configure("Accent.TButton", background=self.colors["accent"])

        # Configurar a janela principal
        root.configure(background=self.colors["background"])
