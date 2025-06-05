CREATE EXTERNAL TABLE metadata_general (
  archivo_json STRING,
  imagen STRING,
  class_id INT,
  class_name STRING,
  confidence FLOAT,
  x1 FLOAT,
  y1 FLOAT,
  x2 FLOAT,
  y2 FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/table/'
TBLPROPERTIES ("skip.header.line.count"="1");
