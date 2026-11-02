import tkinter as tk
from tkinter import messagebox
from logic.auth import AuthManager


class RegisterView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=master.ui_manager.COLOR_BG)
        self.master = master
        self.ui = master.ui_manager
        self.auth = AuthManager()
        self._construir_ui()

    def _construir_ui(self):
        frame = tk.Frame(self, bg=self.ui.COLOR_PANEL, padx=30, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="📝 REGISTRO", font=("Segoe UI", 16, "bold"), bg=self.ui.COLOR_PANEL,
                 fg=self.ui.COLOR_ACCENT).pack(pady=(0, 15))

        tk.Label(frame, text="Usuario:", bg=self.ui.COLOR_PANEL, fg=self.ui.COLOR_TEXT).pack(anchor="w")
        self.entry_user = tk.Entry(frame, bg=self.ui.COLOR_BG, fg=self.ui.COLOR_TEXT, relief="flat")
        self.entry_user.pack(fill="x", pady=(0, 5), ipady=5)

        tk.Label(frame, text="Email:", bg=self.ui.COLOR_PANEL, fg=self.ui.COLOR_TEXT).pack(anchor="w")
        self.entry_email = tk.Entry(frame, bg=self.ui.COLOR_BG, fg=self.ui.COLOR_TEXT, relief="flat")
        self.entry_email.pack(fill="x", pady=(0, 5), ipady=5)

        tk.Label(frame, text="Contraseña:", bg=self.ui.COLOR_PANEL, fg=self.ui.COLOR_TEXT).pack(anchor="w")
        self.entry_pass = tk.Entry(frame, show="*", bg=self.ui.COLOR_BG, fg=self.ui.COLOR_TEXT, relief="flat")
        self.entry_pass.pack(fill="x", pady=(0, 15), ipady=5)

        tk.Button(frame, text="REGISTRARSE", command=self._registrar, bg=self.ui.COLOR_ACCENT, fg=self.ui.COLOR_BG,
                  font=("Segoe UI", 12, "bold"), relief="flat").pack(fill="x", ipady=5)
        tk.Button(frame, text="Volver al Login", command=self._volver, bg=self.ui.COLOR_PANEL, fg=self.ui.COLOR_ACCENT,
                  relief="flat", borderwidth=0).pack(pady=(10, 0))

    def _registrar(self):
        u, e, p = self.entry_user.get().strip(), self.entry_email.get().strip(), self.entry_pass.get().strip()
        if not u or not e or not p:
            messagebox.showwarning("Atención", "Llena todos los campos")
            return

        exito, msj = self.auth.registrar_usuario(u, e, p)
        if exito:
            messagebox.showinfo("Éxito", "Registro exitoso. Ahora puedes iniciar sesión.")
            self._volver()
        else:
            messagebox.showerror("Error", msj)

    def _volver(self):
        self.master.cambiar_vista("login")