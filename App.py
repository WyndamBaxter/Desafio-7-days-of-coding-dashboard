import streamlit as st
import pandas as pd

#--- Configuração da página ---
# Definição do título, ícone e o layout para fullpage
st.set_page_config(
    page_title= 'Dashboard de análises da biblioteca SISBI',
    page_icon= '📚',
    layout='wide'
)

# --- Carregamento de dados ---
df_emprestimos_completo = pd.read_parquet('F:/Programação/Desafio-7-days-of-coding-dashboard/resultados/df_emprestimos_completo.parquet')

# --- Sidebar (Filtros) ---
st.sidebar.header("🔎Filtros")

# --- Conteúdo Principal ---
st.title = ("📚 Dashboard de análises da biblioteca SISBI")
st.markdown("Analise bem...")