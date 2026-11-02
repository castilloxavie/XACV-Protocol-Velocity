# logic/game_engine.py
import random
import time


class Car:
    def __init__(self, x, y, ancho, alto, velocidad):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad


class GameEngine:
    def __init__(self, ancho_canvas, alto_canvas):
        self.ancho_canvas = ancho_canvas
        self.alto_canvas = alto_canvas

        self.pista_ancho = 400
        self.pista_x_inicio = (ancho_canvas - self.pista_ancho) // 2
        self.pista_x_fin = self.pista_x_inicio + self.pista_ancho

        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.velocidad_base = 5.0
        self.puntos = 0
        self.vidas = 3  # <--- NUEVO: Iniciamos con 3 vidas
        self.tiempo_inicio = time.time()
        self.juego_activo = True

        self.carro_jugador = Car(x=self.ancho_canvas // 2 - 25, y=self.alto_canvas - 150, ancho=50, alto=90,
                                 velocidad=15)

        self.carros_ia = [
            Car(x=random.randint(self.pista_x_inicio + 20, self.pista_x_fin - 70), y=-100, ancho=50, alto=90,
                velocidad=self.velocidad_base),
            Car(x=random.randint(self.pista_x_inicio + 20, self.pista_x_fin - 70), y=-400, ancho=50, alto=90,
                velocidad=self.velocidad_base),
            Car(x=random.randint(self.pista_x_inicio + 20, self.pista_x_fin - 70), y=-700, ancho=50, alto=90,
                velocidad=self.velocidad_base)
        ]

    def mover_jugador(self, dx, dy):
        if not self.juego_activo: return
        nuevo_x = self.carro_jugador.x + dx
        nuevo_y = self.carro_jugador.y + dy

        if self.pista_x_inicio + 10 <= nuevo_x <= self.pista_x_fin - self.carro_jugador.ancho - 10:
            self.carro_jugador.x = nuevo_x
        if 0 <= nuevo_y <= self.alto_canvas - self.carro_jugador.alto:
            self.carro_jugador.y = nuevo_y

    def mover_ia(self):
        if not self.juego_activo: return

        tiempo_transcurrido = time.time() - self.tiempo_inicio
        self.velocidad_base = 5.0 + (tiempo_transcurrido * 0.2)

        # Los puntos solo se suman si el juego sigue activo
        self.puntos += 1

        for ia in self.carros_ia:
            ia.y += self.velocidad_base

            if ia.y > self.alto_canvas:
                ia.y = random.randint(-400, -100)
                ia.x = random.randint(self.pista_x_inicio + 20, self.pista_x_fin - ia.ancho - 20)
                self.puntos += 50  # Puntos extra por esquivar

            # DETECCIÓN DE COLISIONES
            if self._hay_colision(self.carro_jugador, ia):
                self.vidas -= 1

                if self.vidas <= 0:
                    self.juego_activo = False  # Game Over definitivo
                else:
                    # Si aún tiene vidas, reposicionamos al jugador y al rival
                    self.carro_jugador.y = self.alto_canvas - 150  # Volver al inicio
                    ia.y = -400  # Mandar el rival muy arriba para que no vuelva a chocar de inmediato
                    ia.x = random.randint(self.pista_x_inicio + 20, self.pista_x_fin - ia.ancho - 20)

    def _hay_colision(self, c1, c2):
        return (c1.x < c2.x + c2.ancho and
                c1.x + c1.ancho > c2.x and
                c1.y < c2.y + c2.alto and
                c1.y + c1.alto > c2.y)

    def obtener_duracion(self):
        return max(1, int(time.time() - self.tiempo_inicio))