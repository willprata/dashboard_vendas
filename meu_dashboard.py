import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown("""
<style>

    /* FUNDO PRINCIPAL */
    .stApp {
        background: #071b2e;
        color: #ffffff;
    }

    /* ÁREA PRINCIPAL */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #0b2944;
        border-right: 1px solid #21496d;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* TÍTULO */
    .titulo {
        font-size: 42px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .subtitulo {
        font-size: 16px;
        color: #9fc4e8;
        margin-bottom: 25px;
    }

    .linha-titulo {
        width: 65px;
        height: 4px;
        background: #29b6f6;
        border-radius: 10px;
        margin-bottom: 25px;
    }

    /* CARDS */
    .cards-container {
        display: flex;
        gap: 16px;
        margin-bottom: 35px;
    }

    .card {
        flex: 1;
        background: #103553;
        border: 1px solid #235b83;
        border-radius: 16px;
        padding: 22px;
        min-height: 125px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.20);
    }

    .card-titulo {
        font-size: 14px;
        color: #9fc4e8;
        margin-bottom: 12px;
    }

    .card-valor {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }

    /* TÍTULOS DAS SEÇÕES */
    .secao {
        font-size: 23px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .grafico-titulo {
        font-size: 16px;
        font-weight: 600;
        color: #d7eaff;
        margin-bottom: 8px;
    }

    /* CAIXAS DOS GRÁFICOS */
    .grafico-box {
        background: #0e2d49;
        border: 1px solid #1d4d70;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 25px;
    }

    /* TEXTO DA SIDEBAR */
    .sidebar-titulo {
        font-size: 23px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .sidebar-texto {
        font-size: 14px;
        color: #a9c9e5;
        line-height: 1.6;
    }

    /* TABELA */
    .tabela-titulo {
        font-size: 23px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 20px;
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARREGAR DADOS
# ============================================================

@st.cache_data
def carregar_dados():
    return pd.read_csv("retail_sales_dataset.csv")


df = carregar_dados()

df["Date"] = pd.to_datetime(df["Date"])


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("""
<div class="sidebar-titulo">📊 Dashboard</div>
<hr>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-titulo">🎯 Filtros</div>

<div class="sidebar-texto">
Utilize os filtros para analisar os dados.
</div>
""", unsafe_allow_html=True)


# FILTRO DE CATEGORIA

lista_de_categorias = sorted(
    df["Product Category"].unique()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)


# FILTRO DE GÊNERO

lista_de_generos = sorted(
    df["Gender"].unique()
)

generos_selecionados = st.sidebar.multiselect(
    "Gênero",
    options=lista_de_generos,
    default=lista_de_generos
)


# FILTRO DE DATA

data_inicial = df["Date"].min()
data_final = df["Date"].max()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_inicial, data_final),
    min_value=data_inicial,
    max_value=data_final
)


# ============================================================
# APLICAR FILTROS
# ============================================================

df_filtrado = df[
    df["Product Category"].isin(categorias_selecionadas)
    & df["Gender"].isin(generos_selecionados)
].copy()


if len(periodo) == 2:

    data_inicio = pd.to_datetime(periodo[0])
    data_fim = pd.to_datetime(periodo[1])

    df_filtrado = df_filtrado[
        (df_filtrado["Date"] >= data_inicio)
        & (df_filtrado["Date"] <= data_fim)
    ]


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="titulo">📊 Dashboard de Vendas</div>',
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


# ============================================================
# CÁLCULO DAS MÉTRICAS
# ============================================================

receita_total = df_filtrado["Total Amount"].sum()

total_pedidos = df_filtrado["Transaction ID"].nunique()

quantidade_vendida = df_filtrado["Quantity"].sum()

if total_pedidos > 0:
    ticket_medio = receita_total / total_pedidos
else:
    ticket_medio = 0


# ============================================================
# CARDS
# ============================================================

st.markdown(f"""
<div class="cards-container">

    <div class="card">
        <div class="card-titulo">💰 RECEITA TOTAL</div>
        <div class="card-valor">R$ {receita_total:,.2f}</div>
    </div>

    <div class="card">
        <div class="card-titulo">🛒 TOTAL DE PEDIDOS</div>
        <div class="card-valor">{total_pedidos}</div>
    </div>

    <div class="card">
        <div class="card-titulo">📦 QUANTIDADE VENDIDA</div>
        <div class="card-valor">{quantidade_vendida}</div>
    </div>

    <div class="card">
        <div class="card-titulo">🎟️ TICKET MÉDIO</div>
        <div class="card-valor">R$ {ticket_medio:,.2f}</div>
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# DESEMPENHO
# ============================================================

st.markdown(
    '<div class="secao">📈 Desempenho das Vendas</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# GRÁFICO 1 - EVOLUÇÃO MENSAL
# ============================================================

with col1:

    st.markdown(
        '<div class="grafico-titulo">'
        'Evolução Mensal da Receita'
        '</div>',
        unsafe_allow_html=True
    )

    dados_mensais = (
        df_filtrado
        .groupby(df_filtrado["Date"].dt.strftime("%Y-%m"))["Total Amount"]
        .sum()
        .reset_index()
    )

    dados_mensais.columns = ["Mês", "Receita"]

    grafico_linha = px.area(
        dados_mensais,
        x="Mês",
        y="Receita"
    )

    grafico_linha.update_traces(
        line=dict(color="#29b6f6"),
        fillcolor="rgba(41, 182, 246, 0.35)"
    )

    grafico_linha.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font=dict(color="#d7eaff"),
        xaxis=dict(
            title="",
            gridcolor="#234866"
        ),
        yaxis=dict(
            title="Receita",
            gridcolor="#234866"
        )
    )

    st.plotly_chart(
        grafico_linha,
        use_container_width=True
    )


# ============================================================
# GRÁFICO 2 - RECEITA POR CATEGORIA
# ============================================================

with col2:

    st.markdown(
        '<div class="grafico-titulo">'
        'Receita por Categoria'
        '</div>',
        unsafe_allow_html=True
    )

    dados_categoria = (
        df_filtrado
        .groupby("Product Category")["Total Amount"]
        .sum()
        .reset_index()
    )

    dados_categoria.columns = ["Categoria", "Receita"]

    grafico_categoria = px.bar(
        dados_categoria,
        x="Categoria",
        y="Receita"
    )

    grafico_categoria.update_traces(
        marker_color="#29b6f6"
    )

    grafico_categoria.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font=dict(color="#d7eaff"),
        xaxis=dict(
            title="",
            gridcolor="#234866"
        ),
        yaxis=dict(
            title="Receita",
            gridcolor="#234866"
        )
    )

    st.plotly_chart(
        grafico_categoria,
        use_container_width=True
    )


