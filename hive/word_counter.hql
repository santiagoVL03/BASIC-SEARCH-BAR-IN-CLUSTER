SELECT archivo_json, class_name, COUNT(*) AS count
FROM metadata_general
GROUP BY archivo_json, class_name
ORDER BY archivo_json, count DESC;