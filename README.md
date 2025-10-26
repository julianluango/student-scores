# 🤓 Student Exam Scores - PySpark ETL & EDA

Este proyecto implementa un flujo **ETL y de Análisis Exploratorio de Datos (EDA)** completo sobre el dataset `student_exam_scores.csv` utilizando **Apache PySpark**.

Se aplica un proceso profesional de limpieza, transformación y análisis, siguiendo las mejores prácticas de ingeniería de datos.

---

## 📊 Descripción del dataset

El dataset contiene información sobre el rendimiento de estudiantes en exámenes, con variables relacionadas al estudio, sueño y asistencia.

**Columnas:**
| Columna | Descripción |
|----------|--------------|
| `student_id` | Identificador único del estudiante |
| `hours_studied` | Horas de estudio promedio por día |
| `sleep_hours` | Promedio de horas de sueño por día |
| `attendance_percent` | Porcentaje de asistencia a clase |
| `previous_scores` | Puntaje promedio en exámenes previos |
| `exam_score` | Puntaje obtenido en el examen actual |

---

## ⚙️ Requisitos

Asegúrate de tener instalado:

- [Python 3.8+](https://www.python.org/downloads/)
- [Apache Spark 3.0+](https://spark.apache.org/downloads.html)
- [pyspark](https://pypi.org/project/pyspark/)

Instalación rápida de PySpark:

```bash
pip install pyspark
```

---

## 🧩 Estructura del proyecto

```
student_exam_scores/
│
├── data/
│   └── student_exam_scores.csv
│
├── output/
│   └── processed_student_exam_scores.parquet
│
├── scripts/
│   └── student_exam_scores_etl.py
│
└── README.md
```

---

## 🚀 Ejecución del script

Ejecuta el proceso ETL en tu entorno local de Spark:

```bash
spark-submit scripts/student_exam_scores_etl.py
```

> 💡 También puedes ejecutarlo directamente desde un notebook PySpark o Databricks.

---

## 🔍 Flujo del proceso ETL

El proceso está dividido en tres fases principales:

### 1️⃣ EDA Inicial
- Inspección de esquema y tipos de datos.  
- Conteo de valores nulos y duplicados.  
- Estadísticas descriptivas básicas.  

### 2️⃣ Transformaciones básicas
- Conversión de tipos numéricos.  
- Eliminación de nulos y duplicados.  
- Creación de nuevas columnas:
  - `performance_level`: categoría según puntaje del examen.  
  - `study_sleep_ratio`: proporción entre horas de estudio y horas de sueño.  
  - `exam_score_normalized`: nota normalizada entre 0 y 1.  

### 3️⃣ EDA Final
- Distribución por nivel de desempeño.  
- Promedios por grupos de asistencia.  
- Correlaciones entre variables numéricas.  
- Estadísticas finales tras la limpieza.  

---

## 💾 Resultados

El dataset procesado se guarda en formato **Parquet**, optimizado para análisis posteriores.

**Ruta de salida:**
```
output/processed_student_exam_scores.parquet
```

El archivo contiene columnas limpias y enriquecidas, listas para ser analizadas o cargadas en herramientas como Power BI, Databricks o Spark SQL.

---

## 📈 Ejemplo de salida

| student_id | hours_studied | sleep_hours | attendance_percent | previous_scores | exam_score | performance_level | study_sleep_ratio | exam_score_normalized |
|-------------|---------------|--------------|--------------------|-----------------|-------------|--------------------|-------------------|-----------------------|
| S001 | 8.0 | 8.8 | 72.1 | 45 | 30.2 | Bajo | 0.91 | 0.12 |
| S004 | 3.5 | 4.8 | 95.1 | 66 | 34.0 | Bajo | 0.73 | 0.21 |
| S009 | 6.2 | 7.5 | 85.3 | 77 | 78.0 | Bueno | 0.83 | 0.69 |

---

## 🧮 Tecnologías usadas

- **Apache Spark** – Procesamiento distribuido
- **PySpark DataFrames** – Transformación y análisis estructurado
- **Python** – Script principal y automatización
- **Parquet** – Almacenamiento optimizado de salida

---

## 🧑‍💻 Autor

**Julian Montenegro**  
Ingeniero de Datos | Análisis y procesamiento de datos con PySpark y Azure  
📧 Contacto: *(agrega tu correo o LinkedIn si deseas)*

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Puedes usarlo y modificarlo libremente citando al autor original.

