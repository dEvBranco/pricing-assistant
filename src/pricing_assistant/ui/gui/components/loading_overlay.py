import tkinter as tk
from tkinter import ttk


class LoadingOverlay:
    """Overlay de loading para operações demoradas"""

    def __init__(self, parent):
        self.parent = parent
        self.overlay = None

    def show(self, message: str = "Processando..."):
        """Mostra overlay de loading"""
        if self.overlay:
            self.hide()

        self.overlay = tk.Toplevel(self.parent)
        self.overlay.title("Carregando")
        self.overlay.geometry("300x150")
        self.overlay.resizable(False, False)
        self.overlay.transient(self.parent)
        self.overlay.grab_set()

        # Centralizar
        self.overlay.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() - 300) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - 150) // 2
        self.overlay.geometry(f"+{x}+{y}")

        # Conteúdo
        main_frame = ttk.Frame(self.overlay, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="⏳", font=("Helvetica", 24)).pack(pady=(0, 10))

        ttk.Label(main_frame, text=message, font=("Helvetica", 10)).pack()

        # Progress bar indeterminada
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate", length=200)
        self.progress.pack(pady=(20, 0))
        self.progress.start()

    def hide(self):
        """Esconde overlay de loading"""
        if self.overlay:
            self.progress.stop()
            self.overlay.grab_release()
            self.overlay.destroy()
            self.overlay = None
