SELECT user_name, COUNT(*) AS total_consultas
FROM logs_excite
GROUP BY user_name;
