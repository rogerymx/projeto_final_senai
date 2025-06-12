
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
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
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

Veja `persona.txt` para uma descrição do público-alvo do sistema.

## 📄 Licença

Este projeto é de uso educacional.
