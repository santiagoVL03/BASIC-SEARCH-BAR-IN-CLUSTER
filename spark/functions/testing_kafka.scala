import org.apache.spark.sql.functions._

val df = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")
  .option("subscribe", "video-events")
  .load()

val mensajes = df.selectExpr("CAST(value AS STRING)")

val query = mensajes.writeStream
  .outputMode("append")
  .format("console")
  .start()
