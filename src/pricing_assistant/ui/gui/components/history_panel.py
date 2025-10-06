import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Callable
from datetime import datetime


class HistoryPanel(ttk.Frame):
    """Painel lateral para histórico de pesquisas"""

    def __init__(self, parent, on_search_select: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_search_select = on_search_select
        self._create_widgets()

    def _create_widgets(self):
        """Cria widgets do painel de histórico"""
        self.columnconfigure(0, weight=1)

        # Título
        title = ttk.Label(self, text="📚 Histórico", font=("Helvetica", 11, "bold"))
        title.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Lista de histórico
        self.history_listbox = tk.Listbox(
            self, width=25, height=20, relief="solid", borderwidth=1
        )
        self.history_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.history_listbox.yview
        )
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Bind double click
        self.history_listbox.bind("<Double-Button-1>", self._on_item_select)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        ttk.Button(btn_frame, text="🗑️ Limpar", command=self._clear_history).grid(
            row=0, column=0, padx=(0, 5)
        )

        self.rowconfigure(1, weight=1)

    def update_history(self, history: List[Dict[str, Any]]):
        """Atualiza a lista de histórico"""
        self.history_listbox.delete(0, tk.END)

        for i, item in enumerate(history):
            display_text = f"{item['search_query'][:20]}..."
            if len(item["search_query"]) > 20:
                display_text = item["search_query"][:20] + "..."
            else:
                display_text = item["search_query"]

            timestamp = item.get("timestamp", "N/A")
            if hasattr(timestamp, "get"):
                timestamp = timestamp.get()

            self.history_listbox.insert(tk.END, f"{display_text}\n{timestamp}")

    def _on_item_select(self, event):
        """Handler para seleção de item do histórico"""
        selection = self.history_listbox.curselection()
        if selection:
            # Em implementação real, recuperaria o item completo do histórico
            tk.messagebox.showinfo(
                "Histórico",
                "Item do histórico selecionado - carregando no formulário...",
            )

    def _clear_history(self):
        """Limpa o histórico"""
        self.history_listbox.delete(0, tk.END)
        tk.messagebox.showinfo("Histórico", "Histórico limpo!")
