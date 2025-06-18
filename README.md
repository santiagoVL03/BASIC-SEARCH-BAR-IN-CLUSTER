# Sistema de Motor de Búsqueda con Índice Invertido - Hadoop HDFS

## 📋 Descripción General

Este repositorio implementa un sistema completo de motor de búsqueda basado en **índice invertido** utilizando **Hadoop HDFS** como sistema de almacenamiento distribuido. El sistema procesa videos, extrae metadata usando inteligencia artificial (YOLO), y construye un índice invertido que permite búsquedas eficientes de objetos detectados en los videos.

## 🏗️ Arquitectura del Sistema

```
Videos → Procesamiento IA → Metadata JSON → Preprocesamiento → CSV → HDFS → Índice Invertido → Motor de Búsqueda
```

### Componentes Principales:

1. **Procesamiento de Videos** (`Src/`)
2. **Preprocesamiento de Datos** (`Utils/`)
3. **Subida a HDFS** (`Cluster/`)
4. **MapReduce** (`Index/`)
5. **Spark Processing** (`spark/`)
6. **Consultas Hive** (`hive/system/`)

## 🔄 Flujo de Procesamiento Completo

### 1. Procesamiento Inicial de Videos 🎥

**Archivo:** `Src/process_video.py`

Este módulo es el punto de entrada del sistema:

- **Entrada:** Videos en formatos `.mp4`, `.avi`, `.mov`, `.mkv`, `.mpg`
- **Procesamiento:** 
  - Extrae frames cada 100 frames del video
  - Utiliza **YOLO v8** para detectar objetos en cada frame
  - Genera bounding boxes, confianza y clasificaciones
- **Salida:** Archivos JSON con metadata de detecciones

```python
# Ejemplo de metadata generada:
{
  "frame_001.jpg": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.85,
      "bbox": [100, 200, 300, 400]
    }
  ]
}
```

### 2. Preprocesamiento y Limpieza 🧹

**Funciones de utilidad:** `Utils/functions.py`

- Elimina inconsistencias en los datos
- Normaliza formatos de metadata
- Convierte JSON a formato CSV/TXT para Hive
- Valida integridad de los datos

### 3. Subida a Hadoop HDFS 📤

**Archivo:** `Cluster/upload_to_hdfs.py`

Este script gestiona la subida organizada de archivos al sistema HDFS:

```bash
# Estructura en HDFS:
/oursystem/
├── input/
│   ├── video/          # Videos originales
│   ├── metadata/       # JSON metadata
│   ├── metadata_table/ # CSV/TXT procesados
│   └── logs/          # Logs del sistema
└── output/
    └── page_rank/     # Resultados de ranking
```

**Funcionalidades:**
- Crea directorios automáticamente en HDFS
- Clasifica archivos por tipo (videos, metadata, logs)
- Maneja errores de subida
- Verifica integridad de archivos

### 4. Procesamiento con MapReduce 🗺️

**Archivos:** `Index/map.py` y `Index/reduce.py`

Implementación clásica de MapReduce para crear el índice invertido:

#### Map Phase (`map.py`):
```python
# Entrada: JSON metadata
# Proceso: Extrae pares (video_name, class_name)
# Salida: video_name\tclass_name
```

#### Reduce Phase (`reduce.py`):
```python
# Entrada: Pares agrupados
# Proceso: Cuenta ocurrencias por video y clase
# Salida: video_name\tclass_name\tcount
```

**Resultado:** Índice que muestra cuántas veces aparece cada objeto en cada video.

### 5. Procesamiento con Apache Spark 🚀

**Archivo:** `spark/functions/search_motor.scala`

Implementación más eficiente usando Spark SQL:

```scala
// Lee CSV desde HDFS
val df = spark.read.option("header", "true").csv(path)

// Crea índice invertido agrupando y contando
val invertedIndex = df
  .groupBy($"video_id", $"class_name")
  .count()
  .orderBy($"count".desc)
```

**Ventajas sobre MapReduce:**
- Procesamiento en memoria
- Mayor velocidad
- API más simple
- Optimizaciones automáticas

### 6. Consultas y Ranking con Hive 📊

