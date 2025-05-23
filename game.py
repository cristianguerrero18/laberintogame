import pygame
import random
import time
from settings import ANCHO, pantalla, reloj, musica_fondo, sonido_victoria, COLORES, fuente_secundaria
from laberinto import Laberinto
from utils import mostrar_mensaje
from menu import pantalla_inicio
from boton import Boton

def main():
    estado = pantalla_inicio()
    nivel_actual = 1
    
    def volver_menu():
        nonlocal estado
        estado = pantalla_inicio()
    
    boton_salir = Boton("Salir", ANCHO - 120, 20, 100, 50, volver_menu)
    
    while estado == 'juego':
        laberinto = Laberinto(nivel_actual)
        ejecutando = True
        ganado = False
        
        while ejecutando:
            mouse_pos = pygame.mouse.get_pos()
            boton_salir.actualizar(mouse_pos)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    if os.path.exists('progreso.json'):
                        os.remove('progreso.json')
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if boton_salir.rect.collidepoint(mouse_pos):
                        boton_salir.click()
                        ejecutando = False
                elif evento.type == pygame.KEYDOWN and not ganado:
                    if evento.key == pygame.K_UP:
                        ganado = laberinto.mover_jugador(-1, 0)
                    elif evento.key == pygame.K_DOWN:
                        ganado = laberinto.mover_jugador(1, 0)
                    elif evento.key == pygame.K_LEFT:
                        ganado = laberinto.mover_jugador(0, -1)
                    elif evento.key == pygame.K_RIGHT:
                        ganado = laberinto.mover_jugador(0, 1)
                    elif evento.key == pygame.K_r:
                        break
                    elif evento.key == pygame.K_ESCAPE:
                        estado = pantalla_inicio()
                        ejecutando = False
            
            if ejecutando:
                laberinto.dibujar()
                
                # Panel de información
                panel = pygame.Surface((200, 150), pygame.SRCALPHA)
                panel.fill((0, 0, 0, 150))
                pantalla.blit(panel, (ANCHO - 220, 20))
                
                tiempo_restante = max(0, int(laberinto.tiempo_limite - (time.time() - laberinto.tiempo_inicio)))
                texto_nivel = fuente_secundaria.render(f"Nivel: {laberinto.nivel}", True, COLORES['nivel'])
                texto_tiempo = fuente_secundaria.render(f"Tiempo: {tiempo_restante}s", True, COLORES['texto'])
                texto_puntuacion = fuente_secundaria.render(f"Puntuación: {laberinto.puntuacion}", True, COLORES['texto'])
                
                pantalla.blit(texto_nivel, (ANCHO - 210, 30))
                pantalla.blit(texto_tiempo, (ANCHO - 210, 60))
                pantalla.blit(texto_puntuacion, (ANCHO - 210, 90))
                
                boton_salir.dibujar()
                
                if ganado:
                    for _ in range(20):
                        laberinto.particulas.append({
                            'pos': [laberinto.meta_pos[1] * laberinto.tamano_celda + laberinto.margen_x + laberinto.tamano_celda//2,
                                    laberinto.meta_pos[0] * laberinto.tamano_celda + laberinto.margen_y + laberinto.tamano_celda//2],
                            'vel': [random.uniform(-2, 2), random.uniform(-2, 2)],
                            'vida': 60
                        })
                    if sonido_victoria:
                        sonido_victoria.play()
                    tiempo_nivel = int(time.time() - laberinto.tiempo_inicio)
                    if nivel_actual < 10:
                        mostrar_mensaje(
                            f"¡Nivel {nivel_actual} completado!\nTiempo: {tiempo_nivel}s\nPuntuación: {laberinto.puntuacion}",
                            COLORES['nivel']
                        )
                        nivel_actual += 1
                    else:
                        mostrar_mensaje(
                            f"¡Juego completado!\nTiempo final: {tiempo_nivel}s\nPuntuación total: {laberinto.puntuacion}",
                            COLORES['meta']
                        )
                        mostrar_mensaje("Gracias por jugar", COLORES['texto'])
                        estado = pantalla_inicio()
                    break
                
                if time.time() - laberinto.tiempo_inicio > laberinto.tiempo_limite:
                    mostrar_mensaje("¡Tiempo agotado!\nVolviendo al nivel 1", COLORES['meta'])
                    nivel_actual = 1
                    break
                
                pygame.display.flip()
                reloj.tick(60)
    
    if musica_fondo:
        musica_fondo.stop()
    if os.path.exists('progreso.json'):
        os.remove('progreso.json')
    pygame.quit()
    sys.exit()