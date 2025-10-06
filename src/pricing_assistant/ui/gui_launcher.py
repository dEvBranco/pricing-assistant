#!/usr/bin/env python3
"""
Launcher para a Interface Gráfica do Pricing Assistant
"""

import sys
import logging
from pathlib import Path
import tkinter as tk

# Configurar path absoluto
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent  # src/pricing_assistant/ -> src/
sys.path.insert(0, str(project_root))

try:
    from pricing_assistant.ui.gui.main_window import PricingAssistantGUI
    from pricing_assistant.services.analysis import AnalysisService
    from pricing_assistant.utils.config import Config
    from pricing_assistant.sources.vinted import VintedSource
except ImportError as e:
    print(f"Erro ao importar componentes GUI: {e}")
    print("Falling back para CLI...")
    try:
        from pricing_assistant.ui.cli import main as cli_main

        cli_main()
        sys.exit(0)
    except ImportError:
        print("CLI também falhou. Verifique a estrutura do projeto.")
        sys.exit(1)


def main():
    """Inicia a aplicação GUI"""
    try:
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # Criar e iniciar aplicação
        root = tk.Tk()

        # Criar data sources
        data_sources = [VintedSource()]
        analysis_service = AnalysisService(data_sources=data_sources)

        PricingAssistantGUI(root, analysis_service)
        root.mainloop()

    except Exception as e:
        print(f"Erro fatal na GUI: {e}")
        print("Iniciando CLI como fallback...")
        try:
            from pricing_assistant.ui.cli import main as cli_main

            cli_main()
        except Exception as cli_error:
            print(f"CLI também falhou: {cli_error}")
            sys.exit(1)


if __name__ == "__main__":
    main()
