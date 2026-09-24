import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #071b2e;
    color: white;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* TÍTULO */

.titulo {
    font-size: 42px;
    font-weight: 700;
    color: white;
}

.subtitulo {
    color: #9fc4e8;
    font-size: 16px;
    margin-bottom: 25px;
}

.linha {
    width: 65px;
    height: 4px;
    background-color: #29b6f6;
    border-radius: 10px;
    margin-top: 10px;
    margin-bottom: 25px;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #0b2944;
    border-right: 1px solid #21496d;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* CARDS */

[data-testid="stMetric"] {
    background-color: #103553;
    border: 1px solid #245b82;
    border-radius: 15px;
    padding: 22px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.20);
}

[data-testid="stMetricLabel"] {
    color: #9fc4e8 !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}


/* TÍTULOS */

.secao {
    color: white;
    font-size: 23px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 15px;
}

.grafico-titulo {
    color: #d7eaff;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 5px;
}


/* BOTÃO */

.stDownloadButton button {
    background-color: #168bd0;
    color: white;
    border: none;
    border-radius: 8px;
}

.stDownloadButton button:hover {
    background-color: #29b6f6;
    color: white;
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

st.sidebar.title("📊 Dashboard")

st.sidebar.markdown("---")

st.sidebar.subheader("🎯 Filtros")

st.sidebar.write(
    "Utilize os filtros para analisar os dados."
)


# ============================================================
# FILTRO CATEGORIA
# ============================================================

categorias = sorted(
    df["Product Category"].unique()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=categorias,
    default=categorias
)


# ============================================================
# FILTRO GÊNERO
# ============================================================

generos = sorted(
    df["Gender"].unique()
)

generos_selecionados = st.sidebar.multiselect(
    "Gênero",
    options=generos,
    default=generos
)


# ============================================================
# FILTRO DE DATA
# ============================================================

data_minima = df["Date"].min().date()
data_maxima = df["Date"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_minima, data_maxima),
    min_value=data_minima,
    max_value=data_maxima
)


# ============================================================
# APLICAR FILTROS
# ============================================================

df_filtrado = df[
    df["Product Category"].isin(categorias_selecionadas)
    &
    df["Gender"].isin(generos_selecionados)
].copy()


if len(periodo) == 2:

    data_inicio = pd.to_datetime(periodo[0])
    data_fim = pd.to_datetime(periodo[1])

    df_filtrado = df_filtrado[
        (df_filtrado["Date"] >= data_inicio)
        &
        (df_filtrado["Date"] <= data_fim)
    ]


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="titulo">📊 Dashboard de Vendas</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="linha"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Análise de vendas, clientes e desempenho por período'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# MÉTRICAS
# ============================================================

receita_total = df_filtrado["Total Amount"].sum()

total_pedidos = df_filtrado["Transaction ID"].nunique()

quantidade_vendida = df_filtrado["Quantity"].sum()

if total_pedidos > 0:

    ticket_medio = receita_total / total_pedidos

else:

    ticket_medio = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Receita Total",
        f"R$ {receita_total:,.2f}"
    )


with col2:

    st.metric(
        "🛒 Total de Pedidos",
        total_pedidos
    )


with col3:

    st.metric(
        "📦 Quantidade Vendida",
        quantidade_vendida
    )


with col4:

    st.metric(
        "🎟️ Ticket Médio",
        f"R$ {ticket_medio:,.2f}"
    )


# ============================================================
# DESEMPENHO DAS VENDAS
# ============================================================

st.markdown(
    '<div class="secao">📈 Desempenho das Vendas</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# EVOLUÇÃO MENSAL
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
        .groupby(
            df_filtrado["Date"].dt.strftime("%Y-%m")
        )["Total Amount"]
        .sum()
        .reset_index()
    )

    dados_mensais.columns = [
        "Mês",
        "Receita"
    ]

    grafico_mensal = px.area(
        dados_mensais,
        x="Mês",
        y="Receita"
    )

    grafico_mensal.update_traces(
        line_color="#29b6f6",
        fillcolor="rgba(41,182,246,0.35)"
    )

    grafico_mensal.update_layout(
        height=380,
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font_color="#d7eaff",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
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
        grafico_mensal,
        use_container_width=True
    )


# ============================================================
# RECEITA POR CATEGORIA
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

    dados_categoria.columns = [
        "Categoria",
        "Receita"
    ]

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
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font_color="#d7eaff",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
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
# ANÁLISE POR GÊNERO
# ============================================================

st.markdown(
    '<div class="secao">👥 Análise por Gênero</div>',
    unsafe_allow_html=True
)


col3, col4 = st.columns(2)


# ============================================================
# RECEITA POR GÊNERO
# ============================================================

with col3:

    dados_genero = (
        df_filtrado
        .groupby("Gender")["Total Amount"]
        .sum()
        .reset_index()
    )

    dados_genero.columns = [
        "Gênero",
        "Receita"
    ]

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
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font_color="#d7eaff",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
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


# ============================================================
# QUANTIDADE POR GÊNERO
# ============================================================

with col4:

    quantidade_genero = (
        df_filtrado
        .groupby("Gender")["Quantity"]
        .sum()
        .reset_index()
    )

    quantidade_genero.columns = [
        "Gênero",
        "Quantidade"
    ]

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
        paper_bgcolor="#0e2d49",
        plot_bgcolor="#0e2d49",
        font_color="#d7eaff",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
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
    '<div class="secao">📋 Dados das Vendas</div>',
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
