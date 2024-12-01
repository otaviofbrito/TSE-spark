# %%
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (SparkSession.builder
         .appName("consulta_cand_raw")
         .master("local[4]")
         .getOrCreate())

# %%
# Load Dataset
source1 = "silver/tse/bem_candidato"
source2 = "silver/tse/consulta_cand"
dest = "gold/tse/consulta_cand"
volume_path = "../../Volumes/"
folder_path1 = f"{volume_path}/{source1}"
folder_path2 = f"{volume_path}/{source2}"
file_path1 = f"{folder_path1}/*.csv"
file_path2 = f"{folder_path2}/*.csv"
output_path = f"{volume_path}/{dest}"

df = spark.read.csv(file_path1,
                    header=True,
                    inferSchema=True)

df2 = spark.read.csv(file_path2,
                    header=True,
                    inferSchema=True)

# %%

result = (df.groupBy("SQ_CANDIDATO")
          .agg(F.sum("VR_BEM_CANDIDATO").alias("VR_BEM_TOTAL")))

result = result.withColumn("VR_BEM_TOTAL", F.round(F.col("VR_BEM_TOTAL"), 2))

df2 = df2.join(result, on="SQ_CANDIDATO", how="left")


# %%
# Saving DataFrame
df2.coalesce(1).write.csv(output_path, header=True, mode="overwrite")

# %%
spark.stop()
