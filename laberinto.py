import pygame
import random
import time
from settings import ANCHO, ALTO, TAMANO_CELDA, COLORES, pantalla, sprite_jugador, sprite_meta

class Laberinto:
    def __init__(self, nivel):
        self.nivel = nivel
        self.filas = min(10 + nivel * 2, 25)
        self.columnas = min(15 + nivel * 2, 35)
        self.tamano_celda = min(TAMANO_CELDA, 
                              int(ANCHO / (self.columnas * 1.2)), 
                              int(ALTO / (self.filas * 1.2)))
        self.margen_x = (ANCHO - self.columnas * self.tamano_celda) // 2
        self.margen_y = (ALTO - self.filas * self.tamano_celda) // 2
        self.grid = [[1 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.generar_laberinto()
        self.jugador_pos = [1, 1]
        self.jugador_target = [1, 1]
        self.meta_pos = (self.filas-2, self.columnas-2)
        self.grid[self.meta_pos[0]][self.meta_pos[1]] = 2
        self.tiempo_inicio = time.time()
        self.tiempo_limite = 60 + (10 * (10 - nivel))  # Tiempo límite decreciente
        self.puntuacion = 0
        self.animacion_t = 0
        self.animacion_duracion = 0.1
        self.pulso_t = 0
        self.particulas = []  # Lista para las partículas

    def generar_laberinto(self):
        stack = [(1, 1)]
        self.grid[1][1] = 0
        
        caminos_extra = self.nivel * 2
        
        while stack or caminos_extra > 0:
            if stack:
                x, y = stack[-1]
                vecinos = []
                
                for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 < nx < self.filas-1 and 0 < ny < self.columnas-1 and self.grid[nx][ny] == 1:
                        vecinos.append((nx, ny, (x + dx//2, y + dy//2)))
                
                if vecinos:
                    nx, ny, (px, py) = random.choice(vecinos)
                    self.grid[nx][ny] = 0
                    self.grid[px][py] = 0
                    stack.append((nx, ny))
                else:
                    stack.pop()
            elif caminos_extra > 0:
                x, y = random.randint(1, self.filas-2), random.randint(1, self.columnas-2)
                if self.grid[x][y] == 1:
                    self.grid[x][y] = 0
                    caminos_extra -= 1

    def dibujar(self):
        # Fondo dinámico con gradiente
        for y in range(ALTO):
            t = y / ALTO
            color = (
                int(COLORES['fondo_base'][0] + (COLORES['fondo_fin'][0] - COLORES['fondo_base'][0]) * t),
                int(COLORES['fondo_base'][1] + (COLORES['fondo_fin'][1] - COLORES['fondo_base'][1]) * t),
                int(COLORES['fondo_base'][2] + (COLORES['fondo_fin'][2] - COLORES['fondo_base'][2]) * t)
            )
            pygame.draw.line(pantalla, color, (0, y), (ANCHO, y))
        
        # Animación de pulso para la meta
        self.pulso_t += 0.05
        t = (1 + abs((self.pulso_t % 2) - 1)) * 0.5
        color_meta = (
            int(COLORES['meta'][0] + (COLORES['meta_pulso'][0] - COLORES['meta'][0]) * t),
            int(COLORES['meta'][1] + (COLORES['meta_pulso'][1] - COLORES['meta'][1]) * t),
            int(COLORES['meta'][2] + (COLORES['meta_pulso'][2] - COLORES['meta'][2]) * t)
        )
        
        for fila in range(self.filas):
            for columna in range(self.columnas):
                rect = pygame.Rect(
                    self.margen_x + columna * self.tamano_celda,
                    self.margen_y + fila * self.tamano_celda,
                    self.tamano_celda, self.tamano_celda
                )
                
                if self.grid[fila][columna] == 1:
                    pygame.draw.rect(pantalla, COLORES['pared'], rect)
                    pygame.draw.line(pantalla, COLORES['pared_sombra'], 
                                   rect.topleft, rect.bottomleft, 3)
                    pygame.draw.line(pantalla, COLORES['pared_sombra'], 
                                   rect.topleft, rect.topright, 3)
                    pygame.draw.line(pantalla, COLORES['pared_brillo'], 
                                   rect.topright, rect.bottomright, 2)
                    pygame.draw.line(pantalla, COLORES['pared_brillo'], 
                                   rect.bottomleft, rect.bottomright, 2)
                elif self.grid[fila][columna] == 0:
                    pygame.draw.rect(pantalla, COLORES['camino'], rect)
                    centro_rect = pygame.Rect(
                        rect.x + self.tamano_celda//4,
                        rect.y + self.tamano_celda//4,
                        self.tamano_celda//2,
                        self.tamano_celda//2
                    )
                    pygame.draw.rect(pantalla, COLORES['camino_ilu'], centro_rect)
                elif self.grid[fila][columna] == 2:
                    if sprite_meta:
                        pantalla.blit(sprite_meta, (self.margen_x + columna * self.tamano_celda,
                                                   self.margen_y + fila * self.tamano_celda))
                    else:
                        pygame.draw.rect(pantalla, color_meta, rect)
                        centro = rect.center
                        pygame.draw.circle(pantalla, COLORES['meta_pulso'], 
                                         centro, int(self.tamano_celda//2.5 * (1 + t * 0.2)), 3)
        
        # Animación suave del jugador
        if self.animacion_t < self.animacion_duracion:
            self.animacion_t += 1/60
            t = min(self.animacion_t / self.animacion_duracion, 1)
            x = self.jugador_pos[0] + (self.jugador_target[0] - self.jugador_pos[0]) * t
            y = self.jugador_pos[1] + (self.jugador_target[1] - self.jugador_pos[1]) * t
        else:
            x, y = self.jugador_target
        
        jugador_rect = pygame.Rect(
            self.margen_x + y * self.tamano_celda + self.tamano_celda//4,
            self.margen_y + x * self.tamano_celda + self.tamano_celda//4,
            self.tamano_celda//2, self.tamano_celda//2
        )
        
        if sprite_jugador:
            pantalla.blit(sprite_jugador, (jugador_rect.x, jugador_rect.y))
        else:
            shadow_rect = pygame.Rect(
                jugador_rect.x, 
                jugador_rect.y + self.tamano_celda//4,
                jugador_rect.width, 
                jugador_rect.height//2
            )
            pygame.draw.ellipse(pantalla, (0, 0, 0, 100), shadow_rect)
            pygame.draw.ellipse(pantalla, COLORES['jugador'], jugador_rect)
            highlight_rect = pygame.Rect(
                jugador_rect.x + 2, 
                jugador_rect.y + 2,
                jugador_rect.width - 4, 
                jugador_rect.height - 4
            )
            pygame.draw.ellipse(pantalla, (255, 255, 255), highlight_rect, 2)
        
        # Dibujar partículas
        for particula in self.particulas[:]:
            particula['pos'][0] += particula['vel'][0]
            particula['pos'][1] += particula['vel'][1]
            particula['vida'] -= 1
            if particula['vida'] <= 0:
                self.particulas.remove(particula)
            else:
                pygame.draw.circle(pantalla, COLORES['particula'], 
                                 (int(particula['pos'][0]), int(particula['pos'][1])), 3)

    def mover_jugador(self, dx, dy):
        x, y = self.jugador_target
        nuevo_x, nuevo_y = x + dx, y + dy
        
        if 0 <= nuevo_x < self.filas and 0 <= nuevo_y < self.columnas and self.grid[nuevo_x][nuevo_y] != 1:
            self.jugador_pos = self.jugador_target[:]
            self.jugador_target = [nuevo_x, nuevo_y]
            self.animacion_t = 0
            if (nuevo_x, nuevo_y) == self.meta_pos:
                self.puntuacion += max(1000 - int(time.time() - self.tiempo_inicio) * 10, 100) * self.nivel
                return True
        return False