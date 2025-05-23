from settings import pantalla, fuente_boton, COLORES
import pygame

class Boton:
    def __init__(self, texto, x, y, ancho, alto, accion):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.accion = accion
        self.hover = False

    def dibujar(self):
        color = COLORES['boton_hover'] if self.hover else COLORES['boton']
        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, COLORES['texto'], self.rect, 2, border_radius=10)
        texto_surface = fuente_boton.render(self.texto, True, COLORES['texto'])
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        pantalla.blit(texto_surface, texto_rect)

    def actualizar(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.accion:
            self.accion()