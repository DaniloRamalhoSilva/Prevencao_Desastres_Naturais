# 🔥 Prevenção de Incêndios Florestais com Machine Learning

Aplicação interativa desenvolvida com **Streamlit** para análise e predição de risco de **incêndios florestais** no Brasil, utilizando dados públicos e técnicas de Machine Learning. A solução também inclui um **assistente IA** baseado em LLM para responder perguntas em linguagem natural sobre o risco de desastres.

---

## 📌 Funcionalidades

### 📊 1. Análise Descritiva
- Filtros interativos por **estado**, **município**, **bioma** e **período**.
- Métricas: média de dias sem chuva, risco médio, total de registros, última data registrada.
- Gráficos de evolução temporal e ranking dos municípios com mais ocorrências.

### 🔮 2. Análise Preditiva
- Modelo de classificação treinado via **PyCaret** para prever o **nível de risco** (Baixo, Médio, Alto, Muito Alto).
- Interface com sliders para **dias sem chuva** e **hora do dia**.
- Cartões de risco com mensagens personalizadas e estilo visual adaptado.

### 🤖 3. Assistente IA (LLM) - (Em fase de desenvolvimento)
- Integração com modelo de linguagem para responder perguntas como:
  - “Qual o município com maior risco nos últimos 30 dias?”
  - “Como evitar incêndios em período seco?”
- Capacidade de combinar dados, predições e sugestões em linguagem natural.

---

## 🧠 Modelo de Machine Learning

- **Biblioteca:** [PyCaret](https://pycaret.gitbook.io/docs/)
- **Tipo de Modelo:** Classificação (Random Forest)
- **Variáveis Consideradas:**
  - Estado, Município, Bioma
  - Número de dias sem chuva
  - Hora do dia
  - Dia da semana

---

## 🗃️ Fonte de Dados

- [TerraBrasilis – Plataforma do INPE](https://terrabrasilis.dpi.inpe.br)
- Dados históricos de focos de calor por bioma e município.

---

## 🚀 Como Executar Localmente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/DaniloRamalhoSilva/Prevencao_Desastres_Naturais.git
   cd Prevencao_Desastres_Naturais
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\\Scripts\\activate no Windows
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o app:**
   ```bash
   streamlit run app.py
   ```

## ☁️ Deploy
O app pode ser publicado gratuitamente usando Streamlit Cloud. Basta conectar este repositório e configurar as variáveis, se necessário.

## 📂 Estrutura do Projeto
   ```bash
   📦 projeto-incendios/
    ├── app.py                          # Arquivo principal com layout e abas
    ├── app_analise_descritiva.py      # Aba de análise descritiva
    ├── app_analise_preditiva.py       # Aba de predição com ML
    ├── app_assistente_ia.py           # Assistente IA com LLM
    ├── app_consideracoes.py           # Aba de considerações finais
    ├── models/
    │   └── pickle_tuned_rf_pycaret3   # Modelo treinado
    ├── data/
    │   └── Risco_Fogo.csv             # Base de dados principal
    ├── requirements.txt
    └── README.md
   ```
## 📈 Resultados Esperados
- Aumento da capacidade de prevenção e monitoramento de desastres ambientais.

- Interface amigável e acessível para tomada de decisão baseada em dados.

- Integração de inteligência artificial para apoiar respostas rápidas e informadas.

## 👨‍🏫 Autores:
- Danilo Ramalho Silva RM: 555183
- João Vitor Pires da Silva RM: 556213
- Israel Dalcin Alves Diniz RM: 554668