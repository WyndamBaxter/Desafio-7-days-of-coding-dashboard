import streamlit as st
import pandas as pd
import plotly_express as px

#--- Configuração da página ---
# Definição do título, ícone e o layout para fullpage
st.set_page_config(
    page_title= 'Dashboard de análises da biblioteca SISBI',
    page_icon= '📚',
    layout='wide'
)

# --- Carregamento de dados ---
@st.cache_data
def load_data():
    df = pd.read_parquet('F:/Programação/Desafio-7-days-of-coding-dashboard/resultados/df_emprestimos_completo.parquet')
    return df

df_emprestimos_completo = load_data()

# --- Diconário para nomes de mêses

meses_nomes = {
     1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}


# --- Sidebar (Filtros) ---
st.sidebar.header("🔎Filtros")

# Filtro de Ano 
anos_disponiveis = sorted(df_emprestimos_completo.data_emprestimo.dt.year.unique())
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis) 

# Filtro por Coleção

colecao_disponivel = sorted(df_emprestimos_completo.colecao.unique())
colecao_selecionada = st.sidebar.multiselect('Coleção', colecao_disponivel, default= colecao_disponivel)

# Filtro por tipo de vínculo

vinculo_disponivel = sorted(df_emprestimos_completo.tipo_vinculo_usuario.unique())
vinculo_selecionado = st.sidebar.multiselect('Tipo de Vínculo', vinculo_disponivel, default= vinculo_disponivel)

# Filtragem do dataframe
df_filtrado = df_emprestimos_completo[
        df_emprestimos_completo.data_emprestimo.dt.year.isin(anos_selecionados)&
        df_emprestimos_completo.colecao.isin(colecao_selecionada)&
        df_emprestimos_completo.tipo_vinculo_usuario.isin(vinculo_selecionado)
    ]

# --- Conteúdo Principal ---

st.title("Dashboard de análise dos empréstimos da biblioteca SISBI")
st.markdown("Analise bem...")

# --- Métricas Gerais ---
st.subheader('Métricas Gerais')

if not df_filtrado.empty:
    emprestimos = len(df_filtrado.id_emprestimo.unique())
    exemplares = len(df_filtrado.id_emprestimo)
    colecao_mais_acessada = df_filtrado.colecao.value_counts().idxmax()
    vinculo_mais_acessado = df_filtrado.tipo_vinculo_usuario.value_counts().idxmax()
else:
    emprestimos, exemplares, colecao_mais_acessada, vinculo_mais_acessado = 0, 0, 'Nenhum', 'Nenhuma'

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Empréstimos", emprestimos)
col2.metric('Total de exemplares', exemplares)
col3.metric('Coleção mais acessada', colecao_mais_acessada)
col4.metric('Tipo de Vínculo', vinculo_mais_acessado)

st.markdown("---")

st.header("Gráficos")

line_graf1, line_graf2 = st.columns(2)

with line_graf1:
    if  len(df_filtrado.data_emprestimo.value_counts().unique()) > 2:
        emprestimos_ano = df_filtrado.groupby(df_filtrado.data_emprestimo.dt.year)['id_emprestimo'].size()
        emprestimos_ano.index.name = 'Ano'
        emprestimos_ano.name = 'Quantidade'
        emprestimos_ano = emprestimos_ano.reset_index()

        grafico_emprestimos_ano = px.line(
            emprestimos_ano,
            x = 'Ano',
            y = 'Quantidade',
            labels= {
                'ano': 'Ano',
                'Quantidade': 'Empréstimos'
            },
            title = 'Quantidade de exemplares emprestados do SISBI ao longo dos anos',
            subtitle= '2010 a 2020',
            

        )
        grafico_emprestimos_ano.update_layout(
            xaxis = {
                'tickmode': 'linear'
            }
        )
        st.plotly_chart(grafico_emprestimos_ano, use_container_width=True)
        
    else:
         st.warning("Nenhum dado para exibir no gráfico.")

with line_graf2:
    if not df_filtrado.empty:
        emprestimos_mes = df_filtrado.groupby(df_filtrado.data_emprestimo.dt.month)['id_emprestimo'].size()
        emprestimos_mes.index.name = 'mes'
        emprestimos_mes.name = 'quantidade'
        emprestimos_mes = emprestimos_mes.reset_index()
        emprestimos_mes['mes'] = emprestimos_mes['mes'].replace({

                1: 'Janeiro', 2: 'Fevereiro', 3:'Março',
                4: 'Abril', 5: 'Maio', 6: 'Junho',
                7: 'Julho', 8:'Agosto', 9:'Setembro',
                10: 'Outubro', 11: 'Novembro', 12:'Dezembro'

            })

        grafico_emprestimos_mes = px.line(
            emprestimos_mes,
            x = 'mes',
            y = 'quantidade',
            labels= {
                'mes': 'Mês',
                'quantidade': ''
            },
            title = 'Quantidade de exemplares emprestados do SISBI ao longo dos mêses.'
            

        )
        st.plotly_chart(grafico_emprestimos_mes, use_container_width=True)
        
    else:
         st.warning("Nenhum dado para exibir no gráfico.")



