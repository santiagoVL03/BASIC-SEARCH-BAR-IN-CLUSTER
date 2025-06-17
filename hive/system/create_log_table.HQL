CREATE EXTERNAL TABLE IF NOT EXISTS logs_system (
  user_name STRING,
  time_date STRING,
  video_name STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/oursystem/input/logs/'
TBLPROPERTIES ("skip.header.line.count"="0");
