import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object InvertedIndex {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("InvertedIndex")
      .getOrCreate()

    import spark.implicits._

    // Ruta del archivo en HDFS o local
    val path = "hdfs:///oursystem/input/metadata_table/*.txt"

    // Leer los archivos CSV ignorando la primera fila (cabecera)
    val df = spark.read
      .option("header", "true") // salta cabecera
      .option("inferSchema", "true")
      .csv(path)
      .select("video_id", "class_name")
      .na.drop() // por si hay nulos

    // Contar ocurrencias por video y objeto
    val invertedIndex = df
      .groupBy($"video_id", $"class_name")
      .count()
      .orderBy($"count".desc)

    // Mostrar resultados
    invertedIndex.show(50, truncate = false)

    // Puedes guardar si deseas:
    invertedIndex.write.csv("hdfs:///oursystem/output/spark_inverted_index")

    spark.stop()
  }
}
