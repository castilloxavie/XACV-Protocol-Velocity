-- Usuario de la aplicación (SOLO EXECUTE, cero acceso a tablas directo)
CREATE USER IF NOT EXISTS 'app_jugador'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'Cambiar_Esta_Clave_2026!';

GRANT EXECUTE ON car_game_db.* TO 'app_jugador'@'localhost';
-- NO se concede SELECT/INSERT/UPDATE/DELETE → cualquier intento de SQL
-- directo (aunque burlara el SP) falla por permisos.

-- Forzar SSL/TLS para la conexión (mitiga sniffing - vector 9 del brief)
ALTER USER 'app_jugador'@'localhost' REQUIRE SSL;

FLUSH PRIVILEGES;