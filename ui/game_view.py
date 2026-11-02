# ui/game_view.py
import tkinter as tk
from tkinter import messagebox
from logic.game_engine import GameEngine
from data.user_repo import UserRepository
import winsound
import os


class GameView(tk.Frame):
    def __init__(self, master, id_usuario):
        super().__init__(master, bg=master.ui_manager.COLOR_BG)
        self.master = master
        self.ui = master.ui_manager
        self.id_usuario = id_usuario
        self.repo = UserRepository()

        # Control de estado
        self.animando = True
        self.ya_guardado = False  # Evita guardar múltiples veces
        self.vidas_anteriores = 3  # Para detectar cuando choca

        self.engine = GameEngine(900, 600)

        self._configurar_controles()
        self._iniciar_partida_visual()

    def _iniciar_partida_visual(self):
        """Prepara el canvas desde cero (se usa al iniciar y al reiniciar)"""
        # Si ya existía un canvas, lo destruimos para no crear capas
        if hasattr(self, 'canvas'):
            self.canvas.destroy()

        self.canvas = tk.Canvas(self, width=900, height=600, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Dibujar pista
        self.canvas.create_line(self.engine.pista_x_inicio, 0, self.engine.pista_x_inicio, 600, fill="white", width=4)
        self.canvas.create_line(self.engine.pista_x_fin, 0, self.engine.pista_x_fin, 600, fill="white", width=4)

        # Dashboard
        self.txt_puntos = self.canvas.create_text(20, 20, text="Puntos: 0", fill="white", font=("Segoe UI", 18, "bold"),
                                                  anchor="nw")
        self.txt_vidas = self.canvas.create_text(450, 20, text="Vidas: ❤️❤️❤️", fill=self.ui.COLOR_ACCENT,
                                                 font=("Segoe UI", 18, "bold"), anchor="n")
        self.txt_velocidad = self.canvas.create_text(880, 20, text="Velocidad: 5.0", fill="white",
                                                     font=("Segoe UI", 18, "bold"), anchor="ne")

        self.lineas_pista = []
        x_centro = self.engine.pista_x_inicio + (self.engine.pista_ancho // 2)
        for y in range(-20, 600, 80):
            linea = self.canvas.create_line(x_centro - 5, y, x_centro - 5, y + 40, fill="white", width=6, dash=(20, 20))
            self.lineas_pista.append(linea)

        # Cargar Assets y Carros
        self.img_jugador = self.ui.cargar_imagen("car/player.png", size=(50, 90))
        self.img_ia1 = self.ui.cargar_imagen("car/ia1.png", size=(50, 90))
        self.img_ia2 = self.ui.cargar_imagen("car/ia2.png", size=(50, 90))
        self.img_ia3 = self.ui.cargar_imagen("car/ia3.png", size=(50, 90))
        self.imagenes_ia = [self.img_ia1, self.img_ia2, self.img_ia3]

        self.obj_jugador = self.canvas.create_image(self.engine.carro_jugador.x, self.engine.carro_jugador.y,
                                                    image=self.img_jugador, anchor="nw")

        self.objs_ia = []
        for i, ia in enumerate(self.engine.carros_ia):
            img = self.imagenes_ia[i]
            if img:
                obj = self.canvas.create_image(ia.x, ia.y, image=img, anchor="nw")
            else:
                obj = self.canvas.create_rectangle(ia.x, ia.y, ia.x + ia.ancho, ia.y + ia.alto, fill="blue")
            self.objs_ia.append(obj)

        # Iniciar el bucle
        self.animando = True
        self.game_loop()

    def _configurar_controles(self):
        self.focus_set()
        self.bind("<Left>", lambda e: self.engine.mover_jugador(-20, 0))
        self.bind("<Right>", lambda e: self.engine.mover_jugador(20, 0))
        self.bind("<Up>", lambda e: self.engine.mover_jugador(0, -20))
        self.bind("<Down>", lambda e: self.engine.mover_jugador(0, 20))

    def game_loop(self):
        if not self.animando:
            return

        if self.engine.juego_activo:
            self.engine.mover_ia()

            # Actualizar posiciones
            self.canvas.coords(self.obj_jugador, self.engine.carro_jugador.x, self.engine.carro_jugador.y)
            for i, ia in enumerate(self.engine.carros_ia):
                self.canvas.coords(self.objs_ia[i], ia.x, ia.y)

            # Animar pista
            for linea in self.lineas_pista:
                self.canvas.move(linea, 0, self.engine.velocidad_base)
                coords = self.canvas.coords(linea)
                if coords[1] > 600:
                    self.canvas.move(linea, 0, -680)

            # Actualizar Dashboard
            self.canvas.itemconfig(self.txt_puntos, text=f"Puntos: {self.engine.puntos}")
            self.canvas.itemconfig(self.txt_velocidad, text=f"Velocidad: {self.engine.velocidad_base:.1f}")
            corazones = "❤️" * self.engine.vidas + "🖤" * (3 - self.engine.vidas)
            self.canvas.itemconfig(self.txt_vidas, text=f"Vidas: {corazones}")

            # EFECTOS: Detectar si perdió una vida
            if self.engine.vidas < self.vidas_anteriores:
                self.vidas_anteriores = self.engine.vidas
                self._efecto_choque()

            self.after(20, self.game_loop)
        else:
            self._mostrar_game_over()

    def _efecto_choque(self):
        """Vibración y Sonido al chocar"""
        # 1. Sonido (winsound solo funciona en Windows)
        ruta_sonido = os.path.join(os.getcwd(), "assets", "crash.wav")
        if os.path.exists(ruta_sonido):
            winsound.PlaySound(ruta_sonido, winsound.SND_ASYNC | winsound.SND_FILENAME)

        # 2. Vibración (Mover la ventana rápidamente)
        try:
            pos_actual = self.master.geometry().split('+')
            x_base, y_base = int(pos_actual[1]), int(pos_actual[2])

            for i in range(4):
                # Mueve la ventana un poco
                offset = 10 if i % 2 == 0 else -10
                self.master.geometry(f"+{x_base + offset}+{y_base + offset}")
                self.master.update()
                self.master.after(30)  # Pausa milimétrica

            # Devolver a la posición original
            self.master.geometry(f"+{x_base}+{y_base}")
        except Exception:
            pass

    def _mostrar_game_over(self):
        self.animando = False

        # Validación para que no guarde 2 veces
        if not self.ya_guardado:
            self.ya_guardado = True
            self._guardar_puntuacion_bd()

        # Panel visual
        self.canvas.create_rectangle(200, 150, 700, 450, fill=self.ui.COLOR_PANEL, outline=self.ui.COLOR_ACCENT,
                                     width=3)
        self.canvas.create_text(450, 200, text="💥 ¡SIN VIDAS! 💥", fill=self.ui.COLOR_DANGER,
                                font=("Segoe UI", 30, "bold"))
        self.canvas.create_text(450, 260, text=f"Puntaje Final: {self.engine.puntos}", fill="white",
                                font=("Segoe UI", 20, "bold"))

        # Botones (los guardamos en variables para poder destruirlos al reiniciar)
        self.btn_reintentar = tk.Button(self, text="VOLVER A JUGAR", command=self._reiniciar_partida,
                                        bg=self.ui.COLOR_ACCENT, fg=self.ui.COLOR_BG, font=("Segoe UI", 12, "bold"))
        self.btn_reintentar.place(relx=0.4, rely=0.65, anchor="center", width=150)

        self.btn_menu = tk.Button(self, text="MENÚ PRINCIPAL", command=lambda: self.master.cambiar_vista("login"),
                                  bg=self.ui.COLOR_DANGER, fg="white", font=("Segoe UI", 12, "bold"))
        self.btn_menu.place(relx=0.6, rely=0.65, anchor="center", width=150)

    def _reiniciar_partida(self):
        # 1. Destruir botones del Game Over
        if hasattr(self, 'btn_reintentar'):
            self.btn_reintentar.destroy()
            self.btn_menu.destroy()

        # 2. Reiniciar motor lógico
        self.engine.reiniciar_juego()

        # 3. Resetear variables de control
        self.ya_guardado = False
        self.vidas_anteriores = 3

        # 4. Reconstruir el Canvas (esto destruye el viejo y crea uno limpio)
        self._iniciar_partida_visual()

    def _guardar_puntuacion_bd(self):
        try:
            duracion = self.engine.obtener_duracion()
            nivel_vel = int(self.engine.velocidad_base)
            rebasados = self.engine.puntos // 50

            query = "CALL sp_guardar_puntuacion(%s, %s, %s, %s, %s, %s, @res, @msg, @record)"
            with self.repo.db._pool.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query,
                                   (self.id_usuario, self.engine.puntos, nivel_vel, duracion, rebasados, "127.0.0.1"))
                    conn.commit()
                    cursor.execute("SELECT @res as resultado, @msg as mensaje, @record as es_record")
                    res = cursor.fetchone()
                    if res['resultado'] == 1:
                        print(f"✅ Score guardado: {res['mensaje']}")
                    else:
                        print(f"⚠️ Score no guardado: {res['mensaje']}")
        except Exception as e:
            print(f"❌ Error al guardar score: {e}")

    def destroy(self):
        self.animando = False
        super().destroy()