import tkinter as tk
from tkinter import ttk
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use("TkAgg")


class ResultsDisplay(ttk.Frame):
    """Display para mostrar resultados da análise"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
        self.current_result = None

    def _create_widgets(self):
        """Cria os widgets de display"""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Notebook para abas
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        # Aba de Recomendações
        self.recommendations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.recommendations_frame, text="💡 Recomendações")

        # Aba de Detalhes
        self.details_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.details_frame, text="📊 Detalhes")

        # Aba de Gráficos
        self.charts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_frame, text="📈 Gráficos")

        # Área de explicação
        self.explanation_frame = ttk.LabelFrame(
            self, text="🧠 Explicação do Raciocínio"
        )
        self.explanation_frame.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
        self.explanation_frame.columnconfigure(0, weight=1)
        self.explanation_frame.rowconfigure(0, weight=1)

        self.explanation_text = tk.Text(
            self.explanation_frame, wrap=tk.WORD, height=6, state=tk.DISABLED
        )
        self.explanation_text.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5
        )

        scrollbar = ttk.Scrollbar(
            self.explanation_frame,
            orient=tk.VERTICAL,
            command=self.explanation_text.yview,
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.explanation_text.config(yscrollcommand=scrollbar.set)

    def show_results(self, analysis_result):
        """Mostra os resultados da análise"""
        self.current_result = analysis_result
        self._show_recommendations()
        self._show_details()
        self._show_charts()
        self._show_explanation()

    def _show_recommendations(self):
        """Mostra recomendações de preço"""
        # Limpar frame anterior
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()

        if not self.current_result:
            return

        rec = self.current_result.pricing_recommendation
        items = self.current_result.comparable_items

        # Layout em grid
        self.recommendations_frame.columnconfigure(1, weight=1)

        # Preço recomendado (destaque)
        ttk.Label(
            self.recommendations_frame,
            text="💰 Preço Recomendado:",
            font=("Helvetica", 12, "bold"),
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        price_label = ttk.Label(
            self.recommendations_frame,
            text=f"€{rec.final_price:.2f}",
            font=("Helvetica", 16, "bold"),
            foreground="#2E8B57",
        )
        price_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))

        # Faixa de preços
        ttk.Label(
            self.recommendations_frame,
            text="📊 Faixa de Preços:",
            font=("Helvetica", 10, "bold"),
        ).grid(row=1, column=0, sticky=tk.W)

        range_label = ttk.Label(
            self.recommendations_frame,
            text=f"€{rec.price_range.min:.2f} - €{rec.price_range.max:.2f}",
            font=("Helvetica", 10),
        )
        range_label.grid(row=1, column=1, sticky=tk.W)

        # Itens encontrados
        ttk.Label(
            self.recommendations_frame,
            text=f"📦 Itens Similares Encontrados: {len(items)}",
            font=("Helvetica", 10),
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        # Botões de ação
        action_frame = ttk.Frame(self.recommendations_frame)
        action_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))

        ttk.Button(
            action_frame, text="💾 Exportar Resultados", command=self._export_results
        ).grid(row=0, column=0, padx=(0, 10))

        ttk.Button(action_frame, text="📋 Copiar Preço", command=self._copy_price).grid(
            row=0, column=1
        )

    def _show_details(self):
        """Mostra detalhes dos itens encontrados"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        if not self.current_result:
            return

        # Treeview para mostrar itens
        columns = ("price", "condition", "title", "date")
        tree = ttk.Treeview(
            self.details_frame, columns=columns, show="headings", height=15
        )

        # Definir cabeçalhos
        tree.heading("price", text="Preço (€)")
        tree.heading("condition", text="Condição")
        tree.heading("title", text="Título")
        tree.heading("date", text="Data")

        # Configurar colunas
        tree.column("price", width=80)
        tree.column("condition", width=100)
        tree.column("title", width=300)
        tree.column("date", width=100)

        # Adicionar dados
        for item in self.current_result.comparable_items:
            tree.insert(
                "",
                tk.END,
                values=(
                    f"{item.price:.2f}",
                    item.condition,
                    item.title[:80] + "..." if len(item.title) > 80 else item.title,
                    item.date,
                ),
            )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.details_frame, orient=tk.VERTICAL, command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.rowconfigure(0, weight=1)

    def _show_charts(self):
        """Mostra gráficos de distribuição de preços"""
        for widget in self.charts_frame.winfo_children():
            widget.destroy()

        if not self.current_result or not self.current_result.comparable_items:
            return

        try:
            # Criar figura matplotlib
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            fig.patch.set_facecolor("#f0f0f0")

            prices = [item.price for item in self.current_result.comparable_items]

            # Histograma
            ax1.hist(prices, bins=10, alpha=0.7, color="skyblue", edgecolor="black")
            ax1.set_title("Distribuição de Preços")
            ax1.set_xlabel("Preço (€)")
            ax1.set_ylabel("Frequência")
            ax1.grid(True, alpha=0.3)

            # Box plot
            ax2.boxplot(prices, vert=True, patch_artist=True)
            ax2.set_title("Box Plot de Preços")
            ax2.set_ylabel("Preço (€)")
            ax2.grid(True, alpha=0.3)

            # Ajustar layout
            plt.tight_layout()

            # Embed no Tkinter
            canvas = FigureCanvasTkAgg(fig, self.charts_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            ttk.Label(
                self.charts_frame, text=f"Erro ao gerar gráficos: {e}", foreground="red"
            ).pack(pady=20)

    def _show_explanation(self):
        """Mostra explicação do raciocínio"""
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)

        if self.current_result and self.current_result.pricing_recommendation:
            rec = self.current_result.pricing_recommendation
            explanation = (
                f"• Preço base calculado: €{rec.base_price:.2f}\n"
                f"• Ajuste por condição: {rec.condition_adjustment * 100:+.1f}%\n"
                f"• Margem de negociação: {rec.negotiation_margin * 100:.1f}%\n"
                f"• Preço final recomendado: €{rec.final_price:.2f}\n\n"
                f"Baseado em {len(self.current_result.comparable_items)} itens similares "
                f"com preços entre €{rec.price_range.min:.2f} e €{rec.price_range.max:.2f}."
            )
            self.explanation_text.insert(1.0, explanation)

        self.explanation_text.config(state=tk.DISABLED)

    def _export_results(self):
        """Exporta resultados para arquivo"""
        # Implementação simplificada
        tk.messagebox.showinfo(
            "Exportar", "Funcionalidade de exportação será implementada aqui."
        )

    def _copy_price(self):
        """Copia preço recomendado para clipboard"""
        if self.current_result:
            price = self.current_result.pricing_recommendation.final_price
            self.clipboard_clear()
            self.clipboard_append(f"€{price:.2f}")
            tk.messagebox.showinfo(
                "Copiado", f"Preço €{price:.2f} copiado para clipboard!"
            )
