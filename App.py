import streamlit as st
import pandas as pd
import plotly_express as px


#--- Configuração da página ---
# Definição do título, ícone e o layout para fullpage
st.set_page_config(
    page_title= 'Dashboard de análises do SISBI',
    page_icon= '📚',
    layout='wide'
)

# --- Carregamento de dados ---
@st.cache_data
def load_data():
    df = pd.read_parquet('F:/Programação/Desafio-7-days-of-coding-dashboard/resultados/df_emprestimos_completo.parquet')
    #df = pd.read_parquet('C:/Users/PC/Desktop/Desafio-7-days-of-coding-dashboard/resultados/df_emprestimos_completo.parquet')
    return df

df_emprestimos_completo = load_data()

# --- Dicionário para nomes de mêses ---
meses_nomes = {
     1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}
# ---Função que gera tabelas de frequência---
def gera_tabela_frequencia(variavel):
    '''
    Esta função irá gerar uma tabela de frequência com percentuais de acordo
    com a variável passada.

    variavel = variável categórica escolhida de dentro do conjunto de dados
    emprestimos_completo
    '''
    dataframe = df_filtrado[variavel].value_counts()
    dataframe = dataframe.reset_index()
    dataframe.columns = [variavel, 'quantidade']
    dataframe['percentual'] = round((dataframe['quantidade']/dataframe['quantidade'].sum())*100,2)
    return dataframe

# --- Sidebar (Filtros) ---
st.sidebar.header("🔎Filtros")

# Filtro de Ano 
anos_disponiveis = sorted(df_emprestimos_completo['data_emprestimo'].dt.year.unique())
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis) 

# Filtro por Coleção

colecao_disponivel = sorted(df_emprestimos_completo['colecao'].unique())
colecao_selecionada = st.sidebar.multiselect('Coleção', colecao_disponivel, default= colecao_disponivel)

# Filtro por tipo de vínculo

vinculo_disponivel = sorted(df_emprestimos_completo['tipo_vinculo_usuario'].unique())
vinculo_selecionado = st.sidebar.multiselect('Tipo de Vínculo', vinculo_disponivel, default= vinculo_disponivel)

# Filtragem do dataframe
df_filtrado = df_emprestimos_completo[
        df_emprestimos_completo['data_emprestimo'].dt.year.isin(anos_selecionados)&
        df_emprestimos_completo['colecao'].isin(colecao_selecionada)&
        df_emprestimos_completo['tipo_vinculo_usuario'].isin(vinculo_selecionado)
    ]

# --- Conteúdo Principal ---

st.title("Dashboard de análise dos empréstimos do SISBI")

# --- Métricas Gerais ---
st.subheader('Métricas Gerais')

