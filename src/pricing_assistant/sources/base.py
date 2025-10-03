"""
Interface base para fontes de dados
"""

from abc import ABC, abstractmethod
from typing import List


class MarketDataSource(ABC):
    """Fonte de dados abstrata"""

    @abstractmethod
    def search(self, query: str, **filters) -> List[dict]:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
