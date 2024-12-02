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
    # folder_path = "./Volumes/gold/tse/consulta_cand" ## -- Usar essa se for rodar sem kubernetes
    folder_path = "/data/gold/tse/consulta_cand"

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


page = st.sidebar.selectbox('Página:', ['Candidatos', 'Bens declarados'])

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

# Título da aplicação
st.title("Gráfico de Pizza Subdividido por Grau de Instrução")

# Seleção dos estados
selected_states = st.multiselect(
    "Selecione os estados para incluir no gráfico:",
    options=data["SG_UF"].unique()
)

# Filtrar os dados com base nos estados selecionados
filtered_df = data[data["SG_UF"].isin(selected_states)]

# Agrupar os dados por grau de instrução e calcular o total de candidatos
grouped_df = (
    filtered_df.groupby(["SG_UF", "DS_GRAU_INSTRUCAO"], as_index=False)
    .agg({"SQ_CANDIDATO": "count"})
)

# Calcular a porcentagem para cada grau de instrução
total_candidatos = grouped_df["SQ_CANDIDATO"].sum()
grouped_df["Porcentagem"] = (
    grouped_df["SQ_CANDIDATO"] / total_candidatos) * 100

# Criar o gráfico de pizza subdividido por grau de instrução
fig = px.pie(
    grouped_df,
    names="DS_GRAU_INSTRUCAO",
    values="Porcentagem",
    color="DS_GRAU_INSTRUCAO",
    title=f"Distribuição de Grau de Instrução - {selected_states}",
    template="plotly",
    labels={"Porcentagem": "% de Candidatos"},
    hole=0.4  # Gráfico de rosca (opcional)
)
st.plotly_chart(fig)