if not df_filtrado.empty:
    emprestimos = len(df_filtrado['id_emprestimo'].unique())
    exemplares = len(df_filtrado['id_emprestimo'])
    colecao_mais_acessada = df_filtrado['colecao'].value_counts().idxmax()
    vinculo_mais_acessado = df_filtrado['tipo_vinculo_usuario'].value_counts().idxmax()
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
    st.subheader('Empréstimos ao longo dos Anos')
    emprestimos_ano = df_filtrado.groupby(df_filtrado['data_emprestimo'].dt.year)['id_emprestimo'].size().reset_index(name='Quantidade')
    emprestimos_ano.rename(columns={'data_emprestimo': 'Ano'}, inplace=True)

    if  len(emprestimos_ano) > 1:
        
        grafico_emprestimos_ano = px.line(
            emprestimos_ano,
            x = 'Ano',
            y = 'Quantidade',
            labels= {
                'ano': 'Ano',
                'Quantidade': 'Empréstimos'
            },
            title = 'Quantidade de exemplares emprestados do SISBI ao longo dos anos',
            subtitle= '2010 a 2020'
            

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
        emprestimos_mes = df_filtrado.groupby(df_filtrado['data_emprestimo'].dt.month)['id_emprestimo'].size().reset_index(name='quantidade')
        emprestimos_mes.rename(columns={'data_emprestimo':'mes'},inplace=True)

        #Ordenação
        emprestimos_mes['mes'] = emprestimos_mes['mes'].map(meses_nomes)
        ordem_meses = list(meses_nomes.values())
        emprestimos_mes['mes'] = pd.Categorical(emprestimos_mes['mes'], categories=ordem_meses, ordered=True)
        emprestimos_mes = emprestimos_mes.sort_values('mes')

        #Impressão do gráfico
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


st.markdown("---")
st.subheader('Distribuição de Empréstimos por Hora do Dia')

if not df_filtrado.empty:
        emprestimos_hora = df_filtrado.groupby(df_filtrado['data_emprestimo'].dt.hour)['id_emprestimo'].size().reset_index(name='quantidade')
        emprestimos_hora.rename(columns={'data_emprestimo': 'hora'}, inplace=True)

        grafico_emprestimos_hora = px.bar(
             emprestimos_hora,
             x = 'hora',
             y = 'quantidade',
             color= 'quantidade',
             color_continuous_scale= 'reds',
             labels= {
                'hora': 'Hora do dia',
                'quantidade': ''
            },
            title = 'Quantidade de exemplares emprestados do SISBI ao longo das horas do dia.'
        )

        st.plotly_chart(grafico_emprestimos_hora, use_container_width=True)
    
else:
        st.warning("Nenhum dado para exibir no gráfico.")


st.markdown('----')
st.header('Análise de Frequências Relativas')

#Mapeamento para resumir títulos

analises = {
     'tipo_vinculo_usuario': 'Tipo de Vínculo dos Usuários',
     'colecao': 'Coleção',
     'biblioteca': 'Biblioteca',
     'classe_CDU': 'Classe CDU'
}

# Cria as abas a partir dos valores do dicionário

lista_nomes_de_abas = list(analises.values())
abas = st.tabs(lista_nomes_de_abas)

# Itera sobre o dicionário e as abas para popular o conteúdo

for i, (coluna, titulo) in enumerate(analises.items()):
     with abas[i]:
          st.subheader(f'Análise para: {titulo}')
            
          df = gera_tabela_frequencia(coluna)
          
          if not df.empty:
               
            # Prepara o dataframe para o gráfico: a primeira coluna se torna o índice
            # Isso é crucial para st.bar_chart funcionar corretamente
               
                df_para_grafico = df.set_index(df.columns[0])

            # Use colunas para organizar o layout
                col9, col10 = st.columns([0.4, 0.6])
            
                with col9:
                    st.write('Tabela de Frequência')
                    st.dataframe(df, width='stretch')
                
                with col10:
                    st.write('Gráfico de Frequência')      
                    st.bar_chart(df_para_grafico)
          else:
               st.warning('Não há dados para exibir esta categoria')

               #Verificar possibilidade de usar o plotly-express REFATORAR ESSE CÒDIGO ATÉ ENTENDER
                
st.markdown('---')
st.header('Distribuição de empréstimos mensais do Acervo Circulante')
st.subheader('Por Alunos de Graduação ')

if not df_filtrado.empty:
     
    alunos_graduacao = df_filtrado.query('tipo_vinculo_usuario == "ALUNO DE GRADUAÇÃO"')
    alunos_graduacao_acervo_circulante = alunos_graduacao.query('colecao == "Acervo Circulante"')
    alunos_graduacao_acervo_circulante['ano'] = alunos_graduacao_acervo_circulante['data_emprestimo'].dt.year
    alunos_graduacao_acervo_circulante['mes'] = alunos_graduacao_acervo_circulante['data_emprestimo'].dt.month
    alunos_graduacao_acervo_circulante = alunos_graduacao_acervo_circulante[['ano', 'mes']]
    alunos_graduacao_acervo_circulante = alunos_graduacao_acervo_circulante.value_counts().to_frame('quantidade').reset_index()

    if not alunos_graduacao_acervo_circulante.empty:

        #Plotando o gráfico

        boxplot_colecao = px.box(
            alunos_graduacao_acervo_circulante,
            x = 'ano',
            y = 'quantidade'
        )

        boxplot_colecao.update_layout(
            
            xaxis = {
                'tickmode': 'linear',
                'title': None,
            },
            yaxis = {
                'title': None
            }
        )

        st.plotly_chart(boxplot_colecao, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico.")
else:
     st.warning("Nenhum dado para exibir no gráfico.")

st.markdown("---")
st.subheader('Por Alunos de Pós - Graduação do Acervo Circulante')

if not df_filtrado.empty:
     
    alunos_pos_graduacao = df_filtrado.query('tipo_vinculo_usuario == "ALUNO DE PÓS-GRADUAÇÃO"')
    alunos_pos_graduacao_acervo_circulante = alunos_pos_graduacao.query('colecao == "Acervo Circulante"')
    alunos_pos_graduacao_acervo_circulante['ano'] = alunos_pos_graduacao_acervo_circulante['data_emprestimo'].dt.year
    alunos_pos_graduacao_acervo_circulante['mes'] = alunos_pos_graduacao_acervo_circulante['data_emprestimo'].dt.month
    alunos_pos_graduacao_acervo_circulante = alunos_pos_graduacao_acervo_circulante[['ano', 'mes']]
    alunos_pos_graduacao_acervo_circulante = alunos_pos_graduacao_acervo_circulante.value_counts().to_frame('quantidade').reset_index()
    
    if not alunos_pos_graduacao_acervo_circulante.empty:
    
    #Plotando o gráfico

        boxplot_colecao_pos = px.box(
            alunos_pos_graduacao_acervo_circulante,
            x = 'ano',
            y = 'quantidade'
        )

        boxplot_colecao_pos.update_layout(
            
            xaxis = {
                'tickmode': 'linear',
                'title': None,
            },
            yaxis = {
                'title': None
            }
        )
        st.plotly_chart(boxplot_colecao_pos, key= 'pos_graduacao', use_container_width=True)
    else:
         st.warning("Nenhum dado para exibir no gráfico.")    
else:
     st.warning("Nenhum dado para exibir no gráfico.")

st.markdown("---")
st.markdown("Detalhes do dataframe")
st.dataframe(df_filtrado.head(50))
    



          
         
         




