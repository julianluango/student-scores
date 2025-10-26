from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

##Crear sesión Spark
spark =( SparkSession.builder
    .appName("BatchScoreStudent-ETL")
    .getOrCreate())

##Cargar dataset
input_path = "./data/student_exam_scores.csv"
df = spark.read.option("header", True).option("inferSchema", True).csv(input_path)

print("===== ESQUEMA INICIAL =====")
df.printSchema()

print("===== PRIMERAS FILAS =====")
df.show(5)

# ==================================================
## EDA INICIAL - PRE LIMPIEZA
# ==================================================

print("===== CONTEO DE NULOS POR COLUMNA =====")
df.select([F.count(F.when(F.col(c).isNull() | F.isnan(c), c)).alias(c) for c in df.columns]).show()

print("===== CONTEO DE DUPLICADOS =====")
duplicados = df.count() - df.dropDuplicates().count()
print(f"Total duplicados: {duplicados}")

print("===== ESTADISTICAS DESCRIPTIVAS =====")
df.describe().show()

# ==================================================
## TRANSFORMACIONES Y LIMPIEZA BÁSICA
# ==================================================

# Eliminar duplicados
df_clean = df.dropDuplicates()

# Eliminar filas con nulos en columnas críticas
df_clean = df_clean.dropna(subset=["exam_score", "hours_studied"])

# Modificar los tipos de datos
for col_name in ["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]:
    df_clean = df_clean.withColumn(col_name, F.col(col_name).cast(DoubleType()))

# Crear columna categórica de desempeño según la nota
df_transformed = df_clean.withColumn(
    "performance_level",
    F.when(F.col("exam_score") >= 90, "Excelente").otherwise(
     F.when(F.col("exam_score") >= 75, "Bueno").otherwise(
     F.when(F.col("exam_score") >= 60, "Regular")
     .otherwise("Bajo")))
)

# Crear columna de ratio: horas de estudio / horas de sueño
df_transformed = df_transformed.withColumn("study_sleep_ratio", F.round(F.col("hours_studied") / F.col("sleep_hours"), 2)
)

# ==================================================
## EDA FINAL - POST LIMPIEZA
# ==================================================

print("===== ESTADISTICAS DESCRIPTIVAS POST-LIMPIEZA =====")
df_transformed.describe(["hours_studied", "sleep_hours", "attendance_percent", "previous_scores", "exam_score"]).show()

print("===== DISTRIBUCIoN POR NIVEL DE DESEMPEÑO =====")
df_transformed.groupBy("performance_level").count().orderBy(F.col("count").desc()).show()

print("===== PROMEDIO DE EXAMEN SEGuN ASISTENCIA =====")
df_transformed.groupBy(
    F.when(F.col("attendance_percent") >= 90, "Alta Asistencia").otherwise(
     F.when(F.col("attendance_percent") >= 70, "Media Asistencia")
     .otherwise("Baja Asistencia"))
     .alias("attendance_group")
).agg(F.round(F.avg("exam_score"), 2).alias("avg_exam_score")).orderBy("avg_exam_score", ascending=False).show()


# ==================================================
## GUARDAR DATOS PROCESADOS
# ==================================================
1
output_path = "./data/processed_student_exam_scores.csv"
df_transformed.write.mode("overwrite").csv(output_path)

print(f"Datos procesados guardados en: {output_path}")

# ==================================================
## CIERRE DE SESION SPARK
# ==================================================
spark.stop()
