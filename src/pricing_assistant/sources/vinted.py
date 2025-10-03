"""
Fonte de dados Vinted - Versão Melhorada com Filtros
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List
from .base import MarketDataSource


class VintedSource(MarketDataSource):
    """Implementação melhorada para Vinted com filtros precisos"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )

    def search(self, query: str, **filters) -> List[dict]:
        """Procura produtos na Vinted com filtros precisos"""
        try:
            print(f"   🌐 A pesquisar na Vinted: '{query}'")
            url = f"https://www.vinted.pt/catalog?search_text={query.replace(' ', '+')}"

            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            listings = self._parse_html(response.text, query)
            filtered_listings = self._filter_relevant(listings, query)

            print(
                f"   ✅ Vinted: {len(filtered_listings)} produtos relevantes de {len(listings)} totais"
            )
            return filtered_listings

        except Exception as e:
            print(f"   ❌ Erro no Vinted: {e}")
            return []

    def _parse_html(self, html: str, original_query: str) -> List[dict]:
        """Parse melhorado do HTML da Vinted"""
        soup = BeautifulSoup(html, "html.parser")
        listings = []

        # Procurar elementos de produtos - selectors mais abrangentes
        product_cards = soup.find_all(
            ["div", "article"],
            class_=lambda x: x
            and any(
                cls in str(x)
                for cls in ["item", "card", "product", "new-item", "feed-grid"]
            ),
        )

        print(f"   🔍 Encontrados {len(product_cards)} elementos de produto")

        for card in product_cards:
            listing = self._extract_product_info(card, original_query)
            if listing and listing.get("price", 0) > 1:  # Preços mínimos realistas
                listings.append(listing)

        return listings

    def _extract_product_info(self, card, original_query: str) -> dict:
        """Extrai informação de produto com validação"""
        try:
            # Extrair título completo
            title = self._extract_title(card)
            if not title or len(title) < 3:
                return None

            # Extrair preço
            price = self._extract_price(card)
            if price <= 1:  # Filtrar preços irrealistas
                return None

            # Validar relevância do produto
            if not self._is_relevant_product(title, original_query):
                return None

            return {
                "title": title[:100],
                "price": price,
                "condition": self._extract_condition(card, title),
                "location": self._extract_location(card),
                "url": self._extract_url(card),
                "posted_date": "Recentemente",
                "relevance_score": self._calculate_relevance(title, original_query),
            }

        except (Exception, AttributeError):
            return None

    def _extract_title(self, card) -> str:
        """Extrai título de múltiplas formas"""
        # Tentar vários selectors
        selectors = [
            card.find("h3"),
            card.find("h4"),
            card.find("h5"),
            card.find(attrs={"data-testid": lambda x: x and "title" in str(x)}),
            card.find(
                attrs={
                    "class": lambda x: x
                    and any(cls in str(x) for cls in ["title", "name", "description"])
                }
            ),
        ]

        for selector in selectors:
            if selector:
                text = selector.get_text(strip=True)
                if text and len(text) > 2:
                    return text

        # Fallback: extrair texto de todo o card e pegar a primeira linha
        card_text = card.get_text(strip=True)
        if card_text:
            lines = [line.strip() for line in card_text.split("\n") if line.strip()]
            return lines[0] if lines else "Produto sem nome"

        return "Produto sem nome"

    def _extract_price(self, card) -> float:
        """Extrai preço de múltiplas formas"""
        # Procurar elementos de preço
        price_selectors = [
            card.find(attrs={"data-testid": lambda x: x and "price" in str(x)}),
            card.find(
                attrs={
                    "class": lambda x: x
                    and any(cls in str(x) for cls in ["price", "amount", "value"])
                }
            ),
            card.find("span", class_=lambda x: x and "€" in str(x)),
        ]

        for selector in price_selectors:
            if selector:
                price_text = selector.get_text(strip=True)
                price = self._clean_price(price_text)
                if price > 0:
                    return price

        # Procurar padrão de preço no texto completo
        card_text = card.get_text()
        price_patterns = [
            r"€\s*(\d+[.,]\d{2})",
            r"(\d+[.,]\d{2})\s*€",
            r"price:\s*€?\s*(\d+[.,]\d{2})",
        ]

        for pattern in price_patterns:
            matches = re.findall(pattern, card_text, re.IGNORECASE)
            if matches:
                price = self._clean_price(matches[0])
                if price > 0:
                    return price

        return 0.0

    def _clean_price(self, price_text: str) -> float:
        """Limpa e converte texto de preço"""
        try:
            # Remover €, espaços e converter vírgulas
            clean = price_text.replace("€", "").replace(" ", "").replace(",", ".")

            # Extrair apenas números e ponto decimal
            clean = re.sub(r"[^\d.]", "", clean)

            # Remover pontos decimais extras (mantém apenas o último)
            parts = clean.split(".")
            if len(parts) > 2:
                clean = parts[0] + "." + "".join(parts[1:])

            return float(clean) if clean else 0.0

        except (ValueError, AttributeError):
            return 0.0

    def _is_relevant_product(self, title: str, query: str) -> bool:
        """Verifica relevância - Versão Multilingue"""
        if not title or not query:
            return False

        title_lower = title.lower()
        query_lower = query.lower()
        query_words = query_lower.split()

        # Traduções e variantes multilingues
        translations = {
            "teclado": ["keyboard", "clavier", "tastiera", "tastatur", "klavye"],
            "apex": ["apex"],  # Mantém igual
            "pro": ["pro", "professional"],
            "v3": ["v3", "version3", "3"],
        }

        # Contar palavras matching considerando traduções
        matching_words = 0
        for query_word in query_words:
            # Verificar palavra original
            if query_word in title_lower:
                matching_words += 1
            else:
                # Verificar traduções
                for translation in translations.get(query_word, []):
                    if translation in title_lower:
                        matching_words += 1
                        break

        # Para produtos específicos como "teclado apex pro v3", aceitar menos matches
        relevance_ratio = matching_words / len(query_words) if query_words else 0

        # DEBUG: Mostrar apenas quando há algum match
        if matching_words > 0:
            print(f"      🔍 RELEVÂNCIA: '{title[:40]}...'")
            print(
                f"      🔍 Matching: {matching_words}/{len(query_words)} (ratio: {relevance_ratio:.2f})"
            )

        # Aceitar produtos com pelo menos 25% de match para produtos específicos
        return relevance_ratio >= 0.25

    def _calculate_relevance(self, title: str, query: str) -> float:
        """Calcula score de relevância (0-1)"""
        title_lower = title.lower()
        query_lower = query.lower()
        query_words = query_lower.split()

        if not query_words:
            return 0.0

        matching_words = sum(1 for word in query_words if word in title_lower)
        return matching_words / len(query_words)

    def _extract_condition(self, card, title: str) -> str:
        """Extrai estado do produto"""
        text = title + " " + card.get_text()
        text_lower = text.lower()

        if any(
            word in text_lower
            for word in ["novo", "nova", "com etiqueta", "new", "selado"]
        ):
            return "novo"
        elif any(
            word in text_lower
            for word in ["muito bom", "excelente", "como novo", "pouco usado"]
        ):
            return "muito bom"
        elif any(
            word in text_lower
            for word in ["bom", "usado", "utilizado", "em bom estado"]
        ):
            return "bom"
        else:
            return "razoável"

    def _extract_location(self, card) -> str:
        """Extrai localização"""
        # Simplificado por agora
        return "Portugal"

    def _extract_url(self, card) -> str:
        """Extrai URL do produto"""
        link = card.find("a", href=True)
        if link and link["href"]:
            return (
                "https://www.vinted.pt" + link["href"]
                if link["href"].startswith("/")
                else link["href"]
            )
        return "https://www.vinted.pt/"

    def _filter_relevant(self, listings: List[dict], query: str) -> List[dict]:
        """Filtra produtos relevantes - critério mais flexível"""
        # Aceitar produtos com relevância baixa mas ordenar pelos mais relevantes
        relevant = [item for item in listings if item.get("relevance_score", 0) >= 0.2]

        # Ordenar por relevância (mais relevante primeiro)
        relevant.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        # Mostrar debug dos produtos encontrados
        if relevant:
            print(f"      📊 Produtos filtrados: {len(relevant)} (de {len(listings)})")
            for i, item in enumerate(relevant[:3]):  # Mostrar top 3
                print(
                    f"      {i + 1}. '{item['title'][:50]}...' - €{item['price']:.2f}"
                )

        return relevant[:10]  # Limitar a 10 produtos

    def is_available(self) -> bool:
        """Verifica se a Vinted está acessível"""
        try:
            response = self.session.head("https://www.vinted.pt", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    @property
    def name(self) -> str:
        return "Vinted"
