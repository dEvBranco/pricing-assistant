"""
Interface de Linha de Comando - Versão Corrigida
"""

import sys
import os

# Configurar path absoluto
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from pricing_assistant.services.analysis import AnalysisService
from pricing_assistant.utils.config import Config
from pricing_assistant.sources.vinted import VintedSource


def main():
    """Função principal da CLI"""
    print("🎯 Pricing Assistant - CLI Mode")
    print("=" * 40)

    try:
        # Criar data sources
        data_sources = [VintedSource()]
        service = AnalysisService(data_sources=data_sources)
        config = Config()

        # Obter input do usuário
        search_query = input("🔍 Produto para pesquisar: ").strip()

        print("\n📦 Condições disponíveis:")
        print("1 - Novo")
        print("2 - Muito Bom")
        print("3 - Bom")
        print("4 - Razoável")

        condition_choice = input("\nEscolha a condição (1-4): ").strip()
        condition_map = {"1": "new", "2": "very_good", "3": "good", "4": "satisfactory"}

        condition = condition_map.get(condition_choice, "new")

        print(f"\n⏳ Analisando '{search_query}' ({condition})...")

        # Executar análise
        result = service.analyze_product(
            search_query=search_query, condition=condition, max_pages=2
        )

        # Mostrar resultados
        print("\n✅ Análise concluída!")
        print(f"📊 Itens encontrados: {len(result.comparable_items)}")
        print(f"💰 Preço recomendado: €{result.pricing_recommendation.final_price:.2f}")
        print(
            f"📈 Faixa de preços: €{result.pricing_recommendation.price_range.min:.2f} - €{result.pricing_recommendation.price_range.max:.2f}"
        )

    except KeyboardInterrupt:
        print("\n👋 Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("💡 Dica: Execute o assistente de configuração primeiro")


if __name__ == "__main__":
    main()
