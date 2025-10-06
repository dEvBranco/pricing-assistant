#!/usr/bin/env python3
import sys

sys.path.insert(0, "src")

from pricing_assistant.services.analysis import AnalysisService
from pricing_assistant.sources.vinted import VintedSource


def main():
    print("🔍 A testar recomendação...")

    data_sources = [VintedSource()]
    service = AnalysisService(data_sources)
    result = service.analyze_product("botas modalfa", "very_good")
    recommendation = result["recommendation"]

    print("🎯 RECOMENDAÇÃO COMPLETA:")
    print(f"Tipo: {type(recommendation)}")
    print("Atributos:")
    for attr in dir(recommendation):
        if not attr.startswith("_"):
            value = getattr(recommendation, attr)
            print(f"  {attr}: {value}")


if __name__ == "__main__":
    main()
