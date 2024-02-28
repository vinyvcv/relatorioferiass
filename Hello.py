import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurações iniciais do Streamlit
st.set_page_config(layout='wide', page_title='Planejamento Anual de Férias')
st.sidebar.image('hapvidalogo.png', width=200)
st.image('hapvidalogo.png', width=500)

# Carregar dados do Excel
excel_path = 'Quadro_Combinado_Atualizado_Com_Anos.xlsx'
df = pd.read_excel(excel_path)

# Preparação dos dados
df['LIMITE'] = pd.to_datetime(df['LIMITE'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
df['INÍCIO'] = pd.to_datetime(df['INÍCIO'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
df['FIM'] = pd.to_datetime(df['FIM'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
df['ANO LIMITE'] = pd.to_datetime(df['LIMITE'], format='%d/%m/%Y').dt.year
df['ANO LIMITE'] = df['ANO LIMITE'].fillna(0).astype(int)

# Sidebar com filtros
st.sidebar.header('Filtros')
todos_responsaveis = ['Selecionar Tudo'] + list(df['RESPONSAVEL'].unique())
selecao_responsavel = st.sidebar.multiselect('Selecione o Responsável', options=todos_responsaveis, default=['Selecionar Tudo'])
todos_meses = ['Selecionar Tudo'] + list(df['MÊS FÉRIAS'].dropna().unique())
selecao_mes = st.sidebar.multiselect('Selecione o Mês de Férias', options=todos_meses, default=['Selecionar Tudo'])
todos_servicos = ['Selecionar Tudo'] + list(df['SERVIÇO'].unique())
selecao_servico = st.sidebar.multiselect('Selecione o Serviço', options=todos_servicos, default=['Selecionar Tudo'])

# Aplicando os filtros
filtered_df = df.copy()
if 'Selecionar Tudo' not in selecao_responsavel:
    filtered_df = filtered_df[filtered_df['RESPONSAVEL'].isin(selecao_responsavel)]
if 'Selecionar Tudo' not in selecao_mes:
    filtered_df = filtered_df[filtered_df['MÊS FÉRIAS'].isin(selecao_mes)]
if 'Selecionar Tudo' not in selecao_servico:
    filtered_df = filtered_df[filtered_df['SERVIÇO'].isin(selecao_servico)]

# Exibição dos dados filtrados
if st.button('Mostrar Detalhes dos Funcionários'):
    st.dataframe(filtered_df[['NOME', 'SERVIÇO','RESPONSAVEL', 'MÊS FÉRIAS', 'LIMITE', 'INÍCIO', 'FIM', 'QUANTIDADE']], width=1500, height=800)

# Código para os gráficos segue aqui...

meses_ordem = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 
               'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
df['MÊS FÉRIAS'] = pd.Categorical(df['MÊS FÉRIAS'], categories=meses_ordem, ordered=True)

# Gráficos
# Quantidade de Funcionários por Serviço
servico_counts = df['SERVIÇO'].value_counts()
fig_servico = px.bar(servico_counts, title="Funcionários por Serviço", labels={'index': 'Serviço', 'value': 'Quantidade'}, color_discrete_sequence=['blue']) 
fig_servico.update_layout(width=1200)
st.plotly_chart(fig_servico) 


# Funcionários Tirando Férias por Mês
ferias_counts = df['MÊS FÉRIAS'].value_counts().sort_index()
fig_ferias = px.bar(ferias_counts, title="Funcionários Tirando Férias por Mês", labels={'index': 'Mês', 'value': 'Quantidade'}, color_discrete_sequence=['yellow'])
fig_ferias.update_layout(width=1200)
st.plotly_chart(fig_ferias)

# Funcionários com Limite por Mês
# Nota: Requer ajuste na coluna 'LIMITE' conforme sua estrutura de dados




# Mapeamento dos meses para ordenação
meses_ordem = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 
               'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

# Certifique-se de que a coluna 'MÊS FÉRIAS' está em maiúsculas
df['MÊS FÉRIAS'] = df['MÊS FÉRIAS'].str.upper()

# Crie uma nova coluna 'MÊS ORDEM' com base na lista de ordenação de meses
df['MÊS ORDEM'] = df['MÊS FÉRIAS'].apply(lambda x: meses_ordem.index(x) if x in meses_ordem else -1)

# Filtrar o DataFrame pelo responsável selecionado na interface do usuário
responsavel_selecionado = st.sidebar.selectbox('Selecione o Responsável', options=df['RESPONSAVEL'].unique(), key='select_responsavel')

# Filtragem de dados pelo responsável e pela coluna 'LIMITE' já convertida para o formato de data
df_filtrado = df[(df['RESPONSAVEL'] == responsavel_selecionado)]