**Archivo:** `hive/system/busqueda_page_ranking.HQL`

Sistema de ranking basado en popularidad:

```sql
-- Calcula page ranking basado en accesos
SELECT 
    mg.video_name,
    COUNT(ls.video_name) AS page_ranking
FROM metadata_general mg
LEFT JOIN logs_system ls ON mg.video_name = ls.video_name  
WHERE mg.class_name LIKE '%${search_class}%'
GROUP BY mg.video_name
ORDER BY page_ranking DESC;
```

**Características:**
- Utiliza variables dinámicas (`${search_class}`)
- Implementa LEFT JOIN para incluir todos los videos
- Ordena por popularidad (más accesos = mayor ranking)
- Guarda resultados en HDFS para el cliente

## 🔍 Motor de Búsqueda - Funcionalidades

### Búsqueda por Objeto
```bash
# Buscar videos que contengan "person"
hive -hivevar search_class=person -f busqueda_page_ranking.HQL
```

### Índice Invertido
```
Objeto: "car"
├── video1.mp4: 15 apariciones
├── video3.mp4: 8 apariciones  
└── video7.mp4: 3 apariciones
```

### Page Ranking
Los videos se ordenan por:
1. **Número de detecciones** del objeto buscado
2. **Frecuencia de acceso** en los logs
3. **Relevancia temporal** (más recientes primero)

## 🛠️ Configuración e Instalación

### Prerrequisitos
```bash
# Hadoop ecosystem
- Hadoop 3.x
- Hive 3.x  
- Spark 3.x

# Python dependencies
- ultralytics (YOLO)
- opencv-python
- pandas
- numpy

# Scala dependencies  
- Scala 2.12+
- SBT
```

### Instalación
```bash
# 1. Clonar repositorio
git clone <repo-url>
cd BASIC-SEARCH-BAR-IN-CLUSTER

# 2. Instalar dependencias Python
pip install -r requirements.txt

# 3. Descargar modelo YOLO
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# 4. Configurar Hadoop (verificar conectividad)
hadoop fs -ls /

# 5. Crear directorios base
mkdir -p videos metadata
```

## 🚀 Uso del Sistema

### Paso 1: Procesar Videos
```bash
# Colocar videos en ./videos/
cp /path/to/videos/*.mp4 ./videos/

# Ejecutar procesamiento
python Src/process_video.py
```

### Paso 2: Subir a HDFS
```bash
python Cluster/upload_to_hdfs.py
```

### Paso 3: Crear Índice (Opción A - MapReduce)
```bash
# Ejecutar MapReduce job
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files Index/map.py,Index/reduce.py \
  -mapper map.py \
  -reducer reduce.py \
  -input /oursystem/input/metadata \
  -output /oursystem/output/mapreduce_index
```

### Paso 3: Crear Índice (Opción B - Spark)
```bash
# Compilar Scala
sbt package

# Ejecutar Spark job
spark-submit --class InvertedIndex target/scala-2.12/invertedindex_2.12-1.0.jar
```

### Paso 4: Realizar Búsquedas
```bash
# Buscar objetos específicos
hive -hivevar search_class=person -f hive/system/busqueda_page_ranking.HQL

# Ver resultados
hadoop fs -cat /oursystem/output/page_rank/person/*
```

## 📊 Estructura de Datos

### Metadata JSON (Intermedio)
```json
{
  "video1|frame_100.jpg": [
    {
      "class_id": 0,
      "class_name": "person", 
      "confidence": 0.92,
      "bbox": [120, 150, 280, 420]
    }
  ]
}
```

### Tabla Hive (Final)
```
video_name    | class_name | count | timestamp
video1.mp4    | person     | 15    | 2024-01-15
video1.mp4    | car        | 3     | 2024-01-15  
video2.mp4    | person     | 8     | 2024-01-15
```

### Resultado de Búsqueda
```
video_name    | page_ranking
video1.mp4    | 25
video3.mp4    | 18
video2.mp4    | 12
```

## 🔧 Optimizaciones Implementadas

### Rendimiento
- **Frame skipping:** Procesa 1 de cada 100 frames
- **Batch processing:** Agrupa operaciones HDFS
- **Spark caching:** Mantiene datos frecuentes en memoria
- **Particionado:** Divide datos por fecha/categoría

