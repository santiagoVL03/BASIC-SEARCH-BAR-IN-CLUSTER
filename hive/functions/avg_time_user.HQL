SELECT 
  nombre_usuario,
  url,
  ROUND(AVG(tiempo), 2) AS promedio_usuario
FROM 
  user_web_time
GROUP BY 
  nombre_usuario, url;
