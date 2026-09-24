import streamlit as st
import pandas as pd


# ---------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# ESTILO VISUAL
# ---------------------------------------------------------

st.markdown("""
<style>

    /* FUNDO PRINCIPAL */

    .stApp {
        background:
            radial-gradient(
                circle at 90% 5%,
                rgba(52, 152, 219, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 20% 90%,
                rgba(46, 204, 113, 0.06),
                transparent 25%
            ),
            #f3f7fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }


    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #f8fbff 0%,
                #eef5fc 100%
            );

        border-right: 1px solid #dce8f5;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #173f6f;
    }

    section[data-testid="stSidebar"] p {
        color: #61758a;
    }


    /* TÍTULO */

    .titulo {
        color: #123f73;
        font-size: 38px;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 2px;
    }

    .subtitulo {
        color: #6b8197;
        font-size: 15px;
        margin-bottom: 28px;
    }


    /* LINHA DECORATIVA */

    .linha {
        height: 4px;
        width: 65px;
        background: linear-gradient(
            90deg,
            #2f80ed,
            #56ccf2
        );
        border-radius: 10px;
        margin-top: 8px;
        margin-bottom: 22px;
    }


    /* CARDS */

    .card {
        position: relative;
        overflow: hidden;

        background: rgba(255, 255, 255, 0.92);

        padding: 20px 22px;

        border-radius: 16px;

        border: 1px solid #dce7f2;

        box-shadow:
            0 5px 18px rgba(32, 73, 125, 0.08);

        min-height: 120px;

        transition: 0.2s;
    }

    .card:hover {
        box-shadow:
            0 8px 24px rgba(32, 73, 125, 0.13);
    }

    .card::after {
        content: "";

        position: absolute;

        width: 100px;
        height: 100px;

        right: -35px;
        bottom: -45px;

        border-radius: 50%;

        background: rgba(47, 128, 237, 0.07);
    }

    .card-titulo {
        color: #71859a;
        font-size: 12px;
        font-weight: 700;

        letter-spacing: 0.5px;

        margin-bottom: 8px;
    }

    .card-valor {
        color: #123f73;
        font-size: 28px;
        font-weight: 750;
    }


    /* TÍTULOS DAS SEÇÕES */

    .secao {
        color: #173f6f;

        font-size: 21px;

        font-weight: 700;

        margin-top: 28px;

        margin-bottom: 12px;
    }


    /* PAINÉIS DOS GRÁFICOS */

    .painel {
        background: rgba(255, 255, 255, 0.90);

        border: 1px solid #dce7f2;

        border-radius: 16px;

        padding: 18px 18px 10px 18px;

        box-shadow:
            0 5px 18px rgba(32, 73, 125, 0.06);

        margin-bottom: 18px;
    }


    /* TÍTULO INTERNO DOS GRÁFICOS */

    .titulo-grafico {
        color: #244f7d;

        font-size: 15px;

        font-weight: 700;

        margin-bottom: 5px;
    }


    /* TABS */

    button[data-baseweb="tab"] {
        color: #66809a;

        font-size: 14px;

        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1769aa;
    }


    /* BOTÃO DOWNLOAD */

    .stDownloadButton button {
        background: linear-gradient(
            135deg,
            #1769aa,
            #2587d8
        );

        color: white;

        border: none;

        border-radius: 9px;

        font-weight: 600;

        padding: 9px 18px;

        box-shadow:
            0 4px 10px rgba(23, 105, 170, 0.18);
    }

    .stDownloadButton button:hover {
        background: linear-gradient(
            135deg,
            #12578e,
            #1769aa
        );

        color: white;
    }


    /* DATAFRAME */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #dce7f2;
    }


    /* RODAPÉ */

    .rodape {
        text-align: center;

        color: #8aa0b5;

        font-size: 12px;

        padding-top: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# CARREGAR DADOS
# ---------------------------------------------------------

@st.cache_data
def carregar_dados():

    dados = pd.read_csv("retail_sales_dataset.csv")

    dados["Date"] = pd.to_datetime(
        dados["Date"]
    )

    return dados


df = carregar_dados()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.markdown("## 📊 Dashboard")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🎯 Filtros")

st.sidebar.write(
    "Utilize os filtros para analisar os dados."
)


# CATEGORIAS

lista_de_categorias = sorted(
    df["Product Category"].unique()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)


# GÊNERO

lista_de_generos = sorted(
    df["Gender"].unique()
)

generos_selecionados = st.sidebar.multiselect(
    "Gênero",
    options=lista_de_generos,
    default=lista_de_generos
)


# PERÍODO

data_inicial = df["Date"].min().date()

data_final = df["Date"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_inicial, data_final),
    min_value=data_inicial,
    max_value=data_final
)


# ---------------------------------------------------------
# FILTROS
# ---------------------------------------------------------

df_filtrado = df[
    (df["Product Category"].isin(categorias_selecionadas)) &
    (df["Gender"].isin(generos_selecionados))
].copy()


if len(periodo) == 2:

    inicio = pd.to_datetime(periodo[0])

    fim = pd.to_datetime(periodo[1])

    df_filtrado = df_filtrado[
        (df_filtrado["Date"] >= inicio) &
        (df_filtrado["Date"] <= fim)
    ]


# ---------------------------------------------------------
# CABEÇALHO
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# MÉTRICAS
# ---------------------------------------------------------

receita_total = df_filtrado["Total Amount"].sum()

total_pedidos = df_filtrado["Transaction ID"].nunique()

quantidade_vendida = df_filtrado["Quantity"].sum()

if total_pedidos > 0:
    ticket_medio = receita_total / total_pedidos
else:
    ticket_medio = 0


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


# ---------------------------------------------------------
# ESPAÇO
# ---------------------------------------------------------

st.write("")


# ---------------------------------------------------------
# SEÇÃO PRINCIPAL
# ---------------------------------------------------------

st.markdown(
    '<div class="secao">📈 Desempenho das Vendas</div>',
    unsafe_allow_html=True
)


grafico1, grafico2 = st.columns(2)


# ---------------------------------------------------------
# EVOLUÇÃO MENSAL
# ---------------------------------------------------------

with grafico1:

    st.markdown(
        '<div class="painel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="titulo-grafico">'
        'Evolução Mensal da Receita'
        '</div>',
        unsafe_allow_html=True
    )

    dados_mensais = df_filtrado.groupby(
        df_filtrado["Date"].dt.to_period("M")
    )["Total Amount"].sum()

    dados_mensais.index = (
        dados_mensais.index.astype(str)
    )

    st.area_chart(
        dados_mensais,
        height=330
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# RECEITA POR CATEGORIA
# ---------------------------------------------------------

with grafico2:

    st.markdown(
        '<div class="painel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="titulo-grafico">'
        'Receita por Categoria'
        '</div>',
        unsafe_allow_html=True
    )

    receita_categoria = (
        df_filtrado
        .groupby("Product Category")["Total Amount"]
        .sum()
    )

    st.bar_chart(
        receita_categoria,
        height=330
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# SEGUNDA SEÇÃO
# ---------------------------------------------------------

st.markdown(
    '<div class="secao">👥 Análise dos Clientes e Produtos</div>',
    unsafe_allow_html=True
)


grafico3, grafico4 = st.columns(2)


# RECEITA POR GÊNERO

with grafico3:

    st.markdown(
        '<div class="painel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="titulo-grafico">'
        'Receita por Gênero'
        '</div>',
        unsafe_allow_html=True
    )

    receita_genero = (
        df_filtrado
        .groupby("Gender")["Total Amount"]
        .sum()
    )

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
        '<div class="painel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="titulo-grafico">'
        'Quantidade Vendida por Categoria'
        '</div>',
        unsafe_allow_html=True
    )

    quantidade_categoria = (
        df_filtrado
        .groupby("Product Category")["Quantity"]
        .sum()
    )

    st.bar_chart(
        quantidade_categoria,
        height=300
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# TABELA
# ---------------------------------------------------------

st.markdown(
    '<div class="secao">📋 Dados das Vendas</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="painel">',
    unsafe_allow_html=True
)

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=400
)

csv = df_filtrado.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Baixar dados filtrados em CSV",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# RODAPÉ
# ---------------------------------------------------------

st.markdown(
    '<div class="rodape">'
    'Dashboard de Vendas • Python + Pandas + Streamlit'
    '</div>',
    unsafe_allow_html=True
)
