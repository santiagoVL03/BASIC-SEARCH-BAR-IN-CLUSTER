CREATE EXTERNAL TABLE metadata_general (
  video_name STRING,
  frame STRING,
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
LOCATION '/oursystem/input/metadata_table/metadata_salida_general.txt'
TBLPROPERTIES ("skip.header.line.count"="1");
