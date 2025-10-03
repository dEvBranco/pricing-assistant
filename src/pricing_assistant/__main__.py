#!/usr/bin/env python3
import sys
import os

# VERSÃO SUPER-SEGURA - path absoluto explícito
current_dir = os.getcwd()
src_path = os.path.join(current_dir, "src")
sys.path.insert(0, src_path)


def main():
    print("=" * 50)
    print("🎯 PRICING ASSISTANT - PATH FIXED")
    print("=" * 50)

    try:
        from pricing_assistant.ui.cli import run_cli

        print("✅ Módulos carregados com sucesso!")
        print("🚀 Iniciando aplicação...\n")
        run_cli()
    except ImportError as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
