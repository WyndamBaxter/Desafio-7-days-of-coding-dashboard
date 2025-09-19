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

# Filtragem do dataframe
df_filtrado = df_emprestimos_completo[
        df_emprestimos_completo.data_emprestimo.dt.year.isin(anos_selecionados)
    ]

# --- Conteúdo Principal ---

st.title("Dashboard de análise dos empréstimos da biblioteca SISBI")
st.markdown("Analise bem...")

# --- Métricas Gerais ---
st.subheader('Métricas Gerais')

if not df_filtrado.empty:
    emprestimos = len(df_filtrado.id_emprestimo.unique())
    exemplares = len(df_filtrado.id_emprestimo)
    mes_numero = df_filtrado.data_emprestimo.dt.month.value_counts().idxmax()
    mes_nome = meses_nomes.get(mes_numero, 'Desconhecido')
    base_mais_acessada = df_filtrado.biblioteca.value_counts().idxmax()
else:
    emprestimos, exemplares, mes_emprestimos_maximo, base_mais_acessada = 0, 0, 'Nenhum', 'Nenhuma'

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Empréstimos", emprestimos)
col2.metric('Total de exemplares', exemplares)
col3.metric('Mês com maior número de empréstimos', mes_nome)
col4.metric('Base mais Acessada', base_mais_acessada)

