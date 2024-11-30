# %%
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("consulta_cand_raw").getOrCreate()

# %%
#Load Dataset
source = "consulta_cand_2024"
volume_path = "../../Volumes/raw/tse"
folder_path = f"{volume_path}/{source}"
file_path = f"{folder_path}/*BRASIL.csv"

df = spark.read.csv(file_path,
                    sep=';',
                    header=True,
                    encoding='latin1',
                    inferSchema=True,
                    multiLine=True)



# %%
#Clean Dataset


# %%
spark.stop()

# %%
