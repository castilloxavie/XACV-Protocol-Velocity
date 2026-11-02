from data.database import DatabaseManager
import logging

class UserRepository:
    """
    Capa de Datos: Se encarga exclusivamente de hablar con los Stored Procedures.
    No contiene lógica de negocio ni UI.
    """
    def __init__(self):
        self.db = DatabaseManager()

    def registrar_usuario(self, username, email, password_hash, salt, ip):
        try:
            query = "CALL sp_registrar_usuario(%s, %s, %s, %s, %s, @res, @msg)"
            with self.db._pool.get_connection() as conn:
                # CORREGIDO AQUÍ: dictionary=True para que devuelva un diccionario
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (username, email, password_hash, salt, ip))
                    conn.commit()
                    # Este SELECT solo lee las variables de sesión llenadas por el SP
                    cursor.execute("SELECT @res as resultado, @msg as mensaje")
                    return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error en BD (registrar_usuario): {e}")
            return {"resultado": -99, "mensaje": "Error de conexión"}

    def iniciar_login(self, username):
        try:
            # Ahora pedimos el @rol al final
            query = "CALL sp_iniciar_login(%s, @res, @msg, @id_user, @hash, @salt, @bloqueado, @rol)"
            with self.db._pool.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (username,))
                    cursor.execute("""
                        SELECT @res as resultado, @msg as mensaje, 
                               @id_user as id_usuario, @hash as pass_hash, 
                               @salt as salt, @bloqueado as bloqueado,
                               @rol as rol
                    """)
                    return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error en BD (iniciar_login): {e}")
            return {"resultado": -99, "mensaje": "Error interno"}

    def registrar_resultado_login(self, id_usuario, exito, ip, user_agent):
        try:
            query = "CALL sp_registrar_resultado_login(%s, %s, %s, %s, @res, @msg)"
            with self.db._pool.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (id_usuario, exito, ip, user_agent))
                    conn.commit()
        except Exception as e:
            logging.error(f"Error en BD (registrar_resultado_login): {e}")