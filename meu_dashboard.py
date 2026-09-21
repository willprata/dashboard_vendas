import streamlit as st
import pandas as pd

# FASE 1 - Estrutura Básica

st.title('Dashboard de Vendas')


@st.cache_data
def carregar_dados():
    return pd.read_csv('retail_sales_dataset.csv')


df = carregar_dados()


# FASE 2 - Layout e Filtros Laterais

st.sidebar.title('Filtros')

lista_de_categorias = df['Product Category'].unique()

categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias',
    options=lista_de_categorias,
    default=lista_de_categorias
)

df_filtrado = df[
    df['Product Category'].isin(categorias_selecionadas)
]


# FASE 3 - Métricas e Visualização

receita_calculada = df_filtrado['Total Amount'].sum()

total_pedidos = df_filtrado['Transaction ID'].nunique()


col1, col2 = st.columns([1, 1])

with col1:
    st.metric(
        label='Receita Total',
        value=f'R$ {receita_calculada:,.2f}'
    )

with col2:
    st.metric(
        label='Total de Pedidos',
        value=total_pedidos
    )


aba1, aba2 = st.tabs([
    'Evolução Mensal',
    'Tabela de Dados'
])


with aba1:

    df_filtrado['Date'] = pd.to_datetime(
        df_filtrado['Date']
    )

    dados_agrupados = df_filtrado.groupby(
        df_filtrado['Date'].dt.to_period('M')
    )['Total Amount'].sum()

    dados_agrupados.index = dados_agrupados.index.astype(str)

    st.area_chart(dados_agrupados)

#.
with aba2:

    st.dataframe(df_filtrado)

    csv = df_filtrado.to_csv(index=False)

    st.download_button(
        label='Baixar dados em CSV',
        data=csv,
        file_name='vendas_filtradas.csv',
        mime='text/csv'
    )