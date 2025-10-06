import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from typing import Dict, Any


class PricingAssistantGUI:
    """Janela principal da aplicação Pricing Assistant"""

    def __init__(self, root: tk.Tk, analysis_service):
        self.root = root
        self.analysis_service = analysis_service

        # Setup da janela
        self._setup_window()

        # Histórico
        self.search_history = []

        # Componentes da UI
        self._create_widgets()

        logging.info("Pricing Assistant GUI inicializada")

    def _setup_window(self):
        """Configura a janela principal"""
        self.root.title("🎯 Pricing Assistant - Marketplaces")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Centralizar na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 800) // 2
        y = (self.root.winfo_screenheight() - 600) // 2
        self.root.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title = ttk.Label(
            self.main_frame, text="🎯 Pricing Assistant", font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 20))

        # Campo de pesquisa
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(search_frame, text="Produto:").pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.focus()

        # Condição
        condition_frame = ttk.Frame(self.main_frame)
        condition_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(condition_frame, text="Condição:").pack(side=tk.LEFT, padx=(0, 10))
        self.condition_var = tk.StringVar(value="new")

        conditions = [
            ("Novo", "new"),
            ("Muito Bom", "very_good"),
            ("Bom", "good"),
            ("Razoável", "satisfactory"),
        ]
        for text, value in conditions:
            rb = ttk.Radiobutton(
                condition_frame, text=text, variable=self.condition_var, value=value
            )
            rb.pack(side=tk.LEFT, padx=(0, 10))

        # Configurações avançadas
        advanced_frame = ttk.LabelFrame(self.main_frame, text="Configurações Avançadas")
        advanced_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(advanced_frame, text="Máx. Páginas:").pack(side=tk.LEFT, padx=(0, 10))
        self.pages_var = tk.IntVar(value=2)
        pages_spin = ttk.Spinbox(
            advanced_frame, from_=1, to=5, textvariable=self.pages_var, width=5
        )
        pages_spin.pack(side=tk.LEFT)

        # Botão analisar
        self.analyze_btn = ttk.Button(
            self.main_frame, text="🎯 Analisar Preços", command=self._start_analysis
        )
        self.analyze_btn.pack(pady=20)

        # Área de resultados
        results_frame = ttk.LabelFrame(self.main_frame, text="📊 Resultados")
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Notebook para abas
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Aba de Recomendações
        self.recommendations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.recommendations_frame, text="💡 Recomendações")

        # Aba de Detalhes
        self.details_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.details_frame, text="📋 Detalhes")

        # Text area para resultados
        self.results_text = tk.Text(
            self.recommendations_frame, wrap=tk.WORD, height=15, state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview para detalhes
        columns = ("price", "condition", "title")
        self.tree = ttk.Treeview(
            self.details_frame, columns=columns, show="headings", height=15
        )

        # Definir cabeçalhos
        self.tree.heading("price", text="Preço (€)")
        self.tree.heading("condition", text="Condição")
        self.tree.heading("title", text="Título")

        # Configurar colunas
        self.tree.column("price", width=80)
        self.tree.column("condition", width=100)
        self.tree.column("title", width=400)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status bar
        self.status_var = tk.StringVar(value="Pronto para analisar")
        status_bar = ttk.Label(
            self.main_frame, textvariable=self.status_var, relief="sunken"
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))

        # Bind Enter key
        self.search_entry.bind("<Return>", lambda e: self._start_analysis())

    def _start_analysis(self):
        """Inicia análise do produto"""
        search_query = self.search_entry.get().strip()

        if not search_query:
            messagebox.showwarning(
                "Campo Vazio", "Por favor, insira um produto para pesquisar."
            )
            self.search_entry.focus()
            return

        product_data = {
            "search_query": search_query,
            "condition": self.condition_var.get(),
            "max_pages": self.pages_var.get(),
        }

        self.status_var.set("Analisando produto...")
        self.analyze_btn.config(state="disabled")

        # Limpar resultados anteriores
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "⏳ Analisando preços...\n")
        self.results_text.config(state=tk.DISABLED)

        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thread para não bloquear a UI
        thread = threading.Thread(
            target=self._perform_analysis, args=(product_data,), daemon=True
        )
        thread.start()

    def _perform_analysis(self, product_data: Dict[str, Any]):
        """Executa análise em background"""
        try:
            # Usar o serviço existente
            analysis_result = self.analysis_service.analyze_product(
                product_data["search_query"], product_data["condition"]
            )

            # Atualizar UI na thread principal
            self.root.after(0, self._on_analysis_success, analysis_result, product_data)

        except Exception as e:
            error_msg = f"Erro na análise: {str(e)}"
            logging.error(error_msg)
            self.root.after(0, self._on_analysis_error, error_msg)

        except Exception as e:
            error_msg = f"Erro na análise: {str(e)}"
            logging.error(error_msg)
            self.root.after(0, self._on_analysis_error, error_msg)

    def _on_analysis_success(self, result, product_data):
        """Callback para análise bem-sucedida - VERSÃO CORRIGIDA"""
        self.analyze_btn.config(state="normal")
        self.status_var.set("Análise concluída com sucesso")

        # Acessar dados da estrutura REAL
        market_data = result.get("market_data", {})
        prices = market_data.get("prices", [])

        # Adicionar ao histórico
        history_item = {
            **product_data,
            "timestamp": "N/A",
            "result_summary": f"{len(prices)} preços encontrados",
        }
        self.search_history.insert(0, history_item)

        # Limitar histórico
        if len(self.search_history) > 10:
            self.search_history = self.search_history[:10]

        # Atualizar display
        self._show_results(result)

        # Mostrar notificação
        messagebox.showinfo(
            "Análise Concluída",
            f"Encontrados {len(prices)} preços para '{result.get('product', 'N/A')}'",
        )

    def _on_analysis_error(self, error_msg: str):
        """Callback para erro na análise"""
        self.analyze_btn.config(state="normal")
        self.status_var.set("Erro na análise")

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"❌ ERRO: {error_msg}")
        self.results_text.config(state=tk.DISABLED)

        messagebox.showerror("Erro na Análise", error_msg)

    def _show_results(self, result):
        """Mostra os resultados da análise - VERSÃO FINAL COMPLETA"""
        # Acessar os dados da estrutura REAL
        product_name = result.get("product", "N/A")
        condition = result.get("condition", "N/A")
        recommendation = result.get("recommendation", {})
        market_data = result.get("market_data", {})

        prices = market_data.get("prices", [])

        # Atualizar texto dos resultados
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        text = f"✅ ANÁLISE CONCLUÍDA: {product_name}\n"
        text += "=" * 50 + "\n\n"

        # Informações básicas
        text += f"📦 PRODUTO: {product_name}\n"
        text += f"🏷️  CONDIÇÃO: {condition}\n\n"

        # Preços encontrados
        text += f"💰 PREÇOS ENCONTRADOS: {len(prices)}\n"
        if prices:
            text += (
                f"📈 FAIXA DE PREÇOS REAIS: €{min(prices):.2f} - €{max(prices):.2f}\n"
            )
            text += f"📊 PREÇO MÉDIO: €{sum(prices) / len(prices):.2f}\n\n"
        else:
            text += "⚠️  Nenhum preço encontrado para análise\n\n"

        # RECOMENDAÇÃO COMPLETA - AGORA COM TODOS OS DADOS!
        text += "🎯 RECOMENDAÇÃO DE PREÇO:\n"

        if recommendation and hasattr(recommendation, "suggested"):
            # Preços recomendados
            text += f"   💰 Preço sugerido: €{getattr(recommendation, 'suggested', 0):.2f}\n"
            text += (
                f"   📉 Preço mínimo: €{getattr(recommendation, 'minimum', 0):.2f}\n"
            )
            text += (
                f"   📈 Preço máximo: €{getattr(recommendation, 'maximum', 0):.2f}\n"
            )
            text += f"   🎯 Confiança: {getattr(recommendation, 'confidence', 0) * 100:.1f}%\n\n"

            # Explicação do raciocínio
            reasoning = getattr(recommendation, "reasoning", [])
            if reasoning:
                text += "🧠 EXPLICAÇÃO:\n"
                for line in reasoning:
                    text += f"   • {line}\n"
        else:
            text += "   • (Recomendação não disponível)\n"

        self.results_text.insert(tk.END, text)
        self.results_text.config(state=tk.DISABLED)

        # Limpar treeview anterior
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Atualizar treeview com preços reais
        for i, price in enumerate(prices, 1):
            self.tree.insert(
                "",
                tk.END,
                values=(f"{price:.2f}", condition, f"{product_name} - Preço {i}"),
            )
