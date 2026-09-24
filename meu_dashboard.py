import streamlit as st
import pandas as pd


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# ESTILO VISUAL - TEMA ESCURO
# =========================================================

st.markdown("""
<style>

    /* Fundo principal */
    .stApp {
        background:
            radial-gradient(
                circle at 80% 10%,
                #183b63 0%,
                #0b1b2d 35%,
                #07111f 100%
            );
        color: #eaf3ff;
    }

    /* Área principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #142b46 0%,
                #0b1d31 100%
            );

        border-right: 1px solid #27496b;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f2f7ff;
    }

    section[data-testid="stSidebar"] p {
        color: #b8cbe0;
    }

    /* Título */
    .titulo-principal {
        color: #f4f8ff;
        font-size: 38px;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .subtitulo {
        color: #9db6d1;
        font-size: 15px;
        margin-bottom: 10px;
    }

    /* Linha abaixo do título */
    .linha-titulo {
        width: 65px;
        height: 4px;

        background: linear-gradient(
            90deg,
            #2196f3,
            #4dd0ff
        );

        border-radius: 10px;

        margin-top: 8px;
        margin-bottom: 22px;
    }

    /* Cards */
    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(25, 61, 99, 0.95),
                rgba(10, 32, 57, 0.98)
            );

        border: 1px solid #28547d;

        border-radius: 16px;

        padding: 20px 22px;

        min-height: 125px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.25);
    }

    [data-testid="stMetric"]:hover {
        border-color: #318ce7;

        box-shadow:
            0 10px 30px rgba(0, 120, 255, 0.18);
    }

    [data-testid="stMetricLabel"] {
        color: #a9c3df !important;

        font-size: 12px !important;

        font-weight: 700 !important;

        letter-spacing: 0.4px;
    }

    [data-testid="stMetricValue"] {
        color: #f5f9ff !important;

        font-size: 28px !important;

        font-weight: 750 !important;
    }

    /* Títulos das seções */
    .titulo-secao {
        color: #eaf4ff;

        font-size: 21px;

        font-weight: 700;

        margin-top: 30px;

        margin-bottom: 12px;
    }

    /* Títulos dos gráficos */
    .titulo-grafico {
        color: #dcecff;

        font-size: 15px;

        font-weight: 700;

        margin-bottom: 8px;
    }

    /* Containers dos gráficos */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(15, 39, 66, 0.70);

        border: 1px solid #254b70;

        border-radius: 15px;
    }

    /* Botão de download */
    .stDownloadButton button {
        background: linear-gradient(
            135deg,
            #0878d1,
            #2196f3
        );

        color: white;

        border: none;

        border-radius: 9px;

        font-weight: 600;
    }

    .stDownloadButton button:hover {
        background: #0a69b7;
        color: white;
    }

    /* Tabela */
    [data-testid="stDataFrame"] {
        border-radius: 12px;

        overflow: hidden;

        border: 1px solid #294d70;
    }

    /* Textos gerais */
    .stMarkdown,
    .stText {
        color: #d9e8f7;
    }

    /* Rodapé */
    .rodape {
        text-align: center;

        color: #718ca8;

        font-size: 12px;

        margin-top: 25px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# CARREGAR DADOS
# =========================================================

@st.cache_data
def carregar_dados():

    dados = pd.read_csv(
        "retail_sales_dataset.csv"
    )

    dados["Date"] = pd.to_datetime(
        dados["Date"]
    )

    return dados


df = carregar_dados()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 📊 Dashboard")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎯 Filtros")

st.sidebar.write(
    "Utilize os filtros para analisar os dados."
)


# =========================================================
# FILTRO DE CATEGORIA
# =========================================================

lista_de_categorias = sorted(
    df["Product Category"].unique()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)


# =========================================================
# FILTRO DE GÊNERO
# =========================================================

lista_de_generos = sorted(
    df["Gender"].unique()
)

generos_selecionados = st.sidebar.multiselect(
    "Gênero",
    options=lista_de_generos,
    default=lista_de_generos
)


# =========================================================
# FILTRO DE DATA
# =========================================================

data_inicial = df["Date"].min().date()

data_final = df["Date"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_inicial, data_final),
    min_value=data_inicial,
    max_value=data_final
)


# =========================================================
# APLICAR FILTROS
# =========================================================

df_filtrado = df[
    (df["Product Category"].isin(categorias_selecionadas))
    &
    (df["Gender"].isin(generos_selecionados))
].copy()


if len(periodo) == 2:

    inicio = pd.to_datetime(
        periodo[0]
    )

    fim = pd.to_datetime(
        periodo[1]
    )

    df_filtrado = df_filtrado[
        (df_filtrado["Date"] >= inicio)
        &
        (df_filtrado["Date"] <= fim)
    ]


# =========================================================
# TÍTULO
# =========================================================

st.markdown(
    '<div class="titulo-principal">📊 Dashboard de Vendas</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="linha-titulo"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Análise de vendas, clientes e desempenho por período'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CÁLCULO DAS MÉTRICAS
# =========================================================

receita_total = df_filtrado[
    "Total Amount"
].sum()

total_pedidos = df_filtrado[
    "Transaction ID"
].nunique()

quantidade_vendida = df_filtrado[
    "Quantity"
].sum()

if total_pedidos > 0:

    ticket_medio = (
        receita_total / total_pedidos
    )

else:

    ticket_medio = 0


# =========================================================
# MÉTRICAS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="💰 Receita Total",
        value=f"R$ {receita_total:,.2f}"
    )


with col2:

    st.metric(
        label="🛒 Total de Pedidos",
        value=total_pedidos
    )


with col3:

    st.metric(
        label="📦 Quantidade Vendida",
        value=quantidade_vendida
    )


with col4:

    st.metric(
        label="🎟️ Ticket Médio",
        value=f"R$ {ticket_medio:,.2f}"
    )


# =========================================================
# SEÇÃO DE DESEMPENHO
# =========================================================

st.markdown(
    '<div class="titulo-secao">'
    '📈 Desempenho das Vendas'
    '</div>',
    unsafe_allow_html=True
)


grafico1, grafico2 = st.columns(2)


# =========================================================
# EVOLUÇÃO MENSAL
# =========================================================

with grafico1:

    st.markdown(
        '<div class="titulo-grafico">'
        'Evolução Mensal da Receita'
        '</div>',
        unsafe_allow_html=True
    )

    dados_mensais = (
        df_filtrado
        .groupby(
            df_filtrado["Date"].dt.to_period("M")
        )["Total Amount"]
        .sum()
    )

    dados_mensais.index = (
        dados_mensais.index.astype(str)
    )

    st.area_chart(
        dados_mensais,
        height=330
    )


# =========================================================
# RECEITA POR CATEGORIA
# =========================================================

with grafico2:

    st.markdown(
        '<div class="titulo-grafico">'
        'Receita por Categoria'
        '</div>',
        unsafe_allow_html=True
    )

    receita_categoria = (
        df_filtrado
        .groupby(
            "Product Category"
        )["Total Amount"]
        .sum()
    )

    st.bar_chart(
        receita_categoria,
        height=330
    )


# =========================================================
# SEGUNDA SEÇÃO
# =========================================================

st.markdown(
    '<div class="titulo-secao">'
    '👥 Análise dos Clientes e Produtos'
    '</div>',
    unsafe_allow_html=True
)


grafico3, grafico4 = st.columns(2)


# =========================================================
# RECEITA POR GÊNERO
# =========================================================

with grafico3:

    st.markdown(
        '<div class="titulo-grafico">'
        'Receita por Gênero'
        '</div>',
        unsafe_allow_html=True
    )

    receita_genero = (
        df_filtrado
        .groupby(
            "Gender"
        )["Total Amount"]
        .sum()
    )

    st.bar_chart(
        receita_genero,
        height=300
    )


# =========================================================
# QUANTIDADE POR CATEGORIA
# =========================================================

with grafico4:

    st.markdown(
        '<div class="titulo-grafico">'
        'Quantidade Vendida por Categoria'
        '</div>',
        unsafe_allow_html=True
    )

    quantidade_categoria = (
        df_filtrado
        .groupby(
            "Product Category"
        )["Quantity"]
        .sum()
    )

    st.bar_chart(
        quantidade_categoria,
        height=300
    )


# =========================================================
# TABELA DE DADOS
# =========================================================

st.markdown(
    '<div class="titulo-secao">'
    '📋 Dados das Vendas'
    '</div>',
    unsafe_allow_html=True
)


st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=400
)


# =========================================================
# DOWNLOAD
# =========================================================

csv = df_filtrado.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Baixar dados filtrados em CSV",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)


# =========================================================
# RODAPÉ
# =========================================================

st.markdown(
    '<div class="rodape">'
    'Dashboard de Vendas • Python + Pandas + Streamlit'
    '</div>',
    unsafe_allow_html=True
)
