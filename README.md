# 💸 Data Salary Explorer

Dashboard interativo desenvolvido com **Streamlit** para explorar **padrões salariais na área de dados**, permitindo análises por ano, senioridade, tipo de contrato, tamanho da empresa e localização geográfica.

O projeto consome dados públicos via CSV e apresenta métricas, gráficos interativos e mapas para facilitar a tomada de insights.

---

## 🚀 Funcionalidades

- 🔎 Filtros dinâmicos por:
  - Ano
  - Senioridade
  - Tipo de contrato
  - Tamanho da empresa
- 📊 Métricas principais:
  - Salário médio
  - Salário máximo
  - Total de registros
  - Cargo mais comum
- 📈 Visualizações:
  - Top 10 cargos por salário médio
  - Distribuição salarial
  - Mapa mundial com salário médio de **Data Scientist**
- 📋 Visualização da base de dados filtrada
- ⚡ Cache de dados para melhor performance

---

## 🧠 Tecnologias utilizadas

- Python 3.10+
- Streamlit
- Pandas
- Plotly Express

---

## 📦 Estrutura do projeto

```
.
├── app.py
├── README.md
├── requirements.txt
└── venv/
```

---

## 🛠️ Configuração do ambiente virtual

### Criar o venv
```bash
python -m venv venv
```

### Ativar o venv

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

---

## 📥 Instalação das dependências

```bash
pip install -r requirements.txt
```

Arquivo `requirements.txt`:

```txt
streamlit
pandas
plotly
```

---

## ▶️ Executando a aplicação

```bash
streamlit run app.py
```

Acesse em:
http://localhost:8501

---

## 🌐 Fonte dos dados

Os dados são carregados automaticamente via CSV público hospedado no GitHub.

---

## ❤️ Créditos

Projeto criado com ❤️ usando Streamlit & Plotly.
