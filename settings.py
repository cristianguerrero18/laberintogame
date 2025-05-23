import pygame

# Configuración general
ANCHO, ALTO = 1024, 768
TAMANO_CELDA = 40
COLORES = {
    'fondo_base': (15, 15, 25),  # Fondo base para el gradiente
    'fondo_fin': (50, 50, 70),  # Color final del gradiente
    'pared': (50, 50, 70),  # Base para paredes metálicas
    'pared_sombra': (30, 30, 50),  # Sombra para paredes
    'pared_brillo': (80, 80, 100),  # Brillo para paredes
    'camino': (200, 200, 210),  # Camino con tono suave
    'camino_ilu': (230, 230, 240),  # Iluminación en el camino
    'jugador': (255, 120, 120),  # Jugador vibrante (respaldo)
    'meta': (100, 255, 100),  # Meta verde brillante (respaldo)
    'meta_pulso': (150, 255, 150),  # Pulso para la meta
    'texto': (240, 240, 240),  # Texto claro
    'nivel': (100, 150, 255),  # Color para nivel
    'boton': (70, 70, 90),  # Botón estándar
    'boton_hover': (100, 100, 120),  # Botón en hover
    'particula': (255, 255, 0),  # Color de las partículas (amarillo)
}

# Configurar pantalla y reloj
pygame.init()
pygame.mixer.init()
print("Sistema de audio inicializado correctamente")
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto Profesional")
reloj = pygame.time.Clock()

# Fuentes
try:
    fuente_principal = pygame.font.SysFont('Arial', 48)
    fuente_secundaria = pygame.font.SysFont('Arial', 28)
    fuente_boton = pygame.font.SysFont('Arial', 32)
except:
    fuente_principal = pygame.font.SysFont(None, 48)
    fuente_secundaria = pygame.font.SysFont(None, 28)
    fuente_boton = pygame.font.SysFont(None, 32)

# Cargar música de fondo
try:
    musica_fondo = pygame.mixer.Sound('resources/background_music.mp3')
    musica_fondo.set_volume(1.0)
    musica_fondo.play(-1)
    print("Música de fondo cargada y reproduciendo")
except Exception as e:
    print(f"Error al cargar background_music.mp3: {e}")
    musica_fondo = None

# Cargar sprites
try:
    sprite_jugador = pygame.image.load('resources/jugador.png').convert_alpha()
    sprite_jugador = pygame.transform.scale(sprite_jugador, (TAMANO_CELDA//2, TAMANO_CELDA//2))
    sprite_meta = pygame.image.load('resources/meta.png').convert_alpha()
    sprite_meta = pygame.transform.scale(sprite_meta, (TAMANO_CELDA, TAMANO_CELDA))
except Exception as e:
    print(f"Error al cargar sprites: {e}")
    sprite_jugador = None
    sprite_meta = None

# Sonidos de paso y victoria (desactivados)
sonido_paso = None
sonido_victoria = None