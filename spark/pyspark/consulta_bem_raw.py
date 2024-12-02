# %%
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (SparkSession.builder
         .appName("consulta_cand_raw")
         .master("spark://spark-master:7077") #.master("local[4]")
         .getOrCreate())

# %%
#Load Dataset
# source = "raw/tse/bem_candidato_2024"
# dest = "silver/tse/bem_candidato"
# volume_path = "../../Volumes/"

source = "raw/tse/bem_candidato"
dest = "silver/tse/bem_candidato"
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
#Clean Dataset

#Select Columns
columns = ["SQ_CANDIDATO", "NR_ORDEM_BEM_CANDIDATO", "CD_TIPO_BEM_CANDIDATO",
           "DS_TIPO_BEM_CANDIDATO", "DS_BEM_CANDIDATO", "VR_BEM_CANDIDATO"]

df = df.select(*columns)

#Removendo #NULO

df = df.replace(
  to_replace=["#NULO", "#NE"],
  value=None
)

df = df.replace(
  to_replace=[-3, -1, -4],
  value=None
)



#Transforming string value to double
df = df.withColumn("VR_BEM_CANDIDATO", F.regexp_replace(df["VR_BEM_CANDIDATO"], ",", "."))
df = df.withColumn("VR_BEM_CANDIDATO", df["VR_BEM_CANDIDATO"].cast("double"))

df.show()
df.printSchema()

# %%
# Saving DataFrame
df.write.csv(output_path, header=True, mode="overwrite")

# %%
spark.stop()

