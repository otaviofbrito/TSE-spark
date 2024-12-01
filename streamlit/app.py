import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import glob
import plotly.io as pio

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
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado na pasta especificada. {file_path}")

    # Como esperamos apenas um arquivo, selecionamos o primeiro
    file_path = file_path[0]

    # Carrega o arquivo CSV no DataFrame
    return pd.read_csv(file_path)


page = st.sidebar.selectbox('Escolha uma página', ['Página 1', 'Página 2'])

data = load_data()


# SECTION 1
# DIV 1
if st.checkbox("Mostrar dados brutos"):
    st.write(data.head())

columns = st.multiselect(
    "Selecione colunas para análise", data.columns.tolist())
if columns:
    st.write(data[columns])

# SECTION 2
st.subheader("Gráficos Interativos")
# DIV 1
st.subheader("1. Distribuição de Candidatos por Estado e Gênero")
st.write("Gráfico de barras empilhadas mostrando o número de candidatos por estado, divididos por Gênero.")
grouped_data = data.groupby(
    ["SG_UF", "DS_GENERO"]).size().reset_index(name="NUM_CANDIDATOS")

fig = px.bar(
    grouped_data,
    x="SG_UF",
    y="NUM_CANDIDATOS",
    color="DS_GENERO",
    title="Distribuição de Candidatos por Estado e Gênero",
    labels={"NUM_CANDIDATOS": "Nº de Candidatos",
            "SG_UF": "Estado", "DS_GENERO": "Gênero"},
    barmode="stack",  # Configuração para barras empilhadas
    color_discrete_map={"MASCULINO": "blue",
                        "FEMININO": "pink"}  # Personalização de cores
)
st.plotly_chart(fig)

# DIV 2
st.subheader("2. Distribuição de Candidatos por Estado e Raça")
st.write("Gráfico de barras empilhadas mostrando o número de candidatos por estado, divididos por Raça.")
grouped_data = data.groupby(
    ["SG_UF", "DS_COR_RACA"]).size().reset_index(name="NUM_CANDIDATOS")

fig = px.bar(
    grouped_data,
    x="SG_UF",
    y="NUM_CANDIDATOS",
    color="DS_COR_RACA",
    title="Distribuição de Candidatos por Estado e Gênero",
    labels={"NUM_CANDIDATOS": "Nº de Candidatos",
            "SG_UF": "Estado", "DS_GENERO": "Gênero"},
    barmode="stack"  # Personalização de cores
)
st.plotly_chart(fig)

# DIV 3
st.subheader("2. Distribuição de Candidatos por Estado e Raça")
st.write("Gráfico de barras empilhadas mostrando o número de candidatos por estado, divididos por Raça.")
grouped_data = data.groupby(
    ["SG_UF", "DS_GRAU_INSTRUCAO"]).size().reset_index(name="NUM_CANDIDATOS")

fig = px.bar(
    grouped_data,
    x="SG_UF",
    y="NUM_CANDIDATOS",
    color="DS_COR_RACA",
    title="Distribuição de Candidatos por Estado e Gênero",
    labels={"NUM_CANDIDATOS": "Nº de Candidatos",
            "SG_UF": "Estado", "DS_GRAU_INSTRUCAO": "Gênero"},
    barmode="stack"  # Personalização de cores
)
st.plotly_chart(fig)

