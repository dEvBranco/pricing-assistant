#!/usr/bin/env python3
"""
Script de lançamento para o Pricing Assistant
"""

import sys
import os

# Adiciona o src ao path
src_path = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, src_path)


def main():
    try:
        from pricing_assistant import main

        main()
    except ImportError as e:
        print(f"Erro de importação: {e}")
        print("Certifique-se de que a estrutura de pastas está correta.")
        sys.exit(1)


if __name__ == "__main__":
    main()
