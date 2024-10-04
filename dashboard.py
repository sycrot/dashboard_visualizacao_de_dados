import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    file_path = 'houses_to_rent.csv'
    
    df = pd.read_csv(file_path)

    # Remove white spaces
    df.columns = df.columns.str.strip()
    
    df['hoa'] = df['hoa'].replace({'R\$': '', ',': '', 'Sem info': '0', 'Incluso': '0'}, regex=True).astype(float)
    df['rent amount'] = df['rent amount'].replace({'R\$': '', ',': '', 'Sem info': '0', 'Incluso': '0'}, regex=True).astype(float)
    df['property tax'] = df['property tax'].replace({'R\$': '', ',': '', 'Sem info': '0', 'Incluso': '0'}, regex=True).astype(float)
    df['fire insurance'] = df['fire insurance'].replace({'R\$': '', ',': '', 'Sem info': '0', 'Incluso': '0'}, regex=True).astype(float)
    df['total'] = df['total'].replace({'R\$': '', ',': '', 'Sem info': '0', 'Incluso': '0'}, regex=True).astype(float)

    df = df.rename(columns={
        'city': 'Cidade',
        'area': 'Área (m²)',
        'rooms': 'Quartos',
        'bathroom': 'Banheiros',
        'parking spaces': 'Vagas de Estacionamento',
        'animal': 'Aceita Animais',
        'furniture': 'Mobiliado',
        'rent amount': 'Valor do Aluguel',
        'property tax': 'IPTU',
        'fire insurance': 'Seguro Incêndio',
        'total': 'Total de Despesas',
        'floor': 'Andar'
    })

    return df

df = load_data()

st.markdown("""
    <style>
    .custom-subheader {
        font-size: 18px !important;
        font-weight: bold;
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)
st.title('Dashboard de Imóveis para Aluguel')
# Mostrar os primeiros registros
st.write('Visualização dos dados:')
st.dataframe(df.head())


# Criar as colunas
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

city_counts = df['Cidade'].value_counts().reset_index()
city_counts.columns = ['Cidade', 'Número de imóveis']

# Gráfico de dispersão do valor do aluguel em relação à área
fig1 = px.scatter(df, x='Área (m²)', y='Valor do Aluguel', color='Cidade',
title='Valor do Aluguel por Área (m²)', 
labels={'Área (m²)': 'Área (m²)', 'Valor do Aluguel': 'Valor do Aluguel'},
template='plotly_white')
col1.plotly_chart(fig1)

cols = col2.columns(len(city_counts))
for i, row in city_counts.iterrows():
    cols[i].metric(label=f"Cidade {str(row['Cidade'])}", value=f"{row['Número de imóveis']} imóveis")

# Gráfico de barras do número de imóveis por cidade

fig2 = px.bar(city_counts, x='Cidade', y='Número de imóveis',
title='Número de Imóveis por Cidade',
labels={'Cidade': 'Cidade', 'Número de Imóveis': 'Número de Imóveis'},
color='Cidade')
col3.plotly_chart(fig2)

# Gráfico de pizza para distribuição de imóveis mobiliados
fig3 = px.pie(df, names='Mobiliado', title='Distribuição de Imóveis Mobiliados')
col4.plotly_chart(fig3)

# Gráfico de violino do valor do aluguel por número de quartos
fig4 = px.violin(df, x='Quartos', y='Valor do Aluguel', box=True, points='all',
title='Distribuição do Valor do Aluguel por Quartos')
col5.plotly_chart(fig4)
