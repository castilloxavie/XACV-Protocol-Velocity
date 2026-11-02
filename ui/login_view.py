import tkinter as tk
from tkinter import messagebox
from logic.auth import AuthManager


class LoginView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=master.ui_manager.COLOR_BG)
        self.master = master
        self.ui = master.ui_manager
        self.auth = AuthManager()
        self._construir_ui()

    def _construir_ui(self):
        frame = tk.Frame(self, bg=self.ui.COLOR_PANEL, padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="🏎️ INICIAR SESIÓN", font=("Segoe UI", 16, "bold"),
                 bg=self.ui.COLOR_PANEL, fg=self.ui.COLOR_ACCENT).pack(pady=(0, 20))

        tk.Label(frame, text="Usuario:", bg=self.ui.COLOR_PANEL, fg=self.ui.COLOR_TEXT).pack(anchor="w")
        self.entry_user = tk.Entry(frame, bg=self.ui.COLOR_BG, fg=self.ui.COLOR_TEXT,
                                   insertbackground=self.ui.COLOR_TEXT, relief="flat")
        self.entry_user.pack(fill="x", pady=(0, 10), ipady=5)

        tk.Label(frame, text="Contraseña:", bg=self.ui.COLOR_PANEL, fg=self.ui.COLOR_TEXT).pack(anchor="w")
        self.entry_pass = tk.Entry(frame, show="*", bg=self.ui.COLOR_BG, fg=self.ui.COLOR_TEXT,
                                   insertbackground=self.ui.COLOR_TEXT, relief="flat")
        self.entry_pass.pack(fill="x", pady=(0, 20), ipady=5)

        tk.Button(frame, text="JUGAR", command=self._login, bg=self.ui.COLOR_ACCENT, fg=self.ui.COLOR_BG,
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(fill="x", ipady=5)

        # Botón para ir a Registro
        tk.Button(frame, text="¿No tienes cuenta? Regístrate", command=self._ir_a_registro, bg=self.ui.COLOR_PANEL,
                  fg=self.ui.COLOR_ACCENT, font=("Segoe UI", 9), relief="flat", borderwidth=0).pack(pady=(10, 0))

    def _login(self):
        u, p = self.entry_user.get().strip(), self.entry_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Atención", "Llena todos los campos")
            return

        exito, datos = self.auth.iniciar_sesion(u, p)
        if exito:
            # Destruimos la vista actual y montamos el juego pasándole el ID
            self.master.vista_actual.destroy()
            from ui.game_view import GameView
            self.master.vista_actual = GameView(self.master, id_usuario=datos['id'])
            self.master.vista_actual.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Error", datos)

    def _ir_a_registro(self):
        self.master.cambiar_vista("registro")