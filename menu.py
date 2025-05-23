import pygame
import sys
import os
from settings import ANCHO, ALTO, COLORES, pantalla, fuente_principal, fuente_secundaria, reloj
from boton import Boton

def pantalla_inicio():
    def iniciar_juego():
        nonlocal estado
        estado = 'juego'

    def mostrar_instrucciones():
        pantalla.fill(COLORES['fondo_base'])
        instrucciones = [
            "Instrucciones:",
            "1. Usa las flechas para mover al jugador",
            "2. Llega al cuadro verde antes de que se acabe el tiempo",
            "3. Gana puntos según el tiempo y nivel",
            "4. Presiona R para reiniciar el nivel",
            "5. Presiona ESC o el botón Salir para volver al menú",
            "Presiona cualquier tecla para volver"
        ]
        for i, linea in enumerate(instrucciones):
            texto = fuente_secundaria.render(linea, True, COLORES['texto'])
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//4 + i * 40))
        pygame.display.flip()
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

    def salir_juego():
        if os.path.exists('progreso.json'):
            os.remove('progreso.json')
        pygame.quit()
        sys.exit()

    botones = [
        Boton("Jugar", ANCHO//2 - 100, ALTO//2 - 80, 200, 60, iniciar_juego),
        Boton("Instrucciones", ANCHO//2 - 100, ALTO//2, 200, 60, mostrar_instrucciones),
        Boton("Salir", ANCHO//2 - 100, ALTO//2 + 80, 200, 60, salir_juego)
    ]

    estado = 'menu'
    while estado == 'menu':
        pantalla.fill(COLORES['fondo_base'])
        titulo = fuente_principal.render("LABERINTO PROFESIONAL", True, COLORES['nivel'])
        subtitulo = fuente_secundaria.render("Un desafío de lógica y habilidad", True, COLORES['texto'])
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//4))
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, ALTO//4 + 60))

        mouse_pos = pygame.mouse.get_pos()
        for boton in botones:
            boton.actualizar(mouse_pos)
            boton.dibujar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if os.path.exists('progreso.json'):
                    os.remove('progreso.json')
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for boton in botones:
                    if boton.rect.collidepoint(mouse_pos):
                        boton.click()

        pygame.display.flip()
        reloj.tick(60)
    
    return estado