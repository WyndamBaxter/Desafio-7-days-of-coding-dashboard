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

# --- Sidebar (Filtros) ---
st.sidebar.header("🔎Filtros")

# Filtro de Ano 
anos_disponiveis = sorted(df_emprestimos_completo.data_emprestimo.dt.year.unique())
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis) 

# Filtro 


# Filtragem do dataframe
df_filtrado = df_emprestimos_completo[
        df_emprestimos_completo.data_emprestimo.dt.year.isin(anos_selecionados)
    ]

# --- Conteúdo Principal ---

st.title("Dashboard de análises da biblioteca SISBI")
st.markdown("Analise bem...")

# --- Métricas Gerais ---
st.subheader('Métricas Gerais')

if not df_filtrado.empty:
    emprestimos = len(df_filtrado.id_emprestimo.unique())
    exemplares = len(df_filtrado.id_emprestimo)
    mes_emprestimos_maximo = df_filtrado
else:
    emprestimos, exemplares = 0, 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Empréstimos", emprestimos)
col2.metric('Total de exemplares', exemplares)
col3.metric('Mês com maior número de empréstimos', exemplares)
col4.metric('Mês com menor número de empréstimos', exemplares)
