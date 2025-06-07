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

### 🤖 3. Assistente IA (LLM)
- Integração com modelo de linguagem para responder perguntas como:
  - “Qual o município com maior risco nos últimos 30 dias?”
  - “Como evitar incêndios em período seco?”
- Capacidade de combinar dados, predições e sugestões em linguagem natural.

### 📝 4. Considerações
- Aba dedicada a anotações, conclusões e próximos passos sem interferência dos filtros.

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
   git clone https://github.com/seu-usuario/projeto-incendios.git
   cd projeto-incendios
