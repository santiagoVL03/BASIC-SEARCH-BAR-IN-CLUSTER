CREATE EXTERNAL TABLE video_data (
  video_name STRING
)
ROW FORMAT DELIMITED
STORED AS TEXTFILE
LOCATION '/oursystem/input/metadata_video_table/'
TBLPROPERTIES ("skip.header.line.count"="1");
-- This table is used to store the list of video names for further processing.
-- It is expected to be populated with video names from the metadata table.
-- THIS TABLE IS DEPRECATED AND WILL BE REMOVED IN FUTURE VERSIONS.