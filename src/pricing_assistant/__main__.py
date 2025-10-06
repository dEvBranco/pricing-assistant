"""
Ponto de entrada principal do Pricing Assistant
"""

import sys
import os

# Adiciona o src ao path do Python
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)  # sobe para src/
sys.path.insert(0, src_dir)


def main():
    """Inicia a aplicação (GUI com fallback para CLI)"""
    try:
        # Tentar GUI primeiro
        from pricing_assistant.ui.gui_launcher import main as gui_main

        gui_main()
    except Exception as e:
        print(f"Erro ao iniciar GUI: {e}")
        print("Tentando CLI...")
        try:
            from pricing_assistant.ui.cli import main as cli_main

            cli_main()
        except Exception as cli_error:
            print(f"Erro ao iniciar CLI: {cli_error}")
            print("Verifique a instalação do projeto.")
            sys.exit(1)


if __name__ == "__main__":
    main()
