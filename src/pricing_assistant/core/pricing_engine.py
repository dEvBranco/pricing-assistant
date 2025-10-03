"""
Motor de precificação - Lógica central MELHORADA
"""

from dataclasses import dataclass
from typing import List
import statistics


@dataclass
class PriceRecommendation:
    """Recomendação de preço"""

    suggested: float
    minimum: float
    maximum: float
    confidence: float
    reasoning: List[str]


class PricingEngine:
    """Motor principal de precificação - Versão Melhorada"""

    def calculate_price(
        self, product_info: dict, market_data: dict
    ) -> PriceRecommendation:
        """Calcula preço baseado em dados de mercado - algoritmo melhorado"""

        if not market_data.get("prices"):
            return self._get_fallback_price(product_info)

        prices = market_data["prices"]

        # Remover outliers
        clean_prices = self._remove_outliers(prices)

        if not clean_prices:
            return self._get_fallback_price(product_info)

        # Usar mediana (mais robusta que média)
        median_price = statistics.median(clean_prices)

        # Ajustar baseado no estado
        condition = product_info.get("condition", "bom")
        multiplier = self._get_condition_multiplier(condition)
        suggested = median_price * multiplier

        # Calcular margens mais inteligentes
        min_price = min(clean_prices)
        max_price = max(clean_prices)

        return PriceRecommendation(
            suggested=round(suggested, 2),
            minimum=round(
                max(min_price, suggested * 0.7), 2
            ),  # Não abaixo do mínimo de mercado
            maximum=round(
                min(max_price, suggested * 1.4), 2
            ),  # Não acima do máximo de mercado
            confidence=min(0.95, len(clean_prices) / 15),
            reasoning=[
                f"Baseado em {len(clean_prices)} preços reais da Vinted",
                f"Mediana de mercado: {median_price:.2f}€",
                f"Variação observada: {min_price:.2f}€ - {max_price:.2f}€",
                f"Ajustado para estado: {condition}",
                "Margem sugerida: -30% a +40% para negociação",
            ],
        )

    def _remove_outliers(self, prices: List[float]) -> List[float]:
        """Remove outliers usando IQR method"""
        if len(prices) < 4:
            return prices

        prices_sorted = sorted(prices)
        Q1 = prices_sorted[len(prices_sorted) // 4]
        Q3 = prices_sorted[3 * len(prices_sorted) // 4]
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        return [p for p in prices if lower_bound <= p <= upper_bound]

    def _get_fallback_price(self, product_info: dict) -> PriceRecommendation:
        """Preço fallback quando não há dados"""
        base_prices = {"novo": 25.0, "muito bom": 20.0, "bom": 15.0, "razoável": 10.0}

        condition = product_info.get("condition", "bom")
        base = base_prices.get(condition, 15.0)

        return PriceRecommendation(
            suggested=base,
            minimum=base * 0.7,
            maximum=base * 1.3,
            confidence=0.3,
            reasoning=["Dados de mercado não disponíveis", f"Preço base: {condition}"],
        )

    def _get_condition_multiplier(self, condition: str) -> float:
        """Multiplicador baseado no estado"""
        return {
            "novo": 1.3,  # +30% para produtos novos
            "muito bom": 1.1,  # +10% para muito bom estado
            "bom": 1.0,  # Preço base para bom estado
            "razoável": 0.7,  # -30% para razoável
        }.get(condition, 1.0)
