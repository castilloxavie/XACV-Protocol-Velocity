# main.py
import tkinter as tk
import atexit
from ui.ui_manager import UIManager
from data.database import DatabaseManager
from ui.login_view import LoginView
from ui.register_view import RegisterView
from ui.game_view import GameView

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XACV Protocol Velocity")
        self.geometry("900x600")
        self.resizable(False, False)

        # Inicializar Capas
        self.ui_manager = UIManager()
        self.db = DatabaseManager()

        self.configure(bg=self.ui_manager.COLOR_BG)
        self.ui_manager.configurar_estilos_ttk(self)

        # Diccionario de vistas
        self.vistas = {
            "login": LoginView,
            "registro": RegisterView,
            "juego": GameView, # Lo dejamos por si lo necesitas, aunque LoginView lo llama directo
        }
        self.vista_actual = None

        # Arrancar en Login
        self.cambiar_vista("login")

        # --- NUEVO: Cierre seguro de la ventana ---
        # Si el usuario da clic en la "X" de arriba a la derecha, se llama a este método
        self.protocol("WM_DELETE_WINDOW", self._cerrar_aplicacion)

    def cambiar_vista(self, nombre_vista):
        """Destruye la vista actual y monta la nueva (Navegación)"""
        if self.vista_actual:
            self.vista_actual.destroy()

        clase_vista = self.vistas[nombre_vista]
        self.vista_actual = clase_vista(self)
        self.vista_actual.pack(fill="both", expand=True)

    def _cerrar_aplicacion(self):
        """Asegura que Tkinter cierre y libere recursos visuales"""
        print("Cerrando aplicación de forma segura...")
        self.destroy()
        self.quit()

# --- NUEVO: Liberar el pool de conexiones a la base de datos ---
def cerrar_recursos_globales():
    """Se ejecuta automáticamente al finalizar Python"""
    try:
        db = DatabaseManager()
        if db._pool:
            # Forzar la eliminación del pool libera las conexiones en MySQL
            del db._pool
            print("✅ Pool de conexiones de BD liberado correctamente.")
    except Exception as e:
        print(f"Nota al cerrar: {e}")

# Registra la función para que se ejecute al cerrar el programa
atexit.register(cerrar_recursos_globales)

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()