-- consulta.hql
-- This query retrieves the video names and their corresponding page ranking based on the number of times they appear in the logs_system table.
-- The search_class variable is used to filter the results based on the class name in the metadata_general table.
-- The results are ordered by page ranking in descending order, showing the most popular videos first.
-- The query uses a LEFT JOIN to ensure that all videos from the metadata_general table are included, even if they have no corresponding entries in the logs_system table.
-- The results will show the video names along with their page ranking, which is the count of how many times they were accessed in the logs_system table.

INSERT OVERWRITE DIRECTORY '/oursystem/output/page_rank/${search_class}'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE

SELECT 
    mg.video_name,
    COUNT(ls.video_name) AS page_ranking
FROM 
    metadata_general mg
LEFT JOIN 
    logs_system ls ON mg.video_name = ls.video_name
WHERE 
    mg.class_name LIKE '%${search_class}%'
GROUP BY 
    mg.video_name
ORDER BY 
    page_ranking DESC;
