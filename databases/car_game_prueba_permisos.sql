USE car_game_db;

-- 1) ¿Las 5 tablas existen?
SHOW TABLES;
-- Debe listar: auditoria_seguridad, estadisticas_usuario,
--              partidas, registro_intentos_login, usuarios

-- 2) ¿Los 8 SPs existen?
SELECT ROUTINE_NAME FROM information_schema.ROUTINES
 WHERE ROUTINE_SCHEMA = 'car_game_db' AND ROUTINE_TYPE = 'PROCEDURE';
-- Debe listar: sp_auditar_evento, sp_guardar_puntuacion, sp_iniciar_login,
--              sp_obtener_estadisticas_usuario, sp_obtener_historial_partidas,
--              sp_obtener_ranking_global, sp_registrar_resultado_login,
--              sp_registrar_usuario

-- 3) ¿Los GRANT están bien?
SHOW GRANTS FOR 'app_jugador'@'localhost';
-- Solo debe aparecer EXECUTE sobre car_game_db.*