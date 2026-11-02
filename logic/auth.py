import bcrypt
import logging
from data.user_repo import UserRepository

class AuthManager:
    """Valida contraseñas, maneja bcrypt y decide si el usuario entra"""

    def __init__(self):
        self.repo = UserRepository()


    def registrar_usuario(self, username, email, password):
        if len(password) < 8:
            return False, "La contraseña debe de tener al menos 8 caracteres"

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        salt_str = salt.decode("utf-8")

        res = self.repo.registrar_usuario(username, email, password_hash, salt_str, "127.0.0.1")

        if res["resultado"] == 1:
            return True, res["mensaje"]
        return False, res["mensaje"]

    def iniciar_sesion(self, username, password):
        res = self.repo.iniciar_login(username)

        if res['resultado'] == 0:
            hash_bd = res['pass_hash'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hash_bd):
                self.repo.registrar_resultado_login(res['id_usuario'], True, "127.0.0.1", "Tkinter")
                # Retornamos un diccionario con los datos del usuario
                datos_usuario = {
                    "id": res['id_usuario'],
                    "rol": res['rol']
                }
                return True, datos_usuario
            else:
                self.repo.registrar_resultado_login(res['id_usuario'], False, "127.0.0.1", "Tkinter")
                return False, "Contraseña incorrecta."

        elif res['resultado'] == -3:
            return False, f"Cuenta bloqueada. {res['mensaje']}"
        else:
            return False, "Usuario o contraseña inválidos."

