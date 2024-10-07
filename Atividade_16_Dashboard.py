pip install matplotlib

import pandas as pd
import streamlit as st
#import seaborn as sns
import matplotlib.pyplot as plt
#import altair as alt


#st.title('Imoveis para Alugar no Brasil')
st.header("Imoveis para Alugar no Brasil", divider=True)


@st.cache_data
def carregar_dados (caminho_arquivo):
    dados = pd.read_csv(caminho_arquivo)

    #Renomear as colunas
    dados.rename(columns = {'city':'Cidade', 
        'area':'Area',
        'rooms':'Quartos',
        'bathroom':'Banheiros',
        'parking spaces':'Garagens',
        'floor':'Andar da Casa',
        'animal':'Animal',
        'furniture':'Mobiliada',
        'hoa (R$)':'Taxa Condomínio (R$)',
        'rent amount (R$)':'Valor do Aluguel(R$)',
        'property tax (R$)':'Taxa IPTU (R$)',
        'fire insurance (R$)':'Seguro Incêncio (R$)',
        'total (R$)':'Total (R$)'},
        inplace = True)

    return dados

# Carregando os dados
df = carregar_dados(r'C:\Users\HP\OneDrive\Documentos\Educacao\AD e IA - UFMA\2 Modulo\6 - Visualizacao de Dados\Unidade 3\18. Atividade 16_Entrega\Material\houses_to_rent_v2.csv')

#--------------------------------------------
# Exibir o valor médio do aluguel
st.subheader('Valor Médio do Aluguel (R$):')
st.write(f'{df["Valor do Aluguel(R$)"].mean():.2f}')

#--------------------------------------------
# Agrupando e contando
df_contagem_casas = df['Cidade'].value_counts().reset_index()
df_contagem_casas.columns = ['Cidade', 'Quantidade de casas']

# Ordenando o DataFrame pela quantidade de casas em ordem decrescente
df_contagem_casas = df_contagem_casas.sort_values(by='Quantidade de casas', ascending=False)

# Título da aplicação
st.subheader('Concentração de Casas por Cidade')

# Criando o gráfico de barras
st.bar_chart(df_contagem_casas, x='Cidade', y='Quantidade de casas')

#----------------------------------------

# Calcula o total do valor do aluguel e da área por cidade
df['Valor por m²'] = df['Valor do Aluguel(R$)'] / df['Area']
df_summary = df.groupby('Cidade').agg({'Valor por m²': 'mean'}).reset_index()

# Criação do gráfico
st.subheader('Valor do Aluguel/m² por Cidade')

plt.figure(figsize=(10, 6))
bars = plt.bar(df_summary['Cidade'], df_summary['Valor por m²'], color='skyblue')
plt.xlabel('Cidade')
plt.ylabel('Valor do Aluguel por m² (R$)')
plt.title('Valor do Aluguel/m² por Cidade')
#plt.xticks(rotation=45)

# Adiciona os valores no topo das barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', 
             ha='center', va='bottom')  # Ajuste de posição do texto

plt.tight_layout()

# Exibir o gráfico no Streamlit
st.pyplot(plt)

#----------------------------------
# Comparação entre mobiliados e não mobiliados

st.subheader('Comparação de Valores de Aluguel: Mobiliados vs Não Mobiliados')

# Agrupamento por cidade e tipo de imóvel
df_mobiliados = df.groupby(['Cidade', 'Mobiliada']).agg({'Valor do Aluguel(R$)': 'mean'}).reset_index()

# Configurando gráfico
fig, ax = plt.subplots(figsize=(8, 6))

for mobiliada_status in df_mobiliados['Mobiliada'].unique():
    subset = df_mobiliados[df_mobiliados['Mobiliada'] == mobiliada_status]
    ax.bar(subset['Cidade'], subset['Valor do Aluguel(R$)'], label=f'Mobiliada: {mobiliada_status}')

# Configurações do gráfico
ax.set_title('Comparação de Aluguel por Cidade (Mobiliados x Não Mobiliados)')
ax.set_xlabel('Cidade')
ax.set_ylabel('Valor do Aluguel (R$)')
ax.legend()

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

# Exibir a tabela no Streamlit
st.subheader("Tabela de Imóveis para alugar no rasil")
st.dataframe(df)
