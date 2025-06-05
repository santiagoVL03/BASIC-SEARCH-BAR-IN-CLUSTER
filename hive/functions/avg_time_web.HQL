SELECT 
  uwt.url,
  ROUND(AVG(uwt.tiempo), 2) AS promedio_global,
  wr.rank,
  wr.puntaje
FROM 
  user_web_time uwt
JOIN 
  web_rank wr
ON 
  uwt.url = wr.url
GROUP BY 
  uwt.url, wr.rank, wr.puntaje
ORDER BY 
  wr.rank ASC;
