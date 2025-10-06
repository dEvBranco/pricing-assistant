import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable


class ProductForm(ttk.Frame):
    """Formulário para entrada de dados do produto"""

    def __init__(self, parent, on_analyze: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_analyze = on_analyze
        self._create_widgets()

    def _create_widgets(self):
        """Cria os widgets do formulário"""
        self.columnconfigure(1, weight=1)

        # Título da seção
        title = ttk.Label(
            self, text="🔍 Análise de Produto", font=("Helvetica", 12, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # Campo de pesquisa
        ttk.Label(self, text="Produto:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20))

        # Condição do produto
        ttk.Label(self, text="Condição:").grid(
            row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(15, 0)
        )
        self.condition_var = tk.StringVar(value="new")
        condition_frame = ttk.Frame(self)
        condition_frame.grid(row=2, column=1, sticky=tk.W, pady=(15, 0))

        conditions = [
            ("Novo", "new"),
            ("Muito Bom", "very_good"),
            ("Bom", "good"),
            ("Razoável", "satisfactory"),
        ]

        for i, (text, value) in enumerate(conditions):
            rb = ttk.Radiobutton(
                condition_frame, text=text, variable=self.condition_var, value=value
            )
            rb.grid(row=0, column=i, padx=(0, 10))

        # Configurações avançadas
        self.advanced_frame = ttk.LabelFrame(self, text="Configurações Avançadas")
        self.advanced_frame.grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0)
        )
        self.advanced_frame.columnconfigure(1, weight=1)

        # Páginas máximas
        ttk.Label(self.advanced_frame, text="Máx. Páginas:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.pages_var = tk.IntVar(value=2)
        pages_spin = ttk.Spinbox(
            self.advanced_frame, from_=1, to=5, textvariable=self.pages_var, width=5
        )
        pages_spin.grid(row=0, column=1, sticky=tk.W)

        # Botão de análise
        self.analyze_btn = ttk.Button(
            self,
            text="🎯 Analisar Preços",
            command=self._on_analyze_click,
            style="Accent.TButton",
        )
        self.analyze_btn.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        # Bind Enter key
        self.search_entry.bind("<Return>", lambda e: self._on_analyze_click())

    def _on_analyze_click(self):
        """Handler do botão analisar"""
        search_query = self.search_var.get().strip()

        if not search_query:
            tk.messagebox.showwarning(
                "Campo Vazio", "Por favor, insira um produto para pesquisar."
            )
            self.search_entry.focus()
            return

        product_data = {
            "search_query": search_query,
            "condition": self.condition_var.get(),
            "max_pages": self.pages_var.get(),
        }

        self.on_analyze(product_data)

    def set_loading(self, loading: bool):
        """Ativa/desativa estado de loading"""
        state = "disabled" if loading else "normal"
        self.search_entry.config(state=state)
        self.analyze_btn.config(state=state)

        if loading:
            self.analyze_btn.config(text="⏳ Analisando...")
        else:
            self.analyze_btn.config(text="🎯 Analisar Preços")

    def load_data(self, data: Dict[str, Any]):
        """Carrega dados no formulário"""
        self.search_var.set(data.get("search_query", ""))
        self.condition_var.set(data.get("condition", "new"))
        self.pages_var.set(data.get("max_pages", 2))
