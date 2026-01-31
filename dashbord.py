import pandas as pd
import plotly.express as px
import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Data Salary Explorer",
    page_icon="💸",
    layout="wide",
)

px.defaults.template = "plotly_dark"
px.defaults.color_continuous_scale = px.colors.sequential.Viridis

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    return pd.read_csv(
        "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
    )

df = carregar_dados()

# Função de filtro
def aplicar_filtro(df, coluna, valores):
    if valores:
        return df[df[coluna].isin(valores)]
    return df


# Opções dos filtros
anos = sorted(df["ano"].unique())
senioridades = sorted(df["senioridade"].unique())
contratos = sorted(df["contrato"].unique())
tamanhos = sorted(df["tamanho_empresa"].unique())

# Inicialização do session_state
if "anos_sel" not in st.session_state:
    st.session_state.anos_sel = anos

if "senioridades_sel" not in st.session_state:
    st.session_state.senioridades_sel = senioridades

if "contratos_sel" not in st.session_state:
    st.session_state.contratos_sel = contratos

if "tamanhos_sel" not in st.session_state:
    st.session_state.tamanhos_sel = tamanhos


# CALLBACK DE RESET 
def resetar_filtros():
    st.session_state.anos_sel = anos
    st.session_state.senioridades_sel = senioridades
    st.session_state.contratos_sel = contratos
    st.session_state.tamanhos_sel = tamanhos

# Sidebar
st.sidebar.title("🔎 Filtros")
st.sidebar.markdown("Refine os dados para explorar padrões salariais.")
# Filtro de ano
st.sidebar.multiselect(
    "📅 Ano",
    anos,
    key="anos_sel"
)
# Filtro de senioridade
st.sidebar.multiselect(
    "🧠 Senioridade",
    senioridades,
    key="senioridades_sel"
)
# Filtro de tipo de contrato
st.sidebar.multiselect(
    "📄 Contrato",
    contratos,
    key="contratos_sel"
)
# Filtro de tamanho da empresa
st.sidebar.multiselect(
    "🏢 Tamanho da empresa",
    tamanhos,
    key="tamanhos_sel"
)
# Botão de reset
st.sidebar.button(
    "🔄 Resetar filtros",
    on_click=resetar_filtros
)

# Aplicação dos filtros
df_filtrado = df.copy()
df_filtrado = aplicar_filtro(df_filtrado, "ano", st.session_state.anos_sel)
df_filtrado = aplicar_filtro(df_filtrado, "senioridade", st.session_state.senioridades_sel)
df_filtrado = aplicar_filtro(df_filtrado, "contrato", st.session_state.contratos_sel)
df_filtrado = aplicar_filtro(df_filtrado, "tamanho_empresa", st.session_state.tamanhos_sel)

# Header
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;">
        <h1 style="color:white;">💸 Data Salary Explorer</h1>
        <p style="color:white; font-size:18px;">
            Descubra padrões, tendências e oportunidades salariais na área de dados.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
# Exibição dos filtros ativos
st.caption(
    f"Filtros ativos → "
    f"Ano: {len(st.session_state.anos_sel)} | "
    f"Senioridade: {len(st.session_state.senioridades_sel)} | "
    f"Contrato: {len(st.session_state.contratos_sel)} | "
    f"Empresa: {len(st.session_state.tamanhos_sel)}"
)



# Visão geral
st.subheader("📌 Visão geral")
# Cálculo das métricas
if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean()
    salario_max = df_filtrado["usd"].max()
    total = len(df_filtrado)
    cargo_top = df_filtrado["cargo"].mode().iloc[0]
else:
    salario_medio = salario_max = total = 0
    cargo_top = "—"
# Exibição das métricas
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Salário médio", f"${salario_medio:,.0f}")
c2.metric("🚀 Salário máximo", f"${salario_max:,.0f}")
c3.metric("📊 Registros", f"{total:,}")
c4.metric("🏆 Cargo mais comum", cargo_top)


# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Análises", "🌍 Geografia", "📋 Dados"])


# TAB 1 - Análises
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        if not df_filtrado.empty:
            top_cargos = (
                df_filtrado
                .groupby("cargo", as_index=False)["usd"]
                .mean()
                .nlargest(10, "usd")
                .sort_values("usd")
            )

            fig_cargos = px.bar(
                top_cargos,
                x="usd",
                y="cargo",
                orientation="h",
                title="Top 10 cargos por salário médio",
                labels={"usd": "Salário médio (USD)", "cargo": ""}
            )
            fig_cargos.update_layout(title_x=0.1)
            st.plotly_chart(fig_cargos, use_container_width=True)
        else:
            st.info("🔎 Ajuste os filtros para visualizar os cargos.")

    with col2:
        if not df_filtrado.empty:
            fig_hist = px.histogram(
                df_filtrado,
                x="usd",
                nbins=30,
                title="Distribuição salarial",
                labels={"usd": "Salário anual (USD)", "count": ""}
            )
            fig_hist.update_layout(title_x=0.1)
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("🔎 Ajuste os filtros para visualizar a distribuição.")

    st.markdown("### 🧠 Insights rápidos")
    st.markdown(
        """
        - Cargos especializados tendem a salários mais altos  
        - Trabalho remoto amplia a faixa salarial  
        - Senioridade impacta fortemente a remuneração  
        """
    )

# TAB 2 Mapa de salários por país
with tab2:
    st.subheader("🌍 Salários por país")

    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']

        if not df_ds.empty:
            media_ds_pais = (
                df_ds
                .groupby('residencia_iso3', as_index=False)['usd']
                .mean()
            )

            fig_map = px.choropleth(
                media_ds_pais,
                locations='residencia_iso3',
                color='usd',
                title='Salário médio de Data Scientist por país',
                labels={'usd': 'Salário médio (USD)'},
                color_continuous_scale='Blues'
            )

            fig_map.update_layout(
                title_x=0.1,
                margin=dict(l=0, r=0, t=50, b=0),
                paper_bgcolor='white',
                geo=dict(
                    bgcolor='white',
                    showframe=False,
                    showcoastlines=True,
                    coastlinecolor='#CCCCCC',
                    showland=True,
                    landcolor='#F3F4F6'
                )
            )

            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("🔎 Nenhum dado de Data Scientist com os filtros atuais.")
    else:
        st.warning("⚠️ Nenhum dado disponível para exibição.")


# TAB 3 - Dados
with tab3:
    st.markdown("### 📋 Base de dados filtrada")
    st.dataframe(df_filtrado, use_container_width=True)
