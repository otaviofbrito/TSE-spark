import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import glob

# Configurar título e descrição
st.title("Análise de Dados de Eleições")
st.write("Este dashboard apresenta gráficos dos dados de eleições brasileiras de 2024 processados.")

# Carregar Dados
@st.cache_data
def load_data():
    # Substitua pelo caminho para o diretório onde o arquivo está localizado
    folder_path = "./Volumes/gold/tse/consulta_cand"
    
    # Encontra o único arquivo CSV na pasta
    file_path = glob.glob(f"{folder_path}/part-*.csv")
    
    # Verifica se algum arquivo foi encontrado
    if not file_path:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado na pasta especificada. {file_path}")
    
    # Como esperamos apenas um arquivo, selecionamos o primeiro
    file_path = file_path[0]
    
    # Carrega o arquivo CSV no DataFrame
    return pd.read_csv(file_path)


page = st.sidebar.selectbox('Escolha uma página', ['Página 1', 'Página 2'])

data = load_data()

# Exibir amostra de dados
if st.checkbox("Mostrar dados brutos"):
    st.write(data.head())

# Filtro
columns = st.multiselect("Selecione colunas para análise", data.columns.tolist())
if columns:
    st.write(data[columns])

# Gráficos
st.subheader("Gráficos Interativos")

# Gráfico Matplotlib
st.write("Gráfico de Barras (Matplotlib)")
fig, ax = plt.subplots()
data["SG_PARTIDO"].value_counts().plot(kind="bar", ax=ax)
st.pyplot(fig)

# Gráfico Seaborn
st.write("Gráfico de Dispersão (Seaborn)")
fig, ax = plt.subplots()
sns.scatterplot(data=data, x="SG_PARTIDO", y="VR_BEM_TOTAL", ax=ax)
st.pyplot(fig)

# Gráfico Plotly
st.write("Gráfico de Linhas (Plotly)")
fig = px.line(data, x="SG_PARTIDO", y="VR_BEM_TOTAL", title="Gráfico Interativo")
st.plotly_chart(fig)

