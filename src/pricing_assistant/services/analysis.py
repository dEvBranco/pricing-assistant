"""
Serviço de análise
"""

from typing import List
from ..core.pricing_engine import PricingEngine
from ..sources.base import MarketDataSource


class AnalysisService:
    """Serviço principal de análise"""

    def __init__(self, data_sources: List[MarketDataSource]):
        self.data_sources = data_sources
        self.pricing_engine = PricingEngine()

    def analyze_product(self, product_name: str, condition: str = "bom") -> dict:
        """Analisa um produto"""
        print(f"🔍 Analisando: {product_name} ({condition})")

        # Coletar dados de mercado
        market_data = self._collect_market_data(product_name, condition)

        # Calcular preço
        product_info = {"name": product_name, "condition": condition}
        recommendation = self.pricing_engine.calculate_price(product_info, market_data)

        return {
            "product": product_name,
            "condition": condition,
            "recommendation": recommendation,
            "market_data": market_data,
        }

    def _collect_market_data(self, query: str, condition: str) -> dict:
        """Coleta dados de todas as fontes disponíveis"""
        all_prices = []

        for source in self.data_sources:
            if source.is_available():
                try:
                    listings = source.search(query, condition=condition)
                    prices = [item["price"] for item in listings if "price" in item]
                    all_prices.extend(prices)
                    print(f"   ✅ {source.name}: {len(prices)} preços")
                except Exception as e:
                    print(f"   ❌ {source.name}: {e}")

        return {"prices": all_prices}
