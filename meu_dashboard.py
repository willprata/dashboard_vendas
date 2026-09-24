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

    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    .titulo {
        color: #173b70;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 3px;
    }

    .subtitulo {
        color: #68758a;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .card {
        background-color: white;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }

    .card-titulo {
        color: #718096;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 7px;
    }

    .card-valor {
        color: #173b70;
        font-size: 27px;
        font-weight: 700;
    }

    .secao {
        color: #173b70;
        font-size: 21px;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    .caixa {
        background-color: white;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04);
    }

    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e2e8f0;
    }

    section[data-testid="stSidebar"] h1 {
        color: #173b70;
    }

    .stDownloadButton button {
        background-color: #173b70;
        color: white;
        border: none;
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)


# CARREGAR DADOS

@st.cache_data
def carregar_dados():

    return pd.read_csv("retail_sales_dataset.csv")


df = carregar_dados()


# PREPARAÇÃO DOS DADOS

df["Date"] = pd.to_datetime(df["Date"])


# TÍTULO

st.markdown(
    '<div class="titulo">📊 Dashboard de Vendas</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Análise de vendas, clientes e desempenho por período'
    '</div>',
    unsafe_allow_html=True
)


# SIDEBAR

st.sidebar.title("🎯 Filtros")

st.sidebar.write(
    "Utilize os filtros para analisar os dados."
)


# FILTRO DE CATEGORIA

lista_de_categorias = df["Product Category"].unique()

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)


# FILTRO DE GÊNERO

lista_de_generos = df["Gender"].unique()

generos_selecionados = st.sidebar.multiselect(
    "Gênero",
    options=lista_de_generos,
    default=lista_de_generos
)


# FILTRO DE DATA

data_inicial = df["Date"].min().date()

data_final = df["Date"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_inicial, data_final),
    min_value=data_inicial,
    max_value=data_final
)


# FILTRAR DADOS

df_filtrado = df[
    (df["Product Category"].isin(categorias_selecionadas)) &
    (df["Gender"].isin(generos_selecionados))
].copy()


if len(periodo) == 2:

    data_inicio = pd.to_datetime(periodo[0])
    data_fim = pd.to_datetime(periodo[1])

    df_filtrado = df_filtrado[
        (df_filtrado["Date"] >= data_inicio) &
        (df_filtrado["Date"] <= data_fim)
    ]


# MÉTRICAS

receita_total = df_filtrado["Total Amount"].sum()

total_pedidos = df_filtrado["Transaction ID"].nunique()

quantidade_vendida = df_filtrado["Quantity"].sum()

if total_pedidos > 0:
    ticket_medio = receita_total / total_pedidos
else:
    ticket_medio = 0


# CARDS

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-titulo">💰 RECEITA TOTAL</div>
            <div class="card-valor">
                R$ {receita_total:,.2f}
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


with col3:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-titulo">📦 QUANTIDADE VENDIDA</div>
            <div class="card-valor">
                {quantidade_vendida}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="card">
            <div class="card-titulo">🎟️ TICKET MÉDIO</div>
            <div class="card-valor">
                R$ {ticket_medio:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ESPAÇO

st.write("")


# PRIMEIRA SEÇÃO DE GRÁFICOS

st.markdown(
    '<div class="secao">📈 Desempenho das Vendas</div>',
    unsafe_allow_html=True
)


grafico1, grafico2 = st.columns(2)


# EVOLUÇÃO MENSAL

with grafico1:

    st.markdown(
        '<div class="caixa">',
        unsafe_allow_html=True
    )

    st.write("**Evolução Mensal da Receita**")

    dados_mensais = df_filtrado.groupby(
        df_filtrado["Date"].dt.to_period("M")
    )["Total Amount"].sum()

    dados_mensais.index = dados_mensais.index.astype(str)

    st.area_chart(
        dados_mensais,
        height=320
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# RECEITA POR CATEGORIA

with grafico2:

    st.markdown(
        '<div class="caixa">',
        unsafe_allow_html=True
    )

    st.write("**Receita por Categoria**")

    receita_categoria = df_filtrado.groupby(
        "Product Category"
    )["Total Amount"].sum()

    st.bar_chart(
        receita_categoria,
        height=320
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# SEGUNDA SEÇÃO

st.markdown(
    '<div class="secao">📊 Análise dos Clientes e Produtos</div>',
    unsafe_allow_html=True
)


grafico3, grafico4 = st.columns(2)


# RECEITA POR GÊNERO

with grafico3:

    st.markdown(
        '<div class="caixa">',
        unsafe_allow_html=True
    )

    st.write("**Receita por Gênero**")

    receita_genero = df_filtrado.groupby(
        "Gender"
    )["Total Amount"].sum()

    st.bar_chart(
        receita_genero,
        height=300
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# QUANTIDADE POR CATEGORIA

with grafico4:

    st.markdown(
        '<div class="caixa">',
        unsafe_allow_html=True
    )

    st.write("**Quantidade Vendida por Categoria**")

    quantidade_categoria = df_filtrado.groupby(
        "Product Category"
    )["Quantity"].sum()

    st.bar_chart(
        quantidade_categoria,
        height=300
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# TABELA

st.markdown(
    '<div class="secao">📋 Dados das Vendas</div>',
    unsafe_allow_html=True
)


st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=400
)


# DOWNLOAD

csv = df_filtrado.to_csv(index=False)

st.download_button(
    label="⬇️ Baixar dados filtrados em CSV",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)
