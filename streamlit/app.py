import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração da função de carregamento de dados


@st.cache_data
def load_data():
    # folder_path = "./Volumes/gold/tse/consulta_cand"
    folder_path = "/data/gold/tse/consulta_cand"
    file_path = glob.glob(f"{folder_path}/part-*.csv")

    if not file_path:
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado na pasta especificada: {file_path}"
        )

    file_path = file_path[0]
    return pd.read_csv(file_path)


# Navegação entre páginas
page = st.sidebar.selectbox(
    'Página:', ['Candidatos', 'Grau de Instrução', 'Bens Declarados'])

# Carregar os dados
data = load_data()

if page == 'Candidatos':
    # Página: Candidatos
    st.title("Análise de Dados de Candidatos - 2024")
    st.write(
        "Este dashboard apresenta gráficos dos dados de eleições brasileiras de 2024 processados.")

    # Mostrar dados brutos
    if st.checkbox("Mostrar dados brutos"):
        st.write(data.head())

    # Seleção de colunas
    columns = st.multiselect(
        "Selecione colunas para análise", data.columns.tolist())
    if columns:
        st.write(data[columns])

    # Gráfico: Distribuição por Estado e Gênero
    st.subheader("1. Distribuição de Candidatos por Estado e Gênero")
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
        barmode="stack",
    )
    st.plotly_chart(fig)

    # Gráfico: Distribuição por Estado e Raça
    st.subheader("2. Distribuição de Candidatos por Estado e Raça")
    grouped_data = data.groupby(
        ["SG_UF", "DS_COR_RACA"]).size().reset_index(name="NUM_CANDIDATOS")
    fig = px.bar(
        grouped_data,
        x="SG_UF",
        y="NUM_CANDIDATOS",
        color="DS_COR_RACA",
        title="Distribuição de Candidatos por Estado e Raça",
        labels={"NUM_CANDIDATOS": "Nº de Candidatos",
                "SG_UF": "Estado", "DS_COR_RACA": "Raça"},
        barmode="stack",
    )
    st.plotly_chart(fig)

elif page == 'Grau de Instrução':
    # Página: Grau de Instrução
    st.title("Análise do Grau de Instrução")
    st.write("Visualize os dados sobre  grau de instrução dos candidatos")

    # Seleção por estado
    selected_states = st.multiselect(
        "Selecione os estados para análise:",
        options=data["SG_UF"].unique()
    )

    if selected_states:
        filtered_df = data[data["SG_UF"].isin(selected_states)]
        grouped_df = (
            filtered_df.groupby(["DS_GRAU_INSTRUCAO"], as_index=False)
            .agg({"SQ_CANDIDATO": "count"})
        )
        grouped_df["Porcentagem"] = (
            grouped_df["SQ_CANDIDATO"] / grouped_df["SQ_CANDIDATO"].sum()) * 100

        # Gráfico de pizza
        fig = px.pie(
            grouped_df,
            names="DS_GRAU_INSTRUCAO",
            values="Porcentagem",
            title=f"Distribuição de Grau de Instrução - {
                ', '.join(selected_states)}",
        )
        st.plotly_chart(fig)
    else:
        st.write("Selecione ao menos um estado para visualizar os gráficos.")

elif page == 'Bens Declarados':
    # Página: Candidatos
    data['VR_BEM_TOTAL'] = data['VR_BEM_TOTAL'].astype(
        float)  # Certificar que é numérico
    columns_to_keep = ['SG_UF', 'DS_GENERO', 'SG_PARTIDO', 'VR_BEM_TOTAL']
    filtered_data = data[columns_to_keep]

    st.title("Análise de Bens Declarados pelos Candidatos - 2024")

    # Gráfico 3: Total de bens declarados por partido
    st.subheader("Total de Bens Declarados por Partido")
    party_grouped = filtered_data.groupby(
        "SG_PARTIDO")["VR_BEM_TOTAL"].sum().reset_index()
    fig = px.bar(
        party_grouped,
        x="SG_PARTIDO",
        y="VR_BEM_TOTAL",
        title="Total de Bens Declarados por Partido",
        labels={"SG_PARTIDO": "Partido",
                "VR_BEM_TOTAL": "Total de Bens Declarados"},
        template="plotly_white"
    )
    st.plotly_chart(fig)

    # Gráfico 4: Média de bens declarados por estado
    st.subheader("Média de Bens Declarados por Estado")
    state_grouped = filtered_data.groupby(
        "SG_UF")["VR_BEM_TOTAL"].mean().reset_index()
    fig = px.bar(
        state_grouped,
        x="SG_UF",
        y="VR_BEM_TOTAL",
        title="Média de Bens Declarados por Estado",
        labels={"SG_UF": "Estado", "VR_BEM_TOTAL": "Média dos Bens Declarados"},
        template="plotly_white"
    )
    st.plotly_chart(fig)

    # Criar ranking dos mais ricos
    st.subheader("Ranking dos Candidatos Mais Ricos - 2024")
    top_n = st.slider("Selecione o número de candidatos para exibir:",
                      min_value=5, max_value=20, value=10)

    # Ordenar por VR_BEM_TOTAL em ordem decrescente
    ranking = data.sort_values(by="VR_BEM_TOTAL", ascending=False).head(top_n)

    # Exibir tabela do ranking
    st.subheader(f"Top {top_n} Candidatos Mais Ricos")
    st.write(ranking[["NM_CANDIDATO", "SG_UF", "DS_CARGO", "VR_BEM_TOTAL"]])

    # Criar gráfico de barras para os mais ricos
    st.subheader("Visualização dos Candidatos Mais Ricos")
    fig = px.bar(
        ranking,
        x="NM_CANDIDATO",
        y="VR_BEM_TOTAL",
        color="SG_UF",
        title=f"Top {top_n} Candidatos Mais Ricos",
        labels={"NM_CANDIDATO": "Candidato",
                "VR_BEM_TOTAL": "Valor dos Bens Declarados"},
        template="plotly_white",
        text_auto=True
    )
    st.plotly_chart(fig)
