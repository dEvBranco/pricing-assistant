🎯 Pricing Assistant
Assistente Inteligente de Precificação para Marketplaces

https://img.shields.io/badge/Python-3.13+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/code%2520style-black-000000.svg

Um assistente pessoal em Python que ajuda a definir preços otimizados para produtos em marketplaces como Vinted, baseado em dados reais de mercado.

https://docs/screenshots/gui-demo.png

✨ Funcionalidades
🔍 Análise de Mercado em Tempo Real

Scraping automático da Vinted

Análise de preços de produtos similares

Filtros por estado e categoria

Deteção automática de relevância

💡 Recomendações Inteligentes

Preço sugerido baseado em mediana de mercado

Margens competitivas e premium

Explicação detalhada do raciocínio

Indicador de confiança baseado em dados

🎨 Interface Moderna

GUI intuitiva com Tkinter

CLI rápida para power users

Temas claro/escuro

Histórico de pesquisas

🌐 Suporte Multilingue

Reconhece produtos em português, francês, espanhol

Filtragem inteligente por relevância

Suporte a múltiplos marketplaces

📊 Relatórios Detalhados

Variação de preços observada

Confiança baseada em dados disponíveis

Histórico de análises

Exportação de resultados

🚀 Começar Rapidamente
Pré-requisitos
Python 3.13 ou superior

Ubuntu 24.04 LTS (ou distribuição Linux similar)

Instalação
Clonar o repositório:

bash
git clone https://github.com/seu-usuario/pricing-assistant.git
cd pricing-assistant
Criar ambiente virtual:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
Instalar dependências:

bash
pip install -r requirements.txt
🖥️ Como Usar
Interface Gráfica (Recomendado)
bash
python src/pricing_assistant/ui/gui_launcher.py
Interface de Linha de Comando
bash
python src/pricing_assistant/ui/cli.py
Como Módulo Python
bash
python -m pricing_assistant
📁 Estrutura do Projeto
text
pricing_assistant/
├── src/pricing_assistant/
│   ├── core/              # Motor de precificação
│   ├── sources/           # Fontes de dados (Vinted, etc.)
│   ├── services/          # Serviços de análise
│   ├── ui/               # Interfaces (GUI + CLI)
│   └── utils/            # Utilidades e configuração
├── tests/                # Testes unitários
├── data/                 # Cache e dados
└── docs/                 # Documentação
🎯 Exemplo de Uso
Na GUI:
Introduza o nome do produto (ex: "t-shirt Nike")

Selecione o estado (Novo, Muito Bom, Bom, Razoável)

Clique em "Analisar Preços"

Veja a análise completa com recomendações

Resultado Típico:
text
✅ ANÁLISE CONCLUÍDA: t-shirt Nike
==================================================

📦 PRODUTO: t-shirt Nike
🏷️  CONDIÇÃO: very_good

💰 PREÇOS ENCONTRADOS: 15
📈 FAIXA DE PREÇOS REAIS: €12.00 - €25.00
📊 PREÇO MÉDIO: €18.50

🎯 RECOMENDAÇÃO DE PREÇO:
   💰 Preço sugerido: €18.50
   📉 Preço mínimo: €15.00
   📈 Preço máximo: €22.00
   🎯 Confiança: 85.0%

🧠 EXPLICAÇÃO:
   • Baseado em 15 preços reais da Vinted
   • Mediana de mercado: €18.50
   • Variação observada: €12.00 - €25.00
   • Ajustado para estado: very_good
   • Margem sugerida: -20% a +20% para negociação
⚙️ Configuração
Edite src/pricing_assistant/utils/config.py para personalizar:

python
# Exemplo de configurações personalizáveis
config = {
    'scraping': {
        'max_pages': 2,
        'delay_between_requests': 1,
        'timeout': 30
    },
    'pricing': {
        'min_confidence': 0.6,
        'negotiation_margin': 0.2
    }
}
🛠️ Desenvolvimento
Executar Testes
bash
python -m pytest tests/
Verificar Código
bash
ruff check src/
mypy src/
Contribuir
Fork o projeto

Crie uma feature branch (git checkout -b feature/AmazingFeature)

Commit das mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📊 Roadmap
Suporte para mais marketplaces (OLX, eBay)

Análise de tendências temporais

Gráficos interativos

API REST

Extensão para navegador

🤝 Contribuições
Contribuições são sempre bem-vindas! Por favor leia o guia de contribuição primeiro.

📄 Licença
Distribuído sob licença MIT. Veja LICENSE para mais informações.

⚠️ Aviso Legal
Este projeto é para fins educacionais e de pesquisa. Os utilizadores são responsáveis por:

Respeitar os termos de serviço dos marketplaces

Implementar rate limiting apropriado

Obter permissões quando necessário

Usar de forma ética e responsável

🆘 Suporte
Encontrou um bug ou tem uma sugestão? Abra uma issue.

Desenvolvido com ❤️ para a comunidade de vendedores online

Precificação inteligente para decisões mais informadas 🎯