import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(page_title="Vagas de Tecnologia 2025", page_icon="💼", layout="wide")

st.title("Vagas de tecnologia em 2025: salários e demanda")
st.caption("Dataset Future Jobs & Skills Demand 2025 (Kaggle, dados sintéticos) com 10 mil vagas em quatro setores.")

df = load_data()

# Paleta da EDA
ROXO = "#2d223a"
ROXO_MEDIO = "#5b3f8c"
ROSE = "#d4a5a0"
CORES_MODALIDADE = alt.Scale(domain=["Remoto", "Presencial"], range=[ROXO_MEDIO, ROSE])

# Variáveis quantitativas do Dashboard 1 (as derivadas foram criadas no notebook de tratamento)
NOMES = {
    "salary_usd": "Salário anual (USD)",
    "porte_empresa_num": "Porte da empresa (1 a 3)",
    "mes_publicacao": "Mês de publicação",
    "dia_semana_num": "Dia da semana (1 = seg)",
    "demanda_cargo_cidade": "Vagas do mesmo cargo na cidade",
}
VARS_QUANT = list(NOMES)


def br(valor, casas=0):
    """Formata número no padrão brasileiro (1.234,5)."""
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Filtros")

    setores = st.multiselect("Setores", sorted(df["setor"].unique()), default=sorted(df["setor"].unique()))
    cidades = st.multiselect("Cidades", sorted(df["cidade"].unique()), default=sorted(df["cidade"].unique()))

    st.divider()
    st.subheader("Laboratório (Dashboard 1)")

    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        format_func=NOMES.get,
    )

    separar_modalidade = st.toggle("Separar histogramas por modalidade", value=False)

    st.caption("Use os intervalos para tirar valores da análise e ver se a correlação muda.")
    intervalos = {}
    for var in variaveis:
        minimo, maximo = int(df[var].min()), int(df[var].max())
        passo = 1000 if var == "salary_usd" else 1
        intervalos[var] = st.slider(
            NOMES[var],
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

df_filtrado = df[df["setor"].isin(setores) & df["cidade"].isin(cidades)]
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(f"{br(len(df_filtrado))} de {br(len(df))} vagas dentro dos filtros.")

aba1, aba2 = st.tabs(["Dashboard 1: correlação e distribuição", "Dashboard 2: indicadores para quem procura vaga"])


# ---------------- Dashboard 1 ----------------
with aba1:
    col_corr, col_dist = st.columns([1, 1.4])

    with col_corr:
        st.subheader("Correlação de Spearman")

        if len(variaveis) < 2:
            st.info("Escolha pelo menos 2 variáveis na barra lateral para calcular a correlação.")
        elif len(df_filtrado) < 30:
            st.warning("Menos de 30 vagas nos filtros atuais. Amplie os intervalos para calcular a correlação.")
        else:
            corr = df_filtrado[variaveis].corr(method="spearman")
            nomes_ordem = [NOMES[v] for v in variaveis]
            corr.index = corr.columns = nomes_ordem

            corr_longa = corr.stack().reset_index()
            corr_longa.columns = ["linha", "coluna", "rho"]

            # só o triângulo de baixo, sem a diagonal
            pos = {nome: i for i, nome in enumerate(nomes_ordem)}
            corr_longa = corr_longa[corr_longa["linha"].map(pos) > corr_longa["coluna"].map(pos)]

            base = alt.Chart(corr_longa).encode(
                x=alt.X("coluna:N", sort=nomes_ordem[:-1], title=None, axis=alt.Axis(labelAngle=-30, labelLimit=160)),
                y=alt.Y("linha:N", sort=nomes_ordem[1:], title=None, axis=alt.Axis(labelLimit=180)),
            )
            mapa = base.mark_rect(stroke="white").encode(
                color=alt.Color(
                    "rho:Q",
                    title="ρ",
                    scale=alt.Scale(scheme="purpleorange", domain=[-1, 1], reverse=True),
                ),
                tooltip=[
                    alt.Tooltip("linha:N", title="Variável"),
                    alt.Tooltip("coluna:N", title="Com"),
                    alt.Tooltip("rho:Q", title="Spearman", format=".2f"),
                ],
            )
            textos = base.mark_text(fontSize=14).encode(
                text=alt.Text("rho:Q", format=".2f"),
                color=alt.condition("abs(datum.rho) > 0.5", alt.value("white"), alt.value(ROXO)),
            )
            st.altair_chart((mapa + textos).properties(height=380), width="stretch")

            maior = corr_longa.loc[corr_longa["rho"].abs().idxmax()]
            st.caption(
                f"Maior correlação em módulo: {maior['linha']} × {maior['coluna']} (ρ = {br(maior['rho'], 2)}). "
                "Abaixo de 0,3 em módulo a relação é considerada fraca."
            )

    with col_dist:
        st.subheader("Distribuição")

        if not variaveis:
            st.info("Escolha pelo menos 1 variável para ver a distribuição.")
        elif df_filtrado.empty:
            st.warning("Nenhuma vaga dentro dos filtros atuais.")
        else:
            for i in range(0, len(variaveis), 2):
                colunas = st.columns(2)
                for coluna, var in zip(colunas, variaveis[i:i + 2]):
                    # variáveis com poucos valores ficam melhores com uma barra por valor
                    poucos_valores = df_filtrado[var].nunique() <= 12
                    eixo_x = (
                        alt.X(f"{var}:O", title=NOMES[var], axis=alt.Axis(labelAngle=0))
                        if poucos_valores
                        else alt.X(f"{var}:Q", bin=alt.Bin(maxbins=20), title=NOMES[var])
                    )
                    hist = alt.Chart(df_filtrado[[var, "modalidade"]]).mark_bar().encode(
                        x=eixo_x,
                        y=alt.Y("count()", title="Vagas"),
                        tooltip=[alt.Tooltip("count()", title="Vagas")],
                    ).properties(height=210)

                    if separar_modalidade:
                        hist = hist.encode(
                            color=alt.Color("modalidade:N", scale=CORES_MODALIDADE, title="Modalidade",
                                            legend=alt.Legend(orient="top")),
                            tooltip=["modalidade", alt.Tooltip("count()", title="Vagas")],
                        )
                    else:
                        hist = hist.mark_bar(color=ROXO_MEDIO)

                    with coluna:
                        st.altair_chart(hist, width="stretch")


# ---------------- Dashboard 2 ----------------
with aba2:
    st.markdown(
        "Para estudantes e profissionais de tecnologia que estão decidindo em qual setor e cidade procurar vaga. "
        "Clique em uma barra do primeiro gráfico para ver os números só daquele setor (clique de novo no fundo para limpar)."
    )

    if df_filtrado.empty:
        st.warning("Nenhuma vaga dentro dos filtros atuais. Ajuste a barra lateral.")
    else:
        area_kpis = st.container()
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**Salário mediano por setor**")
            clique = alt.selection_point(name="setor_sel", fields=["setor"])
            por_setor = df_filtrado.groupby("setor", as_index=False).agg(
                mediana=("salary_usd", "median"), vagas=("salary_usd", "size")
            )
            barras_setor = alt.Chart(por_setor).mark_bar(color=ROXO_MEDIO).encode(
                x=alt.X("mediana:Q", title="Salário mediano (USD)", axis=alt.Axis(format="$,.0f")),
                y=alt.Y("setor:N", sort="-x", title=None),
                opacity=alt.condition(clique, alt.value(1), alt.value(0.35)),
                tooltip=[
                    alt.Tooltip("setor:N", title="Setor"),
                    alt.Tooltip("mediana:Q", title="Mediana", format="$,.0f"),
                    alt.Tooltip("vagas:Q", title="Vagas"),
                ],
            ).add_params(clique).properties(height=260)

            evento = st.altair_chart(barras_setor, key="grafico_setor", on_select="rerun", width="stretch")

        setores_clicados = [item["setor"] for item in evento.selection.get("setor_sel", [])]
        df_d2 = df_filtrado[df_filtrado["setor"].isin(setores_clicados)] if setores_clicados else df_filtrado
        recorte = ", ".join(setores_clicados) if setores_clicados else "todos os setores filtrados"

        with col_b:
            st.markdown(f"**Vagas por cidade e modalidade** ({recorte})")
            barras_cidade = alt.Chart(df_d2).mark_bar().encode(
                x=alt.X("count()", title="Vagas"),
                y=alt.Y("cidade:N", sort="-x", title=None),
                color=alt.Color("modalidade:N", scale=CORES_MODALIDADE, title="Modalidade",
                                legend=alt.Legend(orient="bottom")),
                tooltip=["cidade", "modalidade", alt.Tooltip("count()", title="Vagas")],
            ).properties(height=260)
            st.altair_chart(barras_cidade, width="stretch")

        st.markdown(f"**Vagas por faixa salarial e porte da empresa** ({recorte})")
        barras_faixa = alt.Chart(df_d2).mark_bar().encode(
            x=alt.X("faixa_salarial:N", title="Faixa salarial (USD)",
                    sort=["50-100 mil", "100-150 mil", "150-200 mil", "200-250 mil"], axis=alt.Axis(labelAngle=0)),
            xOffset=alt.XOffset("porte_empresa:N", sort=["Pequena", "Média", "Grande"]),
            y=alt.Y("count()", title="Vagas"),
            color=alt.Color("porte_empresa:N", title="Porte", sort=["Pequena", "Média", "Grande"],
                            scale=alt.Scale(range=[ROSE, "#9b7bb8", ROXO])),
            tooltip=["faixa_salarial", "porte_empresa", alt.Tooltip("count()", title="Vagas")],
        ).properties(height=280)
        st.altair_chart(barras_faixa, width="stretch")

        # KPIs ficam no topo, mas são calculados depois para já considerar o clique no gráfico
        with area_kpis:
            mediana_geral = df_filtrado["salary_usd"].median()
            mediana_recorte = df_d2["salary_usd"].median()
            pct_remoto_geral = (df_filtrado["modalidade"] == "Remoto").mean() * 100
            pct_remoto = (df_d2["modalidade"] == "Remoto").mean() * 100
            pct_acima_200 = (df_d2["salary_usd"] >= 200_000).mean() * 100
            cargo_top = df_d2["cargo"].value_counts()

            delta_salario = delta_remoto = None
            if setores_clicados:
                var_salario = (mediana_recorte / mediana_geral - 1) * 100
                var_remoto = pct_remoto - pct_remoto_geral
                delta_salario = f"{'+' if var_salario >= 0 else ''}{br(var_salario, 1)}% vs. filtro geral"
                delta_remoto = f"{'+' if var_remoto >= 0 else ''}{br(var_remoto, 1)} p.p. vs. filtro geral"

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Vagas", br(len(df_d2)))
            k2.metric("Salário mediano", f"US$ {br(mediana_recorte)}", delta=delta_salario)
            k3.metric("Vagas remotas", f"{br(pct_remoto, 1)}%", delta=delta_remoto)
            k4.metric("Vagas pagando US$ 200 mil ou mais", f"{br(pct_acima_200, 1)}%")
            st.caption(f"Cargo com mais vagas no recorte: {cargo_top.index[0]} ({cargo_top.iloc[0]} vagas).")
