import pygame
import sys
import os
from settings import ANCHO, ALTO, COLORES, pantalla, fuente_secundaria

def mostrar_mensaje(texto, color=COLORES['texto'], tamaño=36, esperar=True):
    fuente = pygame.font.SysFont('Arial', tamaño) if pygame.font.get_fonts() else pygame.font.SysFont(None, tamaño)
    lineas = texto.split('\n')
    superficies = [fuente.render(linea, True, color) for linea in lineas]
    max_ancho = max(s.get_width() for s in superficies)
    alto_total = sum(s.get_height() for s in superficies) + 10 * (len(lineas) - 1)
    
    s = pygame.Surface((max_ancho + 40, alto_total + 40), pygame.SRCALPHA)
    s.fill((0, 0, 0, 200))
    pantalla.blit(s, (ANCHO//2 - max_ancho//2 - 20, ALTO//2 - alto_total//2 - 20))
    
    y = ALTO//2 - alto_total//2
    for superficie in superficies:
        pantalla.blit(superficie, (ANCHO//2 - superficie.get_width()//2, y))
        y += superficie.get_height() + 10
    
    if esperar:
        texto_continuar = fuente_secundaria.render("Presiona cualquier tecla para continuar", True, COLORES['texto'])
        cont_rect = texto_continuar.get_rect(center=(ANCHO//2, ALTO//2 + alto_total//2 + 30))
        pantalla.blit(texto_continuar, cont_rect)
    
    pygame.display.flip()
    
    if esperar:
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    if os.path.exists('progreso.json'):
                        os.remove('progreso.json')
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    esperando = False