### Escalabilidad  
- **Hadoop distributed:** Procesamiento distribuido automático
- **HDFS replication:** Redundancia de datos (factor 3)
- **Dynamic partitioning:** Hive maneja particiones automáticamente
- **Resource management:** YARN gestiona recursos del cluster

### Precisión IA
- **YOLO v8:** Modelo state-of-the-art para detección
- **Confidence filtering:** Solo detecciones > 0.5 confianza  
- **Multi-scale detection:** Detecta objetos de varios tamaños
- **80+ classes:** COCO dataset completo

## 📈 Monitoreo y Logs

### Logs del Sistema
```bash
# Ver logs de procesamiento
hadoop fs -cat /oursystem/input/logs/processing_*.log

# Monitorear jobs activos  
yarn application -list

# Ver métricas HDFS
hdfs dfsadmin -report
```

### Métricas Clave
- **Throughput:** Videos procesados por hora
- **Accuracy:** Precisión de detecciones YOLO
- **Storage:** Uso de espacio HDFS
- **Query time:** Tiempo de respuesta de búsquedas

## 🔍 Casos de Uso

### 1. Búsqueda de Contenido Multimedia
```bash
# Encontrar videos con personas
hive -hivevar search_class=person -f busqueda_page_ranking.HQL

# Buscar vehículos  
hive -hivevar search_class=car -f busqueda_page_ranking.HQL
```

### 2. Análisis de Contenido
```bash
# Videos más populares por categoría
# Tendencias de objetos detectados  
# Estadísticas de uso del sistema
```

### 3. Recomendaciones
```bash
# Videos similares basados en objetos detectados
# Contenido relacionado por contexto visual
```

## 🚨 Troubleshooting

### Errores Comunes

#### HDFS Connection Error
```bash
# Verificar conectividad
hadoop fs -ls /

# Reiniciar servicios si es necesario  
stop-dfs.sh && start-dfs.sh
```

#### YOLO Model Issues
```bash
# Re-descargar modelo
rm ~/.cache/torch/hub/ultralytics_yolov8_*
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

#### Hive Query Errors
```bash
# Verificar tabla existe
hive -e "SHOW TABLES;"

# Revisar permisos HDFS
hadoop fs -chmod -R 755 /oursystem/
```

## 🔄 Roadmap Futuro

### Mejoras Planeadas
- [ ] **Real-time processing:** Streaming con Kafka + Spark
- [ ] **Web interface:** Dashboard para búsquedas
- [ ] **Advanced ML:** Modelos custom entrenados  
- [ ] **Auto-scaling:** Cluster dinámico basado en carga
- [ ] **Multi-modal search:** Búsqueda por texto + imagen
- [ ] **Performance tuning:** Optimizaciones avanzadas

### Integraciones
- [ ] **Elasticsearch:** Búsquedas full-text híbridas
- [ ] **Docker containers:** Deployment simplificado
- [ ] **Kubernetes:** Orquestación cloud-native
- [ ] **MLflow:** Gestión de modelos ML

## 👥 Contribución

### Cómo Contribuir
1. Fork del repositorio
2. Crear branch feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push branch (`git push origin feature/nueva-funcionalidad`)  
5. Crear Pull Request

### Coding Standards
- **Python:** PEP 8
- **Scala:** Scala Style Guide
- **SQL:** Uppercase keywords
- **Documentación:** Español para README, inglés para código

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

## 🙏 Reconocimientos

- **Ultralytics YOLO:** Framework de detección de objetos
- **Apache Hadoop:** Sistema de almacenamiento distribuido  
- **Apache Spark:** Motor de procesamiento rápido
- **Apache Hive:** Data warehouse sobre Hadoop

---

**Desarrollado con ❤️ para el procesamiento distribuido de contenido multimedia**

```
📊 Estadísticas del Proyecto:
- Lenguajes: Python, Scala, HQL, Shell
- Frameworks: Hadoop, Spark, Hive, YOLO
- Arquitectura: Distribuida, Big Data, ML Pipeline
- Objetivo: Motor de búsqueda de contenido visual
```
