"""
Interface de linha de comandos
"""

from ..services.analysis import AnalysisService
from ..sources.vinted import VintedSource


def run_cli():
    """Executa a interface CLI"""
    print("\n🎯 PRICING ASSISTANT")
    print("=" * 50)

    # Inicializar serviços
    sources = [VintedSource()]
    analyzer = AnalysisService(sources)

    while True:
        print("\n📦 O que queres vender?")
        print("💡 Ex: 't-shirt nike', 'teclado', 'cadeira auto'")
        print("❌ 'sair' para terminar")

        produto = input("\n🔍 Produto: ").strip()

        if produto.lower() in ["sair", "exit", "quit"]:
            break

        if not produto:
            continue

        estado = (
            input("📝 Estado (novo/muito bom/bom/razoável) [bom]: ").strip().lower()
        )
        if not estado:
            estado = "bom"

        # Analisar
        try:
            resultado = analyzer.analyze_product(produto, estado)
            mostrar_resultado(resultado)
        except Exception as e:
            print(f"❌ Erro: {e}")

    print("\n👋 Até breve!")


def mostrar_resultado(resultado: dict):
    """Mostra resultados da análise"""
    rec = resultado["recommendation"]

    print(f"\n📊 RESULTADO: {resultado['product'].upper()}")
    print("-" * 40)
    print(f"📝 Estado: {resultado['condition']}")

    if resultado["market_data"]["prices"]:
        prices = resultado["market_data"]["prices"]
        print(f"📈 Mercado: {len(prices)} preços analisados")
        print(f"💰 Variação: €{min(prices):.2f} - €{max(prices):.2f}")

    print("\n💡 RECOMENDAÇÕES:")
    print(f"   🎯 SUGERIDO: €{rec.suggested:.2f}")
    print(f"   ⚡ MÍNIMO: €{rec.minimum:.2f}")
    print(f"   💎 MÁXIMO: €{rec.maximum:.2f}")
    print(f"   🎲 CONFIANÇA: {rec.confidence:.0%}")

    if rec.reasoning:
        print("\n🤔 PORQUÊ:")
        for motivo in rec.reasoning:
            print(f"   • {motivo}")
