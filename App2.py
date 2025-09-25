import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly_express as px
import seaborn as sns

#--- Configuração da página ---
st.set_page_config(
    page_title='Dashboard de análises da biblioteca SISBI',
    page_icon='📚',
    layout='wide'
)

# --- Carregamento de dados ---
@st.cache_data
def load_data():
    # <-- SUGESTÃO: Use um caminho relativo para o arquivo
    df = pd.read_parquet('F:/Programação/Desafio-7-days-of-coding-dashboard/resultados/df_emprestimos_completo.parquet') # Exemplo de caminho relativo
    return df

df_emprestimos_completo = load_data()

# --- Dicionário para nomes de meses ---
meses_nomes = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

# --- Sidebar (Filtros) ---
st.sidebar.header("🔎 Filtros")

anos_disponiveis = sorted(df_emprestimos_completo['data_emprestimo'].dt.year.unique())
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)

colecao_disponivel = sorted(df_emprestimos_completo['colecao'].unique())
colecao_selecionada = st.sidebar.multiselect('Coleção', colecao_disponivel, default=colecao_disponivel)

vinculo_disponivel = sorted(df_emprestimos_completo['tipo_vinculo_usuario'].unique())
vinculo_selecionado = st.sidebar.multiselect('Tipo de Vínculo', vinculo_disponivel, default=vinculo_disponivel)

# Filtragem do dataframe
df_filtrado = df_emprestimos_completo[
    df_emprestimos_completo['data_emprestimo'].dt.year.isin(anos_selecionados) &
    df_emprestimos_completo['colecao'].isin(colecao_selecionada) &
    df_emprestimos_completo['tipo_vinculo_usuario'].isin(vinculo_selecionado)
]

# --- Conteúdo Principal ---
st.title("Dashboard de análise dos empréstimos da biblioteca SISBI")
st.markdown("Analise bem...")

# --- Métricas Gerais ---
st.subheader('Métricas Gerais')

if not df_filtrado.empty:
    emprestimos = len(df_filtrado['id_emprestimo'].unique())
    exemplares = len(df_filtrado) # Mais simples que len(df_filtrado['id_emprestimo'])
    colecao_mais_acessada = df_filtrado['colecao'].value_counts().idxmax()
    vinculo_mais_acessado = df_filtrado['tipo_vinculo_usuario'].value_counts().idxmax()
else:
    emprestimos, exemplares, colecao_mais_acessada, vinculo_mais_acessado = 0, 0, 'Nenhum', 'Nenhuma'

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Empréstimos Únicos", emprestimos)
col2.metric('Total de Exemplares Emprestados', exemplares)
col3.metric('Coleção mais acessada', colecao_mais_acessada)
col4.metric('Vínculo com mais empréstimos', vinculo_mais_acessado)

st.markdown("---")
st.header("Gráficos")

line_graf1, line_graf2 = st.columns(2)

with line_graf1:
    st.subheader('Empréstimos ao longo dos Anos')
    emprestimos_ano = df_filtrado.groupby(df_filtrado['data_emprestimo'].dt.year)['id_emprestimo'].size().reset_index(name='Quantidade')
    emprestimos_ano.rename(columns={'data_emprestimo': 'Ano'}, inplace=True)

    # <-- MUDANÇA: Lógica de verificação corrigida
    if len(emprestimos_ano) > 1:
        grafico_emprestimos_ano = px.line(
            emprestimos_ano,
            x='Ano',
            y='Quantidade',
            labels={'Ano': 'Ano', 'Quantidade': 'Total de Exemplares'}, # <-- MUDANÇA: Label corrigida
            # <-- MUDANÇA: Parâmetro 'subtitle' removido e incorporado ao título
            title='Exemplares emprestados do SISBI por Ano<br><sup>2010 a 2020</sup>'
        )
        grafico_emprestimos_ano.update_layout(xaxis={'tickmode': 'linear'})
        st.plotly_chart(grafico_emprestimos_ano, use_container_width=True)
    else:
        st.warning("Selecione dados de pelo menos dois anos para exibir o gráfico.")

with line_graf2:
    st.subheader('Empréstimos ao longo dos Meses')
    if not df_filtrado.empty:
        emprestimos_mes = df_filtrado.groupby(df_filtrado['data_emprestimo'].dt.month)['id_emprestimo'].size().reset_index(name='Quantidade')
        emprestimos_mes.rename(columns={'data_emprestimo': 'Mês'}, inplace=True)

        # <-- MUDANÇA: Usando o dicionário e ordenando corretamente os meses
        emprestimos_mes['Mês'] = emprestimos_mes['Mês'].map(meses_nomes)
        ordem_meses = list(meses_nomes.values())
        emprestimos_mes['Mês'] = pd.Categorical(emprestimos_mes['Mês'], categories=ordem_meses, ordered=True)
        emprestimos_mes = emprestimos_mes.sort_values('Mês')

        grafico_emprestimos_mes = px.line(
            emprestimos_mes,
            x='Mês',
            y='Quantidade',
            labels={'Mês': 'Mês', 'Quantidade': 'Total de Exemplares'},
            title='Exemplares emprestados do SISBI por Mês'
        )
        st.plotly_chart(grafico_emprestimos_mes, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico.")

st.markdown("---")
st.subheader('Distribuição de Empréstimos por Hora do Dia')
# <-- MUDANÇA: Removido o st.columns(1) desnecessário
if not df_filtrado.empty:
    emprestimos_hora = df_filtrado.groupby(df_filtrado['data_emprestimo'].dt.hour)['id_emprestimo'].size().reset_index(name='Quantidade')
    emprestimos_hora.rename(columns={'data_emprestimo': 'Hora'}, inplace=True)

    # Para Seaborn/Matplotlib, é melhor criar a figura e os eixos separadamente
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=emprestimos_hora,
        x='Hora',
        y='Quantidade',
        ax=ax # Especifica o eixo para o plot
    )
    ax.set_title('Quantidade de exemplares por hora')
    ax.set_xlabel('Hora do Dia')
    ax.set_ylabel('Total de Exemplares')
    st.pyplot(fig, use_container_width=True)
else:
    st.warning("Nenhum dado para exibir no gráfico.")
