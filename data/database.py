from mysql.connector import pooling, Error
from data.config import Config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DatabaseManager:
    """
    Gestor de Base de Datos centralizado.
    Utiliza un Pool de conexiones para su eficiencia (ISO 25010).
    Solo permite ejecutar Stored Procedures (defensa en profundidad).
    """
    _instancia = None
    _pool = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(DatabaseManager, cls).__new__(cls)
            cls._instancia._inicializar_pool()
        return cls._instancia

    def _inicializar_pool(self):
        cfg = Config()
        try:
            self._pool = pooling.MySQLConnectionPool(
                pool_name="car_game_pool",
                pool_size=5,
                pool_reset_session=True,
                host=cfg.DB_HOST,
                port=cfg.DB_PORT,
                user=cfg.DB_USER,
                password=cfg.DB_PASSWORD,
                database=cfg.DB_NAME,
                ssl_disabled=False,
                autocommit=False
            )
            logging.info("✅ Pool de conexiones a la base de datos inicializado correctamente.")
        except Error as e:
            logging.error(f"❌ Error al crear el pool de conexiones: {e}")
            raise e

    def ejecutar_sp(self, nombre_sp: str, args: tuple = (), fetch_all: bool = False):
        """
        Método centralizado para llamar a los Procedimientos Almacenados.
        Retorna los datos (si los hay) o None.
        """
        conexion = None
        cursor = None

        try:
            conexion = self._pool.get_connection()
            cursor = conexion.cursor(dictionary=True)

            # Construimos la llamada al SP con parámetros (%s)
            query = f"CALL {nombre_sp}({','.join(['%s'] * len(args))})"
            cursor.execute(query, args)

            resultados = []
            for resultado in cursor.stored_results():
                resultados.append(resultado.fetchall())

            # CORRECCIÓN ANTI-"Unread result": Consumir cualquier paquete pendiente
            # Esto vacía el buffer del cursor antes del commit.
            try:
                cursor.fetchall()
            except Error:
                pass  # Si no hay más resultados, ignoramos el error silenciosamente

            conexion.commit()

            # Si fetch_all es True, devuelve la lista completa. Si no, el primer resultado.
            return resultados if fetch_all else resultados[0] if resultados else None

        except Error as e:
            if conexion:
                conexion.rollback()
            logging.error(f"❌ Error BD en {nombre_sp}: {e}")
            raise Exception("Error interno de la base de datos. Intente más tarde.")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()