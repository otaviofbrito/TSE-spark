# %%
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date
spark = (SparkSession.builder
         .appName("consulta_cand_raw")
         .master("spark://spark-master:7077")  # .master("local[4]")
         .getOrCreate())

# %%
# Load Dataset
# source = "raw/tse/consulta_cand_2024"
# dest = "silver/tse/consulta_cand"
# volume_path = "../../Volumes/"
# folder_path = f"{volume_path}/{source}"
# file_path = f"{folder_path}/*BRASIL.csv"
# output_path = f"{volume_path}/{dest}"

source = "raw/tse/consulta_cand"
dest = "silver/tse/consulta_cand"
volume_path = "/app/spark/data"
folder_path = f"{volume_path}/{source}"
file_path = f"{folder_path}/*BRASIL.csv"
output_path = f"{volume_path}/{dest}"

df = spark.read.csv(file_path,
                    sep=';',
                    header=True,
                    encoding='latin1',
                    inferSchema=True,
                    multiLine=True)

# %%
# Clean Dataset

# Select Columns
columns = ["CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "CD_ELEICAO",
           "DS_ELEICAO", "SG_UF", "NM_UE", "CD_CARGO", "DS_CARGO", "SQ_CANDIDATO",
           "NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "SG_PARTIDO",
           "NM_PARTIDO", "NR_PARTIDO", "SG_UF_NASCIMENTO", "DT_NASCIMENTO",
           "CD_GENERO", "DS_GENERO", "CD_GRAU_INSTRUCAO", "DS_GRAU_INSTRUCAO",
           "CD_ESTADO_CIVIL", "DS_ESTADO_CIVIL", "CD_COR_RACA", "DS_COR_RACA",
           "CD_OCUPACAO", "DS_OCUPACAO"]

df = df.select(*columns)

# Removendo #NULO

df = df.replace(
    to_replace=["#NULO", "#NE"],
    value=None
)

df = df.replace(
    to_replace=[-3, -1, -4],
    value=None
)

# Corrigindo Data
df = df.withColumn("DT_NASCIMENTO", to_date("DT_NASCIMENTO", "dd/MM/yyyy"))


# %%
# Saving DataFrame
df.write.csv(output_path, header=True, mode="overwrite")

# %%
spark.stop()
