CREATE EXTERNAL TABLE user_web_time (
  nombre_usuario STRING,
  url STRING,
  tiempo INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/log_web/'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE web_rank (
  url STRING,
  rank INT,
  puntaje INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/web_rank/'
TBLPROPERTIES ("skip.header.line.count"="1");
