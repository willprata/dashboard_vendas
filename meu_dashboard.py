import streamlit as st
import pandas as pd


# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# ESTILO

st.markdown("""
<style>

    /* Fundo geral */
    .stApp {
        background-color: #f4f7fb;
    }

    /* Área principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Título */
    .titulo {
        color: #173b70;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 3px;
    }

    .subtitulo {
        color: #68758a;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Cards */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .card-titulo {
        color: #718096;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .card-valor {
        color: #173b70;
        font-size: 30px;
        font-weight: 700;
    }

    /* Título das seções */
    .secao {
        color: #173b70;
        font-size: 21px;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    section[data-testid="stSidebar"] h1 {
        color: #173b70;
    }

    /* Botão de download */
    .stDownloadButton button {
        background-color: #173b70;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
    }

    .stDownloadButton button:hover {
        background-color: #102b52;
        color: white;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 500;
    }

    /* Remove linha vermelha padrão */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #173b70;
    }

</style>
""", unsafe_allow_html=True)


# CARREGAR DADOS

@st.cache_data
def carregar_dados():

    return pd.read_csv("retail_sales_dataset.csv")


df = carregar_dados()


# CABEÇALHO

st.markdown(
    '<div class="titulo">📊 Dashboard de Vendas</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Visão geral das vendas por categoria e período</div>',
    unsafe_allow_html=True
)


# FILTROS

st.sidebar.title("🎯 Filtros")

st.sidebar.write(
    "Selecione as categorias que deseja visualizar:"
)

lista_de_categorias = df["Product Category"].unique()

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)


# FILTRAR DADOS

df_filtrado = df[
    df["Product Category"].isin(categorias_selecionadas)
].copy()


# MÉTRICAS

receita_calculada = df_filtrado["Total Amount"].sum()

total_pedidos = df_filtrado["Transaction ID"].nunique()


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-titulo">💰 RECEITA TOTAL</div>
            <div class="card-valor">
                R$ {receita_calculada:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-titulo">🛒 TOTAL DE PEDIDOS</div>
            <div class="card-valor">
                {total_pedidos}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ABAS

aba1, aba2 = st.tabs(
    [
        "📈 Evolução Mensal",
        "📋 Tabela de Dados"
    ]
)


# GRÁFICO

with aba1:

    st.markdown(
        '<div class="secao">Evolução das Vendas</div>',
        unsafe_allow_html=True
    )

    df_filtrado["Date"] = pd.to_datetime(
        df_filtrado["Date"]
    )

    dados_agrupados = df_filtrado.groupby(
        df_filtrado["Date"].dt.to_period("M")
    )["Total Amount"].sum()

    dados_agrupados.index = dados_agrupados.index.astype(str)

    st.area_chart(
        dados_agrupados,
        height=450
    )


# TABELA

with aba2:

    st.markdown(
        '<div class="secao">Dados das Vendas</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        height=500
    )

    csv = df_filtrado.to_csv(index=False)

    st.download_button(
        label="⬇️ Baixar dados em CSV",
        data=csv,
        file_name="vendas_filtradas.csv",
        mime="text/csv"
    )