# ============================================================
# RESUMO POR GÊNERO
# ============================================================

st.markdown(
    '<div class="secao">👥 Análise por Gênero</div>',
    unsafe_allow_html=True
)

col3, col4 = st.columns(2)


# GRÁFICO DE RECEITA POR GÊNERO

with col3:

    dados_genero = (
        df_filtrado
        .groupby("Gender")["Total Amount"]
        .sum()
        .reset_index()
    )

    dados_genero.columns = ["Gênero", "Receita"]

    grafico_genero = px.bar(
        dados_genero,
        x="Gênero",
        y="Receita"
    )

    grafico_genero.update_traces(
        marker_color="#7c4dff"
    )

    grafico_genero.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font=dict(color="#d7eaff"),
        xaxis=dict(
            title="",
            gridcolor="#234866"
        ),
        yaxis=dict(
            title="Receita",
            gridcolor="#234866"
        )
    )

    st.plotly_chart(
        grafico_genero,
        use_container_width=True
    )


# GRÁFICO DE QUANTIDADE POR GÊNERO

with col4:

    quantidade_genero = (
        df_filtrado
        .groupby("Gender")["Quantity"]
        .sum()
        .reset_index()
    )

    quantidade_genero.columns = ["Gênero", "Quantidade"]

    grafico_quantidade = px.bar(
        quantidade_genero,
        x="Gênero",
        y="Quantidade"
    )

    grafico_quantidade.update_traces(
        marker_color="#00c896"
    )

    grafico_quantidade.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font=dict(color="#d7eaff"),
        xaxis=dict(
            title="",
            gridcolor="#234866"
        ),
        yaxis=dict(
            title="Quantidade",
            gridcolor="#234866"
        )
    )

    st.plotly_chart(
        grafico_quantidade,
        use_container_width=True
    )


# ============================================================
# DADOS DAS VENDAS
# ============================================================

st.markdown(
    '<div class="tabela-titulo">📋 Dados das Vendas</div>',
    unsafe_allow_html=True
)

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD
# ============================================================

csv = df_filtrado.to_csv(index=False)

st.download_button(
    label="⬇️ Baixar dados filtrados em CSV",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)
