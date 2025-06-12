
# Projeto Final - SENAI

Este é um sistema desenvolvido como projeto final do curso no SENAI, utilizando **Python**, **Streamlit**, **SQLite** e **pandas**. O sistema apresenta informações sobre automóveis e aviões, com visualização interativa através de uma interface web.

## 🛠 Tecnologias Utilizadas

- Python 3
- Streamlit
- SQLite
- pandas
- matplotlib (se aplicável)
- Interface com imagens (.png)

## 📁 Estrutura do Projeto

```
projeto_final_senai/
│
├── main.py             # Arquivo principal para rodar o app
├── home.py             # Página inicial
├── air.py              # Página com dados de aviões
├── auto.py             # Página com dados de automóveis
├── database/
│   ├── airplane.db
│   ├── automobile.db
│   ├── airplanes.csv
│   └── automobile.csv
├── carro.png           # Imagem para a página de automóveis
├── logo.png            # Logo do projeto
├── filtros.txt         # Observações sobre filtros
└── persona.txt         # Definição da persona do usuário
```

## ▶️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/rogerymx/projeto_final_senai.git
   cd 'seu-repositorio'
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:
   ```bash
   streamlit run main.py
   ```

## ✅ Funcionalidades

- Navegação entre páginas (home, automóveis, aviões)
- Visualização de dados via gráficos e tabelas
- Filtros interativos para refinar os dados
- Integração com banco de dados SQLite

## 🧑 Persona

Roberto Andrade é CEO da LogCar Air & Mobility, uma empresa do setor de transporte multimodal (aéreo e terrestre). Com 48 anos, ele busca integrar dados logísticos para tomar decisões estratégicas que melhorem a eficiência operacional e orientem investimentos. Seu foco está na análise de desempenho de frotas, consumo de combustível, e visualização clara de indicadores-chave como carga transportada, desempenho por modelo de veículo e eficiência das companhias aéreas.

## 📄 Licença

Este projeto é de uso educacional.
