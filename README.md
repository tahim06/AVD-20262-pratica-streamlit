# Vagas de tecnologia em 2025 — Dashboards em Streamlit

Projeto da disciplina Análise e Visualização de Dados (CESAR School, 2026.2), Aulas 21 a 23.

App em Streamlit com dois dashboards construídos a partir da minha EDA da Aula 11, feita com o dataset
[Future Jobs & Skills Demand 2025](https://www.kaggle.com/datasets/ahsanneural/future-jobs-and-skills-demand-2025)
(10 mil vagas sintéticas nos setores de IA, Blockchain, Tecnologia Verde e Computação Quântica, licença CC0).

**Link do app:** (preencher após o deploy)

## Dashboards

- **Dashboard 1 – Laboratório de correlação e distribuição:** mapa de calor da correlação de Spearman e um histograma
  por variável quantitativa. Na barra lateral dá para escolher as variáveis e usar os sliders para tirar valores da análise.
- **Dashboard 2 – Indicadores para quem procura vaga:** 4 métricas (vagas, salário mediano, % de vagas remotas e
  % de vagas acima de US$ 200 mil) e 3 gráficos. Clicar em um setor no gráfico de salário filtra as métricas e os outros gráficos.

### Sobre as variáveis do Dashboard 1

O dataset original só tem uma variável numérica (`salary_usd`). Para ter correlação, criei no notebook de tratamento:
porte da empresa em escala (1 a 3), mês e dia da semana da publicação e a quantidade de vagas do mesmo cargo na mesma cidade.
Como o dataset é sintético, as correlações ficam perto de zero, o que confirma o que a EDA já indicava:
nenhuma dessas características influencia o salário.

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

O `data/clean/dataset.csv` já está no repositório. Para gerar de novo, rode o `notebooks/eda-com-downloads.ipynb`.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `app.py` | aplicação (sidebar + as duas abas) |
| `src/data_loader.py` | leitura do CSV tratado com `@st.cache_data` |
| `notebooks/eda.ipynb` | EDA original da Aula 11 |
| `notebooks/eda-com-downloads.ipynb` | download, criação das variáveis e exportação para `data/clean/` |
| `data/clean/dataset.csv` | dataset tratado usado pelo app |
| `.streamlit/config.toml` | identidade visual |
| `entregas/` | rascunhos dos dashboards e justificativa das métricas |
| `prompts/` | declaração de uso de IA |
