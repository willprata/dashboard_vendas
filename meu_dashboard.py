import streamlit as st
import pandas as pd
import altair as alt


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# ESTILO DO DASHBOARD
# ==========================================================

st.markdown("""
<style>

    /* =====================================================
       FUNDO GERAL
       ===================================================== */

    .stApp {
        background: #071a2d;
        color: #ffffff;
    }

    [data-testid="stAppViewContainer"] {
        background: #071a2d;
    }

    [data-testid="stMain"] {
        background: #071a2d;
    }


    /* =====================================================
       CABEÇALHO DO STREAMLIT
       ===================================================== */

    header[data-testid="stHeader"] {
        background: #071a2d !important;
    }

    header[data-testid="stHeader"] * {
        color: #ffffff !important;
    }


    /* =====================================================
       ESPAÇAMENTO PRINCIPAL
       ===================================================== */

    .main .block-container {
        padding-top: 2.5rem;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background: #0b223b;
        border-right: 1px solid #214765;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }


    /* =====================================================
       TÍTULO
       ===================================================== */

    .titulo {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .subtitulo {
        color: #9bb5d0;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .linha-titulo {
        width: 65px;
        height: 4px;
        background: #35b6ff;
        border-radius: 10px;
        margin-bottom: 25px;
    }


    /* =====================================================
       CARDS
       ===================================================== */

    .card {
        background: #102f4e;
        border: 1px solid #27557d;
        border-radius: 15px;
        padding: 22px;
        min-height: 125px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    }

    .card-titulo {
        color: #9bb5d0;
        font-size: 14px;
        margin-bottom: 12px;
    }

    .card-valor {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
    }


    /* =====================================================
       TÍTULOS DAS SEÇÕES
       ===================================================== */

    .secao {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
        margin-top: 35px;
        margin-bottom: 15px;
    }

    .subsecao {
        color: #dcecff;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
    }


    /* =====================================================
       ÁREA DOS GRÁFICOS
       ===================================================== */

    div[data-testid="stVegaLiteChart"] {
        background: #0d2742;
        border: 1px solid #214b70;
        border-radius: 15px;
        padding: 8px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18);
    }


    /* =====================================================
       TABELA
       ===================================================== */

    div[data-testid="stDataFrame"] {
        background: #0d2742;
        border: 1px solid #214b70;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18);
    }


    /* =====================================================
       BOTÃO DE DOWNLOAD
       ===================================================== */

    .stDownloadButton button {
        background: #168cff;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
    }

    .stDownloadButton button:hover {
        background: #0b73d1;
        color: #ffffff;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# CARREGAR DADOS
# ==========================================================

@st.cache_data
def carregar_dados():

    return pd.read_csv("retail_sales_dataset.csv")


df = carregar_dados()

df["Date"] = pd.to_datetime(df["Date"])


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown(
    """
    <h2 style="color:white;">📊 Dashboard</h2>

    <hr style="border: 1px solid #234766;">
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(
    """
    <h3 style="color:white;">🎯 Filtros</h3>

    <p style="color:#9bb5d0;">
    Utilize os filtros para analisar os dados.
    </p>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# FILTRO DE CATEGORIA
# ==========================================================

lista_categorias = sorted(
    df["Product Category"].unique()
)


categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=lista_categorias,
    default=lista_categorias
)


# ==========================================================
# FILTRO DE GÊNERO
# ==========================================================

lista_generos = sorted(
    df["Gender"].unique()
)


generos_selecionados = st.sidebar.multiselect(
    "Gênero",
    options=lista_generos,
    default=lista_generos
)


# ==========================================================
# FILTRO DE PERÍODO
# ==========================================================

data_minima = df["Date"].min().date()

data_maxima = df["Date"].max().date()


periodo = st.sidebar.date_input(
    "Período",
    value=(data_minima, data_maxima),
    min_value=data_minima,
    max_value=data_maxima
)


# ==========================================================
# APLICAÇÃO DOS FILTROS
# ==========================================================

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


# ==========================================================
# CABEÇALHO
# ==========================================================

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


# ==========================================================
# CÁLCULO DAS MÉTRICAS
# ==========================================================

receita_total = df_filtrado["Total Amount"].sum()


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


# ==========================================================
# CARDS DAS MÉTRICAS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="card">

            <div class="card-titulo">
                💰 RECEITA TOTAL
            </div>

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

            <div class="card-titulo">
                🛒 TOTAL DE PEDIDOS
            </div>

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

            <div class="card-titulo">
                📦 QUANTIDADE VENDIDA
            </div>

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

            <div class="card-titulo">
                🎟️ TICKET MÉDIO
            </div>

            <div class="card-valor">
                R$ {ticket_medio:,.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# TÍTULO DOS GRÁFICOS
# ==========================================================

st.markdown(
    '<div class="secao">📈 Desempenho das Vendas</div>',
    unsafe_allow_html=True
)


col_grafico1, col_grafico2 = st.columns(2)


# ==========================================================
# GRÁFICO 1
# EVOLUÇÃO MENSAL
# ==========================================================

with col_grafico1:

    st.markdown(
        '<div class="subsecao">'
        'Evolução Mensal da Receita'
        '</div>',
        unsafe_allow_html=True
    )


    dados_mensais = (
        df_filtrado
        .set_index("Date")
        .resample("ME")["Total Amount"]
        .sum()
        .reset_index()
    )


    grafico_mensal = (

        alt.Chart(dados_mensais)

        .mark_area(
            color="#168cff",
            opacity=0.65,
            line={
                "color": "#35b6ff",
                "strokeWidth": 3
            }
        )

        .encode(

            x=alt.X(
                "Date:T",
                title="",
                axis=alt.Axis(
                    labelColor="#b8cbe0",
                    titleColor="#b8cbe0"
                )
            ),

            y=alt.Y(
                "Total Amount:Q",
                title="Receita",
                axis=alt.Axis(
                    labelColor="#b8cbe0",
                    titleColor="#b8cbe0",
                    format=",.0f"
                )
            ),

            tooltip=[

                alt.Tooltip(
                    "Date:T",
                    title="Mês",
                    format="%m/%Y"
                ),

                alt.Tooltip(
                    "Total Amount:Q",
                    title="Receita",
                    format=",.2f"
                )

            ]
        )

        .properties(
            height=330,
            background="#0d2742"
        )

        .configure_view(
            strokeWidth=0
        )

        .configure_axis(
            gridColor="#28506f",
            domainColor="#28506f"
        )
    )


    st.altair_chart(
        grafico_mensal,
        use_container_width=True
    )


# ==========================================================
# GRÁFICO 2
# RECEITA POR CATEGORIA
# ==========================================================

with col_grafico2:

    st.markdown(
        '<div class="subsecao">'
        'Receita por Categoria'
        '</div>',
        unsafe_allow_html=True
    )


    dados_categoria = (
        df_filtrado
        .groupby(
            "Product Category"
        )["Total Amount"]
        .sum()
        .reset_index()
    )


    grafico_categoria = (

        alt.Chart(dados_categoria)

        .mark_bar(
            color="#35b6ff",
            cornerRadiusTopLeft=6,
            cornerRadiusTopRight=6
        )

        .encode(

            x=alt.X(
                "Product Category:N",
                title="",
                axis=alt.Axis(
                    labelColor="#b8cbe0"
                )
            ),

            y=alt.Y(
                "Total Amount:Q",
                title="Receita",
                axis=alt.Axis(
                    labelColor="#b8cbe0",
                    titleColor="#b8cbe0",
                    format=",.0f"
                )
            ),

            tooltip=[

                alt.Tooltip(
                    "Product Category:N",
                    title="Categoria"
                ),

                alt.Tooltip(
                    "Total Amount:Q",
                    title="Receita",
                    format=",.2f"
                )

            ]
        )

        .properties(
            height=330,
            background="#0d2742"
        )

        .configure_view(
            strokeWidth=0
        )

        .configure_axis(
            gridColor="#28506f",
            domainColor="#28506f"
        )
    )


    st.altair_chart(
        grafico_categoria,
        use_container_width=True
    )


# ==========================================================
# DADOS DAS VENDAS
# ==========================================================

st.markdown(
    '<div class="secao">📋 Dados das Vendas</div>',
    unsafe_allow_html=True
)


# ==========================================================
# TABELA
# ==========================================================

df_tabela = df_filtrado.style.set_properties(
    **{
        "background-color": "#0d2742",
        "color": "#ffffff",
        "border-color": "#28506f"
    }
)


st.dataframe(
    df_tabela,
    use_container_width=True,
    height=400
)


# ==========================================================
# DOWNLOAD
# ==========================================================

csv = df_filtrado.to_csv(
    index=False
)


st.download_button(
    label="⬇️ Baixar dados filtrados em CSV",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)